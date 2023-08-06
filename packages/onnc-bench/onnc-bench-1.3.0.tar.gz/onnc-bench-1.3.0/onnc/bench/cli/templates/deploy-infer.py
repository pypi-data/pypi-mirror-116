#!/usr/bin/env python3
import shutil
import os
import argparse
from loguru import logger
from onnc.bench.cli.message import *
from onnc.bench.cli.exceptions import *
from onnc.bench.cli.message import *


def deploy_infer(bench, output):
    if os.path.exists(output):
        exception_handler(DeployExists(output))

    if not os.path.exists(bench):
        exception_handler(BenchNotExists(output))

    shutil.copytree(os.path.join(bench, 'loadable'), output)

    logger.success(msgDeployDone[0])
    logger.success(msgDeployDone[1])


def parse_args():
    # type: () -> Args
    parser = argparse.ArgumentParser(description='ArgumentParser')
    parser.add_argument('-t',
                        '--target',
                        type=str,
                        help='The name of the bench')
    parser.add_argument('-o', '--output', required=True, help='Output path.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    deploy_infer(args.target, args.output)
