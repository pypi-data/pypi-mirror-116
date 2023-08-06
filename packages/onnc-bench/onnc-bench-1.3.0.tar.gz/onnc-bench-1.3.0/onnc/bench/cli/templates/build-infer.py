#!/usr/bin/env python3
import argparse
import os
import json
from loguru import logger
import sentry_sdk
from sentry_sdk import capture_exception

from onnc.bench import Workspace
from onnc.bench.cli.message import *
from onnc.bench.cli.exceptions import exception_handler
from onnc.bench.cli.exceptions import BenchNotExists, ONNCApiKeyEmpty
from onnc.bench.cli.exceptions import WorkspaceUploadFailure, WorkspaceCompileFailure
from onnc.bench.cli.exceptions import WorkspaceDownloadFailure
from onnc.bench.config import get_device_list
from onnc.bench.cli.message import *

def build_infer(target, board):
    if not os.path.exists(target):
        exception_handler(BenchNotExists(target))

    model = os.path.join(target, 'model.h5')
    samples = os.path.join(target, 'samples.npy')
    input_name = 'input_1'
    report = compile(model, samples, input_name, board,
                     os.path.join(target, 'loadable'))

    with open(os.path.join(target, 'compile_report.json'), 'w') as f:
        f.write(json.dumps(report, indent=4, sort_keys=True))
        f.close()

    with open(os.path.join(target, 'loadable', 'compile_report.json'),
              'w') as f:
        f.write(json.dumps(report, indent=4, sort_keys=True))
        f.close()


def compile(model, samples, input_name, board, output='loadable'):

    with open('LICENSE.txt', 'r') as f:
        api_key = f.read()
        if not api_key:
            exception_handler(ONNCApiKeyEmpty())

    with Workspace(api_key=api_key) as ws:
        logger.success(msgComile[0])
        try:
            res_ul = ws.upload_model(model, samples, input_name=input_name)
        except Exception as e:
            exception_handler(WorkspaceUploadFailure(ws.ws_id))

        logger.success(msgComile[1])

        try:
            res_cmp = ws.compile(board=board)
            logger.info(f'{res_cmp["report"]}')

        except Exception as e:
            capture_exception(e)
            exception_handler(WorkspaceCompileFailure(ws.ws_id))

        logger.success(msgComile[2])

        try:
            res_dl = ws.download(output, unzip=True)
        except Exception as e:
            exception_handler(WorkspaceCompileFailure(ws.ws_id))
        logger.success(msgComile[3])
        logger.success(msgComile[4])

    return res_cmp["report"]


def parse_args():
    supported_devices = get_device_list()

    parser = argparse.ArgumentParser(description='ArgumentParser')
    parser.add_argument('-t', '--target', required=True, help='Output path.')
    parser.add_argument('-b',
                        '--board',
                        choices=(supported_devices.keys()),
                        required=True,
                        help='The model of the MCU board.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    build_infer(args.target, args.board)
