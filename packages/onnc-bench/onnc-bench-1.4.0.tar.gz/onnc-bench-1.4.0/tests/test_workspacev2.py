from onnc.bench.workspace import Workspace
import unittest
import os
import sys
sys.path.append('../')
from onnc.bench import launch

api_key = os.environ['ONNC_APIKEY']


class TestWorkspace(unittest.TestCase):
    def test_h5(self):

        workspace = launch(api_key,
                           'NUMAKER_IOT_M487')

        workspace.quantize('./resources/samples.pb')
        workspace.compile('./resources/model.onnx', 'input_1', 'Identity')

        workspace.quantize('./resources/vww/samples/coco_11x96x96x3.npy')
        workspace.compile('./resources/vww/models/model.h5', 'input_1', 'Identity')

        workspace.close()
