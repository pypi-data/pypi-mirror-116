from onnc.bench.workspace import Workspace
import unittest
import os

api_key = os.environ['ONNC_APIKEY']

class TestWorkspace(unittest.TestCase):
    def test_create(self):

        try:
            cicd_mode = int(os.environ['ONNC_CICD_MODE'])
        except:
            cicd_mode = 0

        if cicd_mode == 0:
            pre_cmd = [
                'pip uninstall -y onnc-bench',
                'cd ../',
                'pip install .',
            ]
        else:
            pre_cmd = []

        cmds = [
            'rm -rf /tmp/testbench',
            'rm -rf /tmp/output',
            'onnc-create /tmp/testbench',
            'cd /tmp/testbench',
            f'onnc-login --key {api_key}',
            './create-project -t vww -o infer1',
            './build-project -t infer1 -d NUMAKER_IOT_M487',
            './deploy-project -t infer1 -o /tmp/output',
            'rm -rf /tmp/testbench',
            'rm -rf /tmp/output'
        ]
        self.assertEqual(os.system(' && '.join(pre_cmd + cmds)), 0)

