#!/usr/bin/env python3
import argparse
import os
import json
from loguru import logger
from onnc.bench.cli.message import *
from onnc.bench.cli.exceptions import exception_handler
from onnc.bench.cli.exceptions import TemplateListNotFound, BenchExists
from onnc.bench.config import get_bench_templates
from onnc.bench.cli.message import *

templates = get_bench_templates()


def create_infer(template, output):
    if os.path.exists(output):
        exception_handler(BenchExists(output))

    templates = get_bench_templates()

    cmds = ["git clone {} {}".format(templates[template], output)]
    os.system(" && ".join(cmds))
    logger.success(msgCreateInferDone[0].format(template))
    logger.success(msgCreateInferDone[1].format(output))
    logger.success(msgCreateInferDone[2])


def parse_args():
    # type: () -> Args
    templates = get_bench_templates()

    parser = argparse.ArgumentParser(description='ArgumentParser')
    parser.add_argument('-t',
                        '--template',
                        choices=templates.keys(),
                        help='Choose a template')
    parser.add_argument('-o', '--output', required=True, help='Output path.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    create_infer(args.template, args.output)
