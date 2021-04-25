import tempfile
import os
from urllib.parse import urljoin
import pytest
import requests
import pathlib

from page_loader import download

FIXTURES_DIR = "fixtures"

URL = "https://this-domain.com"
ERROR_URL = "https://error.com"

OUT_HTML_NAME = "this-domain-com.html"
RES_DIR_NAME = "this-domain-com_files"

RESOURCES = [
    {
        "file_name": "relative.jpg",
        "file_name_out": "this-domain-com-res-relative.jpg",
        "url": "/res/relative.jpg"
    },
    {
        "file_name": "absolute.jpg",
        "file_name_out": "this-domain-com-res-absolute.jpg",
        "url": "/res/absolute.jpg"
    },
    {
        "file_name": "relative.css",
        "file_name_out": "this-domain-com-res-relative.css",
        "url": "res/relative.css"
    },
    {
        "file_name": "absolute.css",
        "file_name_out": "this-domain-com-res-absolute.css",
        "url": "/res/absolute.css"
    },
    {
        "file_name": "relative.js",
        "file_name_out": "this-domain-com-res-relative.js",
        "url": "res/relative.js"
    },
    {
        "file_name": "absolute.js",
        "file_name_out": "this-domain-com-res-absolute.js",
        "url": "/res/absolute.js"
    },
]

map_status_to_route = {
    "500": "server-error",
    "404": "not-found",
    "401": "unauthorized",
    "400": "bad",
    "403": "forbidden",
}


def get_path(file_name):
    dir_path = pathlib.Path(__file__).absolute().parent
    return os.path.join(dir_path, FIXTURES_DIR, file_name)


def read_file(path, mode="r"):
    with open(path, mode) as f:
        result = f.read()
    return result


def read_fixture(file_name, mode="r"):
    return read_file(get_path(file_name), mode)


@pytest.mark.parametrize("status", map_status_to_route.keys())
def test_http_errors(requests_mock, status):
    route = map_status_to_route[status]
    url = urljoin(URL, route)
    requests_mock.get(url, status_code=int(status))

    with tempfile.TemporaryDirectory() as output:
        with pytest.raises(requests.exceptions.HTTPError):
            download(url, output)


def test_page_loader(requests_mock):
    """Check that page loader is working correctly."""
    html = read_fixture("sample_page.html")
    requests_mock.get(URL, text=html)

    for resource in RESOURCES:
        file_name, file_name_out, url = resource.values()
        resource_content = read_fixture(
            os.path.join("res", file_name), "rb"
        )
        requests_mock.get(urljoin(URL, url), content=resource_content)

    with tempfile.TemporaryDirectory() as output:
        html_path = os.path.join(output, OUT_HTML_NAME)
        file_folder_path = os.path.join(output, RES_DIR_NAME)
        output_path = download(URL, output)
        html_content = read_file(html_path)
        expected_html_content = read_fixture("sample_page_out.html")

        assert output_path == html_path
        assert html_content == expected_html_content
        assert len(os.listdir(file_folder_path)) == len(RESOURCES)

        for resource in RESOURCES:
            file_name, file_name_out, url = resource.values()
            resource_path = os.path.join(file_folder_path, file_name_out)
            fixture_resource_path = os.path.join("res", file_name)
            resource_content = read_file(resource_path, "rb")
            expected_resource_content = read_fixture(
                fixture_resource_path, "rb"
            )
            assert resource_content == expected_resource_content

