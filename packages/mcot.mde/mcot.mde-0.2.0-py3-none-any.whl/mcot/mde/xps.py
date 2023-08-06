"""
Implements the xps data structure described by Markus Nilsson
(https://github.com/markus-nilsson/md-dmri/blob/master/mdm/readme.txt)

This quantifies multiple diffusion encoding data
"""

import numpy as np
import pandas as pd
from scipy.io import loadmat, savemat
from mcot.maths import spherical
from fsl.data.image import removeExt
from fsl.utils.path import addExt, getExt
import json


def get_sidecar(filename, ) -> "AcquisitionParams":
    """
    Gets the sidecar corresponding to a known file

    :param filename: path of NIFTI image
    :return: corresponding metadata
    """
    basename = removeExt(filename)
    path = addExt(
            basename,
            allowedExts=('.json', '.mat', '.bvals', '.bvecs'),
            fileGroups=[('.bvals', '.bvecs')],
            mustExist=True,
            unambiguous=True
    )
    if getExt(path, ('.json', '.mat', '.bvals', '.bvecs')) in ('.bvals', '.bvecs'):
        return AcquisitionParams.read_bvals_bvecs(
                path, addExt(path, ['.bvecs'], mustExist=True), modality='LTE'
        )
    else:
        return AcquisitionParams.read(path)


class AcquisitionParams(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, value in self.items():
            super().__setitem__(key, np.atleast_1d(value))
        self.auto_update(check=False)

    def __setitem__(self, key, value):
        value = np.atleast_1d(value)
        if value.shape[0] not in (1, self.n):
            raise ValueError(f"new {key} does not have size {self.n}: {value}")
        super().__setitem__(key, value)
        self.auto_update(check=False)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        for key, value in self.items():
            super().__setitem__(key, np.atleast_1d(value))
        self.auto_update(check=False)

    def auto_update(self, check=True):
        """
        Applies all conversions and optionally check consistency in parameters

        Returns itself
        """
        bad_keys = [key for key, arr in self.items() if arr.shape[0] not in (1, self.n)]
        if len(bad_keys) != 0:
            raise ValueError(f'Following keys do not match the expected size of {self.n}: {bad_keys}')
        params = dict(self)
        nparams = 0
        while len(params) != nparams:
            nparams = len(params)
            for (input, output), func in conversions.items():
                if (all(name in params for name in input) and
                        not all(name in params for name in output)):
                    res = func(params)
                    res.update(params)
                    params = res
        super().update(params)
        if check:
            self.check()
        return self

    def check(self, ):
        self.auto_update(False)
        bad_keys = [key for key, arr in self.items() if arr.shape[0] not in (1, self.n)]
        if len(bad_keys) != 0:
            raise ValueError(f'Following keys do not match the expected size of {self.n}: {bad_keys}')
        for (input, output), func in conversions.items():
            if all(name in self for name in input):
                res = func(self)
                for name in res:
                    if not _test(name, self, res):
                        for single in input:
                            print('input', single, self[single])
                        print(name, self[name], res[name])
                        raise ValueError(f"Found an inconsistent values for {name}, when converting from {input}")

    def get_index(self, sort_by=None, **parameters):
        """
        Indexes the volumes based on the parameters

        :param parameters: mapping of parameters to how different they are allowed to be, e.g.

            - xps.get_index(b=100) groups to data into shells with b-values within 100
            - xps.get_index(b=100, te=0) ensures that only volumes with the same TE will be assigned to a given shell
            - NaNs are in the same shell, but in a different shell from everything else

        :param sort_by: name of the parameter to sort the indices by
        :return: (n, ) integer array with the indices (0-based)
        """
        within_range = None
        for name, max_offset in parameters.items():
            arr = self[name]
            if arr.ndim == 1:
                arr = arr[:, None]
            offset = abs(arr[:, None, :] - arr[None, :, :]).max(-1)
            is_nan = ~np.isfinite(arr)
            new_range = (offset <= max_offset) | (is_nan[:, None, :] & is_nan[None, :, :]).any(-1)
            if within_range is None:
                within_range = new_range
            else:
                within_range &= new_range

        if within_range is None:
            return np.zeros(self.n, dtype='int')

        indices = -np.ones(within_range.shape[0], dtype='int')
        while (indices == -1).any():
            nshell = 0
            new_shell = np.zeros(within_range.shape[0], dtype='bool')
            new_shell[np.where(indices == -1)[0][0]] = True
            while nshell != new_shell.sum():
                nshell = new_shell.sum()
                new_shell = within_range[new_shell, :].any(0)
            indices[new_shell] = max(indices) + 1

        if sort_by is not None:
            new_group = self.groupby(indices)
            indices = np.argsort(np.argsort(new_group[sort_by]))[indices]

        return indices

    def to_pandas(self, ):
        """
        Converts to a pandas dataframe (dropping any multi-dimensional parameters)

        :return: resulting dataframe
        """
        return pd.DataFrame.from_dict({key: np.full(self.n, value) if value.size == 1 else value
                                       for key, value in self.items() if np.array(value).ndim <= 1})

    @classmethod
    def from_pandas(cls, df, ) -> 'AcquisitionParams':
        """
        Converts from a pandas dataframe to a dictionary

        :param df: pandas dataframe
        :return:
        """
        res = cls(df.to_dict('series'))
        return res

    def groupby(self, indices, drop=()) -> 'AcquisitionParams':
        """
        Groups the parameters by the indices, taking the mean for all parameters

        :param indices: indices grouping observations in shells (zero-based)
        :param drop: parameters to drop
        :return: new acquisition parameters with one value per shell (total of max(indices) + 1)
        """
        if isinstance(drop, str):
            drop = (drop, )
        df = self.to_pandas().groupby(by=indices).mean()
        for name in ('b_passxx', 'b_passyy', 'b_passzz') + tuple(drop):
            if name in df:
                df.drop(name, axis=1, inplace=True)
        return self.from_pandas(df)

    @property
    def n(self, ):
        """
        Number of observations
        """
        return max(arr.shape[0] for arr in self.values())

    @classmethod
    def from_mat(cls, filename: str) -> 'AcquisitionParams':
        """
        Reads an XPS MDE structure from the matlab file

        :param filename: .mat matlab structure produced by Markus Nilsson md-dmri library
        :return: XPS MDE structure
        """
        conversions = {
            'u': 'bvec',
            'u2': 'bvec2',
        }
        base_obj = loadmat(filename)['xps'][0, 0]
        res = cls({(conversions[name] if name in conversions else name): np.squeeze(base_obj[name])
                   for name in base_obj.dtype.names if name != 'n'})
        return res

    def to_mat(self, filename: str):
        """
        Writes an XPS MDE to a matlab file

        :param filename: .mat matlab structure readable by Markus Nilsson md-dmri library
        """
        conversions = {
            'bvec': 'u',
            'bvec2': 'u2',
        }
        for name in self:
            if name not in conversions:
                conversions[name] = name
        xps = np.zeros((1, 1), dtype=(
                [('n', 'object')] + [(conversions[name], 'object') for name in self if name != 'n']
        ))
        xps['n'] = np.full((1, 1), len(self['b']))
        for name in self:
            xps[0, 0][conversions[name]] = np.atleast_2d(self[name])
        savemat(filename, {'xps': xps})

    def to_json(self, filename: str):
        """
        Writes an XPS MDE structure to a JSON file

        :param filename: .json filename
        """
        def to_list(arr):
            arr = np.asarray(arr)
            if arr.ndim == 0:
                if arr.dtype == 'float':
                    return float(arr)
                elif arr.dtype == 'int':
                    return int(arr)
                elif arr.dtype == 'U':
                    return str(arr)
                else:
                    raise ValueError(f"Unrecognized type {arr.dtype}")
            else:
                return [to_list(val) for val in arr]

        as_dict = {name: to_list(value) for name, value in self.items()}
        with open(filename, 'w') as f:
            json.dump(as_dict, f, indent=4)

    @classmethod
    def from_json(cls, filename: str) -> 'AcquisitionParams':
        """
        Reads an XPS MDE structure from a JSON file

        :param filename: .json file
        :return: XPS MDE structure
        """
        with open(filename, 'r') as f:
            as_dict = json.load(f)
        res = AcquisitionParams(as_dict)
        return res

    @classmethod
    def read(cls, filename: str):
        """
        Reads the acquisition parameters from a JSON or matlab file

        :param filename: filename ending with .json or .mat
        :return: the stored MDE XPS structure
        """
        extension = filename.split('.')[-1]
        if extension.lower() == 'json':
            return cls.from_json(filename)
        elif extension.lower() == 'mat':
            return cls.from_mat(filename)
        else:
            raise IOError(f"Detected extension {extension} not in json or mat")

    def write(self, filename: str):
        """
        Writes the acquisition parameters to a JSON or matlab file

        :param filename: filename ending with .json or .mat
        :return: the stored MDE XPS structure
        """
        extension = filename.split('.')[-1]
        if extension.lower() == 'json':
            return self.to_json(filename)
        elif extension.lower() == 'mat':
            return self.to_mat(filename)
        else:
            raise IOError(f"Detected extension {extension} not in json or mat")

    @classmethod
    def read_bvals_bvecs(cls, bvals_fn, bvecs_fn=None, modality='LTE'):
        """
        Converts bvals/bvecs file into an MDE XPS structure

        :param bvals_fn: file with b-values
        :param bvecs_fn: file with b-vectors
        :param modality: modality (one of LTE, PTE, or STE)
        :return: XPS object
        """
        bvals = np.loadtxt(bvals_fn, dtype='f8').flatten()
        if modality == 'STE':
            return cls(b=bvals, b_delta=0, b_eta=0, theta=0, phi=0, psi=0)
        else:
            bvecs = np.loadtxt(bvecs_fn, dtype='f8')
            if bvecs.shape[1] == bvals.shape[0] and bvecs.shape[1] != 3:
                bvecs = bvecs.T
            if modality == 'PTE':
                b_delta = -0.5
            elif modality == 'LTE':
                b_delta = 1
            else:
                raise ValueError(f'Modality {modality} not one of (LTE, PTE, or STE)')
            if bvecs.shape != (bvals.size, 3):
                raise ValueError("b-vector shape is not (N, 3) as expected")
            res = cls(b=bvals, bvec=bvecs, psi=0, b_delta=b_delta, b_eta=0)
            return res

    def __eq__(self, other):
        if not isinstance(other, dict):
            return False
        if self.keys() != other.keys():
            return False
        for name in self:
            if not _test(name, self, other):
                return False
        return True

    def __getitem__(self, item):
        if isinstance(item, str):
            if item == 'b_symm':
                return self['b_passzz']
            elif item == 'b_perp':
                return (self['b_passxx'] + self['b_passyy']) / 2
            return super().__getitem__(item)
        elif isinstance(item, tuple):
            raise IndexError("AcquisitionParams can not be treated as multi-dimensional")
        else:
            new_dict = {}
            n = self.n
            for name, value in self.items():
                if value.shape[0] == n:
                    new_dict[name] = value[item]
                elif value.shape[0] == 1:
                    new_dict[name] = value
                else:
                    raise ValueError(f"Array stored under {name} has the wrong shape: {value.shape}")
            return AcquisitionParams(new_dict)


conversions = {}


def register_conversion(input, output):
    if isinstance(input, str):
        input = (input, )
    if isinstance(output, str):
        output = (output, )

    def add_func(func):
        def from_params(params):
            res = func(*[np.asarray(params[name]) for name in input])
            if len(output) == 1:
                return {output[0]: res}
            else:
                assert len(output) == len(res)
                return {name: value for name, value in zip(output, res)}
        conversions[(tuple(input), tuple(output))] = from_params
        return func
    return add_func


@register_conversion('bt', 'b')
def bt2b(bt):
    """
    Derives b-value from the b-tensor
    """
    bt = np.asarray(bt)
    return np.sum(bt[:, :3], -1)


@register_conversion('bt', 'btensor')
def bt2btensor(bt):
    """
    Converts flattend b-value into b-tensor using

    :param bt:
    :return:
    """
    bt = np.asarray(bt)
    arr = bt.astype('float')
    arr[:, 3:] *= np.sqrt(0.5)
    indices = np.array([
        [0, 3, 4],
        [3, 1, 5],
        [4, 5, 2],
    ], dtype='i4')
    return arr[:, indices]


@register_conversion('btensor', 'bt')
def btensor2bt(btensor):
    """
    Flattens the b-tensor
    """
    btensor = np.asarray(btensor)
    bflat = btensor[:, [0, 1, 2, 0, 0, 1], [0, 1, 2, 1, 2, 2]]
    bflat[:, 3:] /= np.sqrt(0.5)
    return bflat


@register_conversion('btensor', ('b_passxx', 'b_passyy', 'b_passzz', 'bvec', 'bvec2'))
def decompose(btensor):
    """
    Decomposes the b-tensor into eigen-values and symmetry axis
    """
    L, V = np.linalg.eigh(btensor)
    indices = np.argsort(abs(L - np.mean(L, -1)[:, None]), -1)

    other_idx = list(np.meshgrid(*(np.arange(sz) for sz in L.shape), indexing='ij'))
    other_idx[-1] = indices
    L = L[tuple(other_idx)]

    other_idx = list(np.meshgrid(*(np.arange(sz) for sz in V.shape), indexing='ij'))
    other_idx[-1] = indices[..., None, :]
    V = V[tuple(other_idx)]

    return L[:, 0], L[:, 1], L[:, 2], V[:, :, 2], V[:, :, 0]


@register_conversion(('b_passxx', 'b_passyy', 'b_passzz', 'bvec', 'bvec2'), 'btensor')
def reconstruct(b_passxx, b_passyy, b_passzz, bvec, bvec2):
    """
    Reconstructs the b-tensor based on the eigen-values/vectos
    """
    bvec_yy = np.cross(bvec, bvec2)
    res = (
            b_passxx[:, None, None] * bvec2[:, :, None] * bvec2[:, None, :] +
            b_passyy[:, None, None] * bvec_yy[:, :, None] * bvec_yy[:, None, :] +
            b_passzz[:, None, None] * bvec[:, :, None] * bvec[:, None, :]
    )
    return res


@register_conversion(('bvec', 'bvec2'), ('phi', 'theta', 'psi'))
def fullrot2angle(bvec, bvec2):
    """
    Converts the symmetry + secondary axes to an angle
    """
    bvec_yy = np.cross(bvec, bvec2)
    rotmat = np.stack([bvec2, bvec_yy, bvec], -1)
    return spherical.mat2euler(rotmat)


@register_conversion('bvec', ('phi', 'theta'))
def bvec2angle(bvec):
    """
    Converts the symmetry axis to an angle
    """
    u_rand = np.random.randn(3)
    u_rand /= np.sqrt(np.sum(u_rand ** 2, -1))
    bvec2 = np.cross(bvec, u_rand)
    return fullrot2angle(bvec, bvec2)[:2]


@register_conversion(('phi', 'theta', 'psi'), ('bvec', 'bvec2'))
def angle2fullrot(phi, theta, psi):
    rotmat = spherical.euler2mat(phi, theta, psi)
    return rotmat[:, :, 2], rotmat[:, :, 0]


@register_conversion(('phi', 'theta'), 'bvec')
def angle2bvec(phi, theta):
    return angle2fullrot(phi, theta, 0)[0]


@register_conversion(('b_passxx', 'b_passyy', 'b_passzz'), ('b', 'b_delta', 'b_eta'))
def eigenvalues2shape(bxx, byy, bzz):
    b = (bxx + byy + bzz)
    b_delta = (bzz - (bxx + byy) / 2) / (b + 1e-20)
    b_eta = 1.5 * (byy - bxx) / (b * b_delta + 1e-20)
    return b, b_delta, b_eta


@register_conversion(('b', 'b_delta', 'b_eta'), ('b_passxx', 'b_passyy', 'b_passzz'))
def eigenvalues2shape(b, b_delta, b_eta):
    bxx = b * (1 - b_delta * (1 + b_eta)) / 3
    byy = b * (1 - b_delta * (1 - b_eta)) / 3
    bzz = b * (1 + 2 * b_delta) / 3
    return bxx, byy, bzz


def _test(name, main, comparison):
    if name == 'bvec':
        return np.all(np.isclose(abs((main[name] * comparison[name]).sum(-1)), 1) | (main['b_delta'] == 0))
    elif name == 'bvec2':
        return np.all(np.isclose(abs((main[name] * comparison[name]).sum(-1)), 1) | (main['b_eta'] == 0))
    elif name in ('phi', 'theta'):
        return np.all(np.isclose(main[name], comparison[name]) | (main['b_delta'] == 0))
    elif name == 'psi':
        return np.all(np.isclose(main[name], comparison[name]) | (main['b_eta'] == 0))
    else:
        return np.allclose(main[name], comparison[name])


def concat(*parts):
    """
    Concatenate multiple MDE XPS objects

    :param parts: individual MDE XPS objects
    :return: new MDE XPS object
    """
    dfs = [part.to_pandas() for part in parts]
    return AcquisitionParams.from_pandas(pd.concat(dfs))
