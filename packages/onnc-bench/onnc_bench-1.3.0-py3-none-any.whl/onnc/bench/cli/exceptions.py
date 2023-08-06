from .message import *
from loguru import logger


class NotinONNCBenchDir(Exception):
    def __init__(self, folder):
        self.message = msgNotinONNCBenchDir.format(folder)
        self.code = 10


class InvalidONNCApiKey(Exception):
    def __init__(self, key):
        self.message = msgInvalidONNCApiKey.format(key)
        self.code = 20


class BenchExists(Exception):
    def __init__(self, path):
        self.message = msgBenchExists.format(path)
        self.code = 30


class DeployExists(Exception):
    def __init__(self, path):
        self.message = msgDeployExists.format(path)
        self.code = 40


class BenchNotExists(Exception):
    def __init__(self, path):
        self.message = msgBenchNotExists.format(path)
        self.code = 60


class TemplateListNotFound(Exception):
    def __init__(self, path):
        self.message = msgTemplateListNotFound.format(path)
        self.code = 70


class ONNCApiKeyEmpty(Exception):
    def __init__(self):
        self.message = msgONNCApiKeyEmpty.format()
        self.code = 80


class WorkspaceUploadFailure(Exception):
    def __init__(self, ws_id):
        self.message = msgWorkspaceUploadFailure.format(ws_id)
        self.code = 300


class WorkspaceCompileFailure(Exception):
    def __init__(self, ws_id):
        self.message = msgWorkspaceCompileFailure.format(ws_id)
        self.code = 310


class WorkspaceDownloadFailure(Exception):
    def __init__(self, ws_id):
        self.message = msgWorkspaceDownloadFailure.format(ws_id)
        self.code = 320


def exception_handler(e):
    logger.error(f"CODE:{e.code}|{e.message}")
    exit(1)