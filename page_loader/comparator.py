import os
import requests
import logging
import urllib.parse as up
from bs4 import BeautifulSoup

from page_loader.restools import save_file
from page_loader.restools import save_res
from page_loader.restools import mk_name


logging.basicConfig(level=logging.INFO)


def prepare_res(html, url, folder_path):
    map_tag_to_attr = {
        "link": "href",
        "script": "src",
        "img": "src"
    }
    soup = BeautifulSoup(html, 'html.parser')
    tags = []
    for tag in map_tag_to_attr.keys():
        tags.extend(soup.find_all(tag))

    links = []
    for tag in tags:
        attr = map_tag_to_attr[tag.name]
        link = tag.get(attr)

        if not link:
            continue

        full_url = up.urljoin(f"{url}/", link)

        if up.urlparse(full_url).netloc != up.urlparse(url).netloc:
            continue

        file_name = mk_name(full_url)
        file_path = os.path.join(folder_path, file_name)
        tag[attr] = file_path
        links.append({
            "link": full_url,
            "file_path": file_path
        })
    return links, soup.prettify(formatter="html5")


def download(url, output=os.getcwd()):
    html_name = mk_name(url)
    html_path = os.path.join(output, html_name)
    file_folder_name = mk_name(url, is_dir=True)
    file_folder_path = os.path.join(output, file_folder_name)

    logging.info(f"GET {url}")
    response = requests.get(url)
    response.raise_for_status()
    logging.info("Done.")

    logging.info(f"MAKE RESOURCES DIR AT: '{file_folder_path}'")
    if not os.path.exists(file_folder_path):
        os.mkdir(file_folder_path)
    logging.info("Done.")

    logging.info("Preparing resources...")
    resources, html = prepare_res(response.text, url, file_folder_name)
    logging.info("Done.")

    logging.info("Downloading resources:")
    for resource in resources:
        save_res(resource, output)
    logging.info("Done.")

    logging.info(f"Saving html to {html_path}")
    save_file(html, html_path)
    logging.info("Done.")
    return html_path
