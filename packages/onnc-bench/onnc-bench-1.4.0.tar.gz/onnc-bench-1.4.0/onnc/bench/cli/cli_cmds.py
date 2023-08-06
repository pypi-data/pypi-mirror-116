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
@click.argument('workspace', type=click.Path(exists=False))
def onnc_create(workspace):
    """onnc-create creates a WORKSPACE for onnc-bench."""
    if os.path.exists(workspace):
        exception_handler(BenchExists(workspace))

    path = os.path.abspath(workspace)

    os.makedirs(path)

    logger.success(msgONNCCreateDone[0].format(path))

    with open(os.path.join(path, 'LICENSE.txt'), 'w') as f:
        f.close()

    for f in ['build-project.py', 'create-project.py',
              'deploy-project.py']:

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
    if not os.path.exists('LICENSE.txt'):
        exception_handler(NotinONNCBenchDir(os.getcwd()))  # NotinONNCBenchDir()

    if not key:
        logger.info(msgUserRegister)

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
