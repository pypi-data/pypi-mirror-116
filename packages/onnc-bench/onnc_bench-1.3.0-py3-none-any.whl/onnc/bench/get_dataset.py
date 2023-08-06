import numpy as np
import os
from abc import ABC
from roa import read_only_attributes
from .identifier import *
from .utils import get_tmp_path


@read_only_attributes('samples', 'sample_size', 'dtype', 'sample_shape')
class Dataset(ABC):

    def __init__(self, samples):
        assert len(samples) != 0
        self.samples = samples

    @property
    @abstractmethod
    def sample_size(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def dtype(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def sample_shape(self):
        raise NotImplementedError

    def get_samples(self, k=None):
        if k == None:
            return self.samples
        return self._get_samples(k)

    @abstractmethod
    def _get_samples(self, k):
        pass

    def serialize(self, path=None):
        if not path:
            path = get_tmp_path() + '.npy'
        np.save(path, self.samples)
        return path


class NPDataset(Dataset):
    sample_size = 0
    dtype = None
    sample_shape = None

    def __init__(self, samples):
        super().__init__(samples)
        self.sample_size = len(samples)
        self.dtype = str(self.samples.dtype)
        self.sample_shape = self.samples.shape

    def _get_samples(self, k=-1):
        return self.data if k == -1 else self.data[:k]


def down_sample(samples, k_samples, shuffle, seed):
    assert type(samples) in [np.ndarray, np.memmap]
    if shuffle:
        np.random.seed(seed)
        samples = np.random.permutation(samples)
    return samples[:k_samples]


class Visitor:

    def __init__(self, f):
        self.f = f
        self.cases = {}

    # Create hash map for each dtype
    def case(self, _format):

        def call(fun):
            self.cases[_format] = fun

        return call

    def __call__(self, samples, sample_format, k_samples, shuffle, seed):
        dataset = self.cases[sample_format]
        return dataset(samples, k_samples, shuffle, seed)


@Visitor
def _get_dataset(x):
    pass


@_get_dataset.case(NPY)
def npy_headers(path, k_samples, shuffle, seed):
    samples = np.load(path, mmap_mode='r')
    samples = down_sample(samples, k_samples, shuffle, seed)
    return NPDataset(samples)


@_get_dataset.case(NPYDIR)
def npydir_dataloader(path, k_samples, shuffle, seed):
    files = os.listdir(path)
    if not files:
        return None
    files = down_sample(np.array(files), k_samples, shuffle, seed)
    samples = [np.load(os.path.join(path, f)) for f in files]
    return NPDataset(np.array(samples))


@_get_dataset.case(NPZ)
def npz_headers(path, k_samples, shuffle, seed):
    """
    Since we will load the whole dataset anyway, the following
    method won't be applied:
    Takes a path to an .npz file, which is a Zip archive of .npy files.
    Generates a sequence of (name, shape, np.dtype).

    ref: https://stackoverflow.com/questions/35990775/finding-shape-of-saved-numpy-array-npy-or-npz-without-loading-into-memory
    """
    # npz cannot be accessed as mmap
    # https://stackoverflow.com/questions/29080556/how-does-numpy-handle-mmaps-over-npz-files
    loaded = np.load(path)
    # Use the first key's value as dataset
    assert len(list(iter(loaded.keys()))) == 1
    samples = next(iter(loaded.values()))
    samples = down_sample(samples, k_samples, shuffle, seed)
    return NPDataset(samples)


@_get_dataset.case(NP_ndarray)
def npndarray_headers(samples, k_samples, shuffle, seed):
    samples = down_sample(samples, k_samples, shuffle, seed)
    return NPDataset(samples)

@_get_dataset.case(NP_memmap)
def npmemmap_headers(samples, k_samples, shuffle, seed):
    samples = down_sample(samples, k_samples, shuffle, seed)
    return NPDataset(samples)


@_get_dataset.case(NPZFileObject)
def npz_file_object(loaded, k_samples, shuffle, seed):
    # Use the first key's value as dataset
    assert len(list(iter(loaded.keys()))) == 1
    samples = next(iter(loaded.values()))
    samples = down_sample(samples, k_samples, shuffle, seed)
    return NPDataset(samples)


@_get_dataset.case(PB)
def pb_headers(path, k_samples, shuffle, seed):
    import onnx
    import onnx.numpy_helper
    with open(path, 'rb') as f:
        tensor = onnx.TensorProto()
        tensor.ParseFromString(f.read())
        samples = onnx.numpy_helper.to_array(tensor)
        samples = down_sample(samples, k_samples, shuffle, seed)
        return NPDataset(samples)


def get_dataset(samples, k_samples, shuffle=True, seed=123):
    fi = FormatIdentifier()
    sample_format = fi.identify(samples)
    return _get_dataset(samples,
                        sample_format,
                        k_samples,
                        shuffle=shuffle,
                        seed=seed)
