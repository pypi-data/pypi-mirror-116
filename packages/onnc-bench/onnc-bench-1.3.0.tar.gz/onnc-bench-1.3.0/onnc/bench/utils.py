import tempfile
import os


def get_tmp_path():
    return os.path.join(tempfile._get_default_tempdir(),
                        next(tempfile._get_candidate_names()))


def remove_if_exist(path):
    if type(path) != str:
        return
    if os.path.exists(path):
        print("Remove ", path)
        os.remove(path)
