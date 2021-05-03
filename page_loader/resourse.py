import os
import re
import requests
from progress.bar import IncrementalBar
import urllib.parse as urlp
from bs4 import BeautifulSoup

PATTERN = '[^a-zA-Z0-9]'

MAP_TAG_TO_ATTR = {
    "link": "href",
    "script": "src",
    "img": "src"
}


def make_name(url: str,
              suffix=".html",
              replacer='-',
              pattern=PATTERN,
              is_dir=False):

    parsed_url = urlp.urlparse(url)
    path, ext = os.path.splitext(parsed_url.path)
    full_name = f"{parsed_url.netloc}{path}"

    formatted_name = re.sub(pattern, replacer, full_name)
    postfix = ext if ext else suffix
    postfix = "_files" if is_dir else postfix
    file_name = f"{formatted_name}{postfix}"

    return file_name


def prepare(html, url, folder_path):

    soup = BeautifulSoup(html, 'html.parser')
    tags = [tag for tag in soup.find_all() if tag.name in MAP_TAG_TO_ATTR]
    links = []

    for tag in tags:
        attr = MAP_TAG_TO_ATTR[tag.name]
        link = tag.get(attr)

        if not link:
            continue

        full_url = urlp.urljoin(f"{url}/", link)

        if urlp.urlparse(full_url).netloc != urlp.urlparse(url).netloc:
            continue

        file_name = make_name(full_url)
        file_path = os.path.join(folder_path, file_name)
        tag[attr] = file_path
        links.append({
            "link": full_url,
            "file_path": file_path
        })
    return links, soup.prettify(formatter="html5")


def download(resource, output):
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


def save(content, path: str, mode="w+"):
    with open(path, mode) as f:
        return f.write(content)
