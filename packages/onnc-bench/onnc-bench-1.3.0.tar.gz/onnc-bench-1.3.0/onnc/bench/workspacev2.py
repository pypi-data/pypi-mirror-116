import enum
from typing import Any, Callable, List, Union
import os
from .workspace import Workspace


class SampleSource(enum.Enum):
    auto = 0
    keras = 1
    torchvision = 2
    directory = 3


class SampleFormat(enum.Enum):
    numpy = 0
    pb = 1
    fp = 2


class ModelFormat(enum.Enum):
    auto = 0
    keras = 1
    tensorflow = 2
    pytorch = 3


class CompressFormt(enum.Enum):
    none = 0
    zip = 1
    tar = 2


class Samples():
    def __init__(self, data: Any, source: SampleSource=SampleSource.auto):
        self._sample_list: List[Any] = []

    def transform(self, callable: Callable, **optional)->Any:
        callable(self._sample_list, **optional)

    def append(self, sample: Any) -> None:
        self._sample_list.append(sample)

    def remove(self, sample: Any) -> None:
        self._sample_list.remove(sample)

    def __len__(self) -> int:
        return len(self._sample_list)

    @property
    def shape(self) -> List[int]:
        _shape = [1, 3, 224, 224]
        return _shape

    @property
    def is_empty(self) -> bool:
        return len(self._sample_list) == 0

    def clear(self) -> None:
        self._sample_list = []

    def save(self, path: Union[str, os.PathLike],
             format: SampleFormat=SampleFormat.numpy) -> None:
        pass

    def set_method(self, callable: Callable, **optional) -> None:
        pass


class WorkspaceV2():
    def __init__(self, key: str, device: str):
        self.ws = Workspace(key)
        self._rf_vars = {
            "device": device,
            "samples": None,
            "batch": None,
            "model": None,
            "input_name": None,
            "output_name": None,
            "input_as_nchw": None,
        }

    def quantize(self, samples: Samples, batch: int=500):
        self._rf_vars["samples"] = samples
        self._rf_vars["batch"] = batch

    def compile(self, model: Union[str, os.PathLike, object],
                input_name: str=None, output_name: str=None,
                input_as_nchw: str='auto',
                type_: ModelFormat=ModelFormat.auto):

        self._rf_vars["model"] = model
        self._rf_vars["input_name"] = input_name
        self._rf_vars["output_name"] = output_name
        self._rf_vars["input_as_nchw"] = input_as_nchw
        self._rf_vars["type_"] = type_

        self.ws.upload_model(model=self._rf_vars["model"],
                             samples=self._rf_vars["samples"],
                             input_name=self._rf_vars["input_name"],
                             output_name=self._rf_vars["output_name"],
                             input_as_nchw=self._rf_vars["input_as_nchw"]
                             )
        res = self.ws.compile(board=self._rf_vars['device'])
        return res

    def deploy(self, model: Union[str, os.PathLike, object], samples: Samples,
               input_name: str='input_1', output_name: str=None,
               input_as_nchw: str='auto', type_: ModelFormat=ModelFormat.auto,
               batch: int=500):

        self.quantize(samples=samples, batch=batch)
        res = self.compile(model=model, input_name=input_name, 
                           output_name=output_name,
                           input_as_nchw=input_as_nchw,
                           type_=type_)
        return res

    def save(self, path: Union[str, os.PathLike],
             compressed: CompressFormt=CompressFormt.none):
        res = self.ws.download(path)
        if compressed:
            pass
        return res

    def clear(self):
        # explicitly clear workspace. 
        pass

    def close(self):
        # shutdown workspace, delete the remote workspace
        self.ws.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()


def launch(key: str, device: str):
    return WorkspaceV2(key, device)

