from abc import ABC, abstractmethod
import os
import zipfile
import numpy as np
import inspect
import sys


class Identifier(ABC):
    """Abstract class to identifier the format of a serialized
       model/dataset

    The class uses Command Chain design pattern and work with
    `FormatIdentifier` to select corresponding Identifier
    """
    format = None

    def __init__(self):
        pass

    @classmethod
    @abstractmethod
    def is_me(cls, path):
        """Identify if this class can handle the given file

        :param path: A path to a serialized model/dataset
        :type path: str
        :return: If the file can be handled by this class.
        :rtype: bool
        """
        pass


class FormatIdentifier():
    """Select a identifier according to the input object

    """

    identifiers = set()

    def __init__(self):
        pass

    @classmethod
    def register(cls, identifier: Identifier):
        """Register a supported identifier

        :param identifier: A identifier class
        :type identifier: Identifier

        """
        cls.identifiers.add(identifier)

    def identify(self, path):
        """Select an identifier according to the input object

        :param path: A path to a serialized model or datasets
        :type path: str

        :return: A identifier corresponding to input object
        :rtype: Identifier

        """

        for _cls in self.identifiers:
            if _cls.is_me(path):
                return _cls

        raise Exception(f'Unable to identify object format: {type(path)}')


class H5(Identifier):
    """
    Use file extension and magic number to identify the file
    """
    format = 'H5'

    @classmethod
    def is_me(cls, path):
        if not (type(path) is str and os.path.exists(path) and
                os.path.isfile(path)):
            return False

        if path.lower().endswith('.h5'):
            return True

        with open(path, 'rb') as f:
            return f.read(8) == bytes.fromhex('894844460d0a1a0a')


class ONNX(Identifier):
    """
    Use file extension and magic number to identify the file
    """
    format = 'ONNX'

    @classmethod
    def is_me(cls, path):
        if not (type(path) is str and os.path.exists(path) and
                os.path.isfile(path)):
            return False

        if path.lower().endswith('.onnx'):
            return True

        # Fixme
        with open(path, 'rb') as f:
            d = f.read(4)
            return d == bytes.fromhex('08031207') or d == bytes.fromhex(
                '08041207')


class NPY(Identifier):
    """
    Use file extension and magic number to identify the file
    """
    format = 'NPY'

    @classmethod
    def is_me(cls, path):
        if not (type(path) is str and os.path.exists(path) and
                os.path.isfile(path)):
            return False
        if path.lower().endswith('.npy'):
            return True
        with open(path, 'rb') as f:
            return f.read(6) == bytes.fromhex('934E554D5059')


class NPYDIR(Identifier):
    """
    Use file extension and magic number to identify the file
    """
    format = 'NPYDIR'

    @classmethod
    def is_me(cls, path):
        if not (type(path) is str and os.path.exists(path) and
                os.path.isdir(path)):
            return False
        files = os.listdir(path)
        if not files:
            return False
        return files[0].lower().endswith('.npy')


class NPZ(Identifier):
    """
    Use file extension and magic number to identify the file
    """
    format = 'NPZ'

    @classmethod
    def is_me(cls, path):
        if not (type(path) is str and os.path.exists(path) and
                os.path.isfile(path)):
            return False

        if path.lower().endswith('.npz'):
            return True

        try:
            with zipfile.ZipFile(path) as archive:
                for name in archive.namelist():
                    if not name.endswith('.npy'):
                        continue

                    npy = archive.open(name)
                    version = np.lib.format.read_magic(npy)
                    return True
        except:
            pass

        return False


class NP_ndarray(Identifier):
    """
    Use file extension and magic number to identify the file
    """
    format = 'NPY'

    @classmethod
    def is_me(cls, x):
        return type(x) is np.ndarray


class NP_memmap(Identifier):
    """
    Use file extension and magic number to identify the file
    """
    format = 'NPY'
    @classmethod
    def is_me(cls, x):
        return type(x) is np.memmap


class NPZFileObject(Identifier):
    """
    Use file extension and magic number to identify the file
    """
    format = 'NPZ'

    @classmethod
    def is_me(cls, x):
        return x.__class__.__name__ == "NpzFile"


class PTH(Identifier):
    """
    Pth archives the model in zip format.

    This identifier determin if the input file is in zip format by magic
    number, then get the file list and check if it match torch strucutre
    """
    format = 'PTH'

    @classmethod
    def is_me(cls, path):
        if not (type(path) is str and os.path.exists(path) and
                os.path.isfile(path)):
            return False

        with open(path, 'rb') as f:
            if not f.read(4) == bytes.fromhex('504b0304'):
                return False

        z = zipfile.ZipFile(path)
        file_names = '|'.join(z.namelist())
        return 'torch/nn' in file_names or 'torch\\nn' in file_names


class PB(Identifier):
    """
    Use file extension and magic number to identify the file
    """

    format = 'PB'

    @classmethod
    def is_me(cls, path):
        if not (type(path) is str and os.path.exists(path) and
                os.path.isfile(path)):
            return False

        # I dont find such pattern in:
        # 1. https://github.com/chen0040/java-tensorflow-samples/blob/master/audio-classifier/src/main/resources/tf_models/resnet-v2.pb
        # 2. https://github.com/bugra/putting-tensorflow-2-models-to-production/blob/master/models/resnet/1538687457/saved_model.pb
        # 3. https://github.com/U-t-k-a-r-s-h/Auto-Labeling-tool-using-Tensorflow/blob/master/Mobilenet.pb
        # 4. https://codechina.csdn.net/shy_201992/human-pose-estimation-opencv/-/blob/master/graph_opt.pb
        #
        # with open(path, 'rb') as f:
        #     if f.read(8) == 'PBDEMS2\0':
        #         return True

        return path.lower().endswith('.pb')


class SavedModel(Identifier):
    """
    Use directory pattern to identify the file
    """

    format = 'SavedModel'

    @classmethod
    def is_me(cls, path):
        if not (type(path) is str and os.path.exists(path) and
                os.path.isdir(path)):
            return False
        return (os.path.exists(os.path.join(path, 'saved_model.pb')) and
                os.path.exists(os.path.join(path, 'variables')))


# Auto register
for name, obj in inspect.getmembers(sys.modules[__name__]):
    if inspect.isclass(obj) and issubclass(
            obj, Identifier) and obj.__name__ != "Identifier":
        FormatIdentifier.register(obj)
