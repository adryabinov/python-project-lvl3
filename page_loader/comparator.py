import os
import re
import urllib.request
import urllib.error
import urllib.parse


def load_url(url: str) -> str:

    response = urllib.request.urlopen(url)
    webContent = response.read()

    return str(webContent)


def save_content(content, path: str):
    with open(path, "w+") as f:
        return f.write(content)


def download(url: str, path: str) -> str:

    abs_path = os.path.abspath(path)

    if not os.path.isdir(abs_path):
        raise IOError(f'{abs_path} is not found')

    path_to_file = os.path.join(
        abs_path,
        url_to_filename(url)
    )

    save_content(load_url(url), path_to_file)

    return str(path_to_file)


def url_to_filename(url: str) -> str:

    drop_scheme_url = re.sub('.*?://', '', url, 1)
    replaced_symbols = re.sub('[^a-zA-Z0-9]', '-', drop_scheme_url)
    filename = f"{replaced_symbols}.html"

    return filename
