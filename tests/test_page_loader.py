import tempfile
import pathlib
import os
import stat
import json
import pytest
import requests
from urllib.parse import urljoin
from page_loader import download


URL = "https://this-domain.com"
HTML_NAME = "this-domain-com.html"
RESOURCES_DIR_NAME = "this-domain-com_files"
FIXTURES_DIR = "fixtures"

map_status_to_route = {
    "500": "server-error",
    "404": "not-found",
    "401": "unauthorized",
    "400": "bad",
    "403": "forbidden",
}


def read_file(path, mode="r"):
    with open(path, mode) as f:
        result = f.read()
    return result


def get_path(file_name):
    dir_path = pathlib.Path(__file__).absolute().parent
    return os.path.join(dir_path, FIXTURES_DIR, file_name)


def read_fixture(fixture_name, mode="r"):
    return read_file(get_path(fixture_name), mode)


RESOURCES = json.loads(read_fixture('resources.json'))


@pytest.mark.parametrize("status", map_status_to_route.keys())
def test_http_errors(requests_mock, status):
    route = map_status_to_route[status]
    url = urljoin(URL, route)
    requests_mock.get(url, status_code=int(status))

    with tempfile.TemporaryDirectory() as output:
        with pytest.raises(requests.exceptions.HTTPError):
            download(url, output)


def test_not_found_error(requests_mock):
    html = read_fixture("index.html")
    requests_mock.get(URL, text=html)
    with tempfile.TemporaryDirectory() as output:
        with pytest.raises(FileNotFoundError):
            download(URL, os.path.join(output, "not_dir"))


def test_not_dir_error(requests_mock):
    html = read_fixture("index.html")
    requests_mock.get(URL, text=html)
    with tempfile.TemporaryDirectory() as output:
        _, tmp_path = tempfile.mkstemp(dir=os.path.abspath(output))
        with pytest.raises(NotADirectoryError):
            download(URL, tmp_path)


def test_fs_permission_error(requests_mock):
    html = read_fixture("index.html")
    requests_mock.get(URL, text=html)
    with tempfile.TemporaryDirectory() as output:
        os.chmod(output, stat.S_ENFMT)
        with pytest.raises(PermissionError):
            download(URL, output)


def test_page_loader(requests_mock):
    html = read_fixture("index.html")
    requests_mock.get(URL, text=html)

    for resource in RESOURCES:
        url = RESOURCES[resource]["url"]
        output_content = read_fixture(
            os.path.join("res", resource), "rb"
        )
        requests_mock.get(urljoin(URL, url), content=output_content)

    with tempfile.TemporaryDirectory() as output:
        html_path = os.path.join(output, HTML_NAME)
        resources_dir_path = os.path.join(output, RESOURCES_DIR_NAME)
        output_path = download(URL, output)
        html_content = read_file(html_path)
        expected_html_content = read_fixture("expected-index.html")

        assert output_path == html_path
        assert html_content == expected_html_content
        assert len(os.listdir(resources_dir_path)) == len(RESOURCES)

        for resource in RESOURCES:
            output_name = RESOURCES[resource]["expected_name"]
            output_path = os.path.join(resources_dir_path, output_name)
            fixture_path = os.path.join("res", resource)
            output_content = read_file(output_path, "rb")
            expected_content = read_fixture(
                fixture_path, "rb"
            )
            assert output_content == expected_content
