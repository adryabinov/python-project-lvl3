import pathlib
import os
import tests.file as file

FIXTURES_DIR = "fixtures"


def get_path(file_name):
    dir_path = pathlib.Path(__file__).absolute().parent
    return os.path.join(dir_path, FIXTURES_DIR, file_name)


def read(file_name, mode="r"):
    return file.read(get_path(file_name), mode)
