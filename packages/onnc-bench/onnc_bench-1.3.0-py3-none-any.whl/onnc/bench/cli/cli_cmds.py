"""
1. create directory
2. copy scripts:
    1. build-infer.py
    2. create-infer.py
    3. deploy-infer.py
"""

import os
import click
import jinja2
from loguru import logger

from .exceptions import NotinONNCBenchDir, InvalidONNCApiKey, BenchExists
from .exceptions import exception_handler
from .message import *
from .. import __version__
from . import template_path
from onnc.bench.config import verify_key
import stat


@click.command('onnc-create')
@click.version_option(__version__)
@click.argument('path', type=click.Path(exists=False))
def onnc_create(path):
    if os.path.exists(path):
        exception_handler(BenchExists(path))

    path = os.path.abspath(path)

    os.makedirs(path)

    logger.success(msgONNCCreateDone[0].format(path))

    with open(os.path.join(path, 'LICENSE.txt'), 'w') as f:
        f.close()

    for f in ['build-infer.py', 'create-infer.py',
              'deploy-infer.py']:
        render_infer_template(template_path, f, os.path.join(path, f[:-3]))
        os.chmod(os.path.join(path, f[:-3]),
                 stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR |
                 stat.S_IRGRP | stat.S_IROTH)

    logger.success(msgONNCCreateDone[1].format(path))
    logger.success(msgONNCCreateDone[2].format(path))

@click.command('onnc-login')
@click.version_option(__version__)
@click.option('--key', default=None, help="Your ONNC API key")
def onnc_login(key=None):

    if not key:
        logger.info(msgUserRegister[0])
        logger.info(msgUserRegister[1])

    if not os.path.exists('LICENSE.txt'):
        exception_handler(NotinONNCBenchDir(os.get_cwd()))  # NotinONNCBenchDir()

    if key is None:
        key = click.prompt(msgUserEnterKey, type=str)

    if not verify_key(key):
        exception_handler(InvalidONNCApiKey(key))

    with open('LICENSE.txt', 'w') as f:
        f.write(key)
        f.close()

    logger.success(msgLoginDone)


def render_infer_template(template_dir, template_file, output_file, **kwargs):

    templateLoader = jinja2.FileSystemLoader(searchpath=template_dir)
    templateEnv = jinja2.Environment(loader=templateLoader)

    # Render model->onnx recepie
    template = templateEnv.get_template(template_file)

    script_cont = template.render(**kwargs)

    with open(output_file, 'w') as f:
        f.write(script_cont)
        f.close()

    return output_file
