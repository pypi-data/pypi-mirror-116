#!/usr/bin/env python3
import argparse
import os
import json
import tempfile
import shutil
from loguru import logger
from onnc.bench.cli.message import *
from onnc.bench.cli.exceptions import exception_handler
from onnc.bench.cli.exceptions import TemplateListNotFound, BenchExists
from onnc.bench.config import get_bench_templates
from onnc.bench.cli.message import *

templates = get_bench_templates()


def get_tmp_path():
    return os.path.join(tempfile._get_default_tempdir(),
                        next(tempfile._get_candidate_names()))


def create_infer(template, output):
    if os.path.exists(output):
        exception_handler(BenchExists(output))

    templates = get_bench_templates()
    git_clone_tmp = get_tmp_path()
    output_abs = os.path.abspath(output)

    if os.path.exists(output_abs):
        logger.error(f'Fatal error: destination path {output} already exists and is not an empty directory.')
        exit(1)
    else:
        os.makedirs(output_abs)

    cmds = [
        "git clone {} {}".format(templates[template], git_clone_tmp),
        f"cd {git_clone_tmp}",
        f"git archive main | tar -x -C {output_abs}"
        ]
    os.system(" && ".join(cmds))
    logger.success(msgCreateInferDone[0].format(template))
    logger.success(msgCreateInferDone[1].format(output))
    logger.success(msgCreateInferDone[2])

    shutil.rmtree(git_clone_tmp, ignore_errors=True)

templates = get_bench_templates()


def parse_args():
    # type: () -> Args

    parser = argparse.ArgumentParser(description='`create-project` downloads a project template from ONNC bench github website. It also modifies all environment variables and paths for current workspace.')
    parser.add_argument('-t',
                        '--template',
                        default=None,
                        choices=templates.keys(),
                        help='The name of the template.')
    parser.add_argument('-o', '--output',
                        default=None,
                        help='The name of the project.')

    parser.add_argument('-l', '--list',
                        action='store_true',
                        help='List all available template projects')

    return parser, parser.parse_args()


if __name__ == '__main__':
    parser, args = parse_args()
    if args.list:
        print("Available template list:")
        for idx, t in enumerate(templates.keys()):
            print(f'{idx+1}. {t}')

    elif args.template and args.output:
        create_infer(args.template, args.output)

    else:
        parser.print_help()
        print('')
        print('create-project: error: the following arguments are required: -t/--template, -o/--output')
