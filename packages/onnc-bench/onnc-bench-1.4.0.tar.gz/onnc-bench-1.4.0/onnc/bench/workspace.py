from typing import Union
import json
import shutil
import os
import sys
import tempfile
import requests
import zipfile

from .config import api_host
from .utils import get_tmp_path, remove_if_exist
from .get_dataset import get_dataset
from .serializer import ModelSerializerSelector, PytorchSerializer
from .identifier import FormatIdentifier
from .handler import http_resp_handler, SaaSError, AuthenticationError
from .handler import HTTPError


class Workspace(object):
    """ONNC cloud workspace

    """

    def __init__(self, api_key, host=api_host):
        self.host = host
        self.ws_params = {
            "api_key": api_key,
            "ws_id": None,
            "model_id": None,
            "sample_id": None,
            "loadable_id": None,
        }
        self.model_info = {}

        self._create(api_key)

    @property
    def ws_id(self):
        return self.ws_params["ws_id"]

    @http_resp_handler
    def _create(self, api_key: str):
        response = requests.post(f"{self.host}/api/v1/workspace/",
                                 json=self.ws_params)
        return response

    # Future work: this function belong to Model
    def _serialize(self, x, selector, json_, files, shape):
        category = selector.category
        if type(x) != str:
            serializer = selector.select(x)()
            if isinstance(serializer, PytorchSerializer):
                x = serializer.serialize(x, shape)
            else:
                x = serializer.serialize(x)

        if not json_[f"{category}_format"]:
            identifier = FormatIdentifier().identify(x)
            json_[f"{category}_format"] = identifier.format
        if os.path.isdir(x):
            tmp_path = get_tmp_path()
            shutil.make_archive(tmp_path, 'zip', x)
            x = tmp_path + '.zip'
            json_[f"is_{category}_zipped"] = True
        else:
            json_[f"is_{category}_zipped"] = False

        files.append(('files', (category, open(x, 'rb'), 'application/octet')))
        return x


    @http_resp_handler
    def upload_model(self,
                     model: Union[str, object],
                     samples: Union[str, object],
                     input_name: str = None,
                     output_name: str = None,
                     input_as_nchw: str = "auto"):
        """Upload model and it's corresponding calibration samples

        :param model: A file or dir path str to a serialized model or a model\
                      object.
        :type model: Union[str, object]
        :param samples:  A file or dir path str to a serialized Numpy dataset\
                         or a Numpy dataset object.
        :param input_name: The input tensor name of the given model.
        :param output_name: The output tensor name of the given model.
        :param input_as_nchw: should be one of "noset", "auto" and
                               "as_input_name"
            (for tf2onnx)
            - noset:
                Omit --inputs-as-nchw argument
            - auto:
                Apply an auto detected input name to --inputs-as-nchw argument
            - as_input_name:
                Apply input_name to --inputs-as-nchw


        :return: A dictionary contains `success`, `model_id`, `sample_id`

                 For example:
                    {
                        'success': True,
                        'model_id': '',
                        'sample_id': ''
                    }
        :rtype: dict

        """
        assert input_as_nchw in ["noset", "auto", "as_input_name"]
        json_ = {
            "input_name": input_name,
            "input_as_nchw": input_as_nchw,
            "ws_id": self.ws_params["ws_id"],
            "api_key": self.ws_params["api_key"],
            "is_model_zipped": None,
            "is_sample_zipped": None,
            "model_format": None,
            "sample_format": "NPY",
            "is_sample_zipped": False,
            "input_shape": [],
            "dtype": None
        }

        # Samples could be one of the class derived from
        # the Identifier in indentifier.py:
        max_upload_size = 1000
        dataset = get_dataset(samples, max_upload_size)
        input_shape = list(dataset.sample_shape)
        input_shape[0] = 1
        json_.update({"input_shape": input_shape, "dtype": dataset.dtype})
        # Re-sample the dataset if too large
        json_.update({"uploaded_sample_size": dataset.sample_size})

        # Start serializing
        files = []
        model = self._serialize(model, ModelSerializerSelector,
                                json_, files, input_shape)
        files.append(('files', ("sample", open(dataset.serialize(),
                                               'rb'), 'application/octet')))
        files.append(('files', ('json', json.dumps(json_), 'form-data')))

        response = requests.post(f"{self.host}/api/v1/model/", files=files)

        # Remove artifacts
        if type(model) == str:
            remove_if_exist(os.path.join(model, '.zip'))
        return response

    @http_resp_handler
    def compile(self, board: str, ram_size: int = 0):
        """Compil the uploaded model in the workspace


        :param board: The name of supported board
        :type board: str
        :param ram_size: Limit of free RAM size on the board. Please note:
                          This number varies according to the memory usage of
                          OS, application..., you may need to do trail and error
                          to find the optimal value.
        :type board: int
        :return: A dictionary contains `success`, `loadable_id`, `board`,
                 `ram_size`, `report`.

                For example:
                    {
                        'success': success,
                        'loadable_id': loadable_id,
                        'board': board,
                        'ram_size': ram_size,
                        'report': {'ram': ram, 'rom': rom}
                    }
        :rtype: dict

        """
        json_ = {
            "ram_size": ram_size,
            "board": board,
            "ws_id": self.ws_params["ws_id"],
            "api_key": self.ws_params["api_key"],
            "model_id": self.ws_params["model_id"],
            "sample_id": self.ws_params["sample_id"]
        }

        url = f"{self.host}/api/v1/tinyonnc/"
        response = requests.post(url, json=json_)
        return response

    @http_resp_handler
    def download(self, download_path, unzip=True):
        """Download the compiled library and examples

        :param download_path: The path to save the file
        :type download_path: str
        :param unzip: If the workspace unzip the downloaded file
        :type unzip: bool


        :return: A dictionary contains `success`

                 For example:
                     {
                         'success': True,
                     }
        :rtype: dict

        """

        url = f"{self.host}/api/v1/tinyonnc/loadable/"
        response = requests.post(url, json=self.ws_params)

        if unzip:
            _download_path = get_tmp_path()
            if download_path.lower().endswith('.zip'):
                download_path = download_path[:-4]
        else:
            _download_path = download_path
            if not download_path.lower().endswith('.zip'):
                download_path = download_path+'.zip'


        with open(_download_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=512 * 1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
            f.close()

        if unzip:
            with zipfile.ZipFile(_download_path, 'r') as zip_ref:
                zip_ref.extractall(download_path)
        else:
            shutil.move(_download_path, download_path)

        return response

    @http_resp_handler
    def close(self):
        """Close workspace and remove temp files in the cloud

        :return: A dictionary contains `success`

                 For example:
                     {
                         'success': True,
                     }
        :rtype: dict

        """

        response = requests.delete(f"{self.host}/api/v1/workspace/",
                                   json=self.ws_params)
        return response

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()
