import os
import re
import requests
from progress.bar import IncrementalBar
import urllib.parse as up


def save_file(content, path: str, mode="w+"):
    with open(path, mode) as f:
        return f.write(content)


def save_res(resource, output):
    link, file_path = resource.values()

    with open(os.path.join(output, file_path), "wb") as file:
        response = requests.get(link, stream=True)
        total_size_in_bytes = int(response.headers.get("content-length", 0))
        block_size = 1024
        number_of_blocks = total_size_in_bytes // block_size + 1
        with IncrementalBar(
                f"{file_path}",
                max=number_of_blocks,
                suffix="%(percent)d%%"
        ) as bar:
            for data in response.iter_content(block_size):
                file.write(data)
                bar.next()


def mk_name(url: str, suffix=".html", is_dir=False):
    parsed_url = up.urlparse(url)
    path, ext = os.path.splitext(parsed_url.path)
    full_name = f"{parsed_url.netloc}{path}"
    formatted_name = re.sub("[^a-zA-Z0-9]", "-", full_name)
    postfix = ext if ext else suffix
    postfix = "_files" if is_dir else postfix
    filename = f"{formatted_name}{postfix}"

    return filename
