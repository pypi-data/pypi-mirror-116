from onnc.bench.workspace import Workspace
import unittest
import os

api_key = os.environ['ONNC_APIKEY']

cmds = [
    'pip uninstall -y onnc-bench',
    'cd ../',
    'pip install .',        
    'onnc-create ./testbench',
    'cd ./testbench',
    f'onnc-login --key {api_key}',
    './create-project -t vww -o infer1',
    './build-project -t infer1 -d NUMAKER_IOT_M487',
    './deploy-project -t infer1 -o /tmp/output',
]

os.system(' && '.join(cmds))
