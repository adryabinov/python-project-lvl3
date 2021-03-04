import os

def download(url: str, path: str) -> str:
    abs_path = os.path.abspath(path)

    if not os.path.isdir(abs_path):
        raise IOError (f'{abs_path} is not found')

    return str(abs_path)

