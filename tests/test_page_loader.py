import tempfile
import os
import stat
import json
import pytest
import requests
from urllib.parse import urljoin

import tests.fixture as fixture
import tests.file as file

from page_loader import download


URL = "https://this-domain.com"
HTML_NAME = "this-domain-com.html"
FILES_DIR_NAME = "this-domain-com_files"

map_status_to_route = {
    "500": "server-error",
    "404": "not-found",
    "401": "unauthorized",
    "400": "bad",
    "403": "forbidden",
}

map_fs_code_to_error = {
    "2": "No such file or directory",
    "13": "Permission denied",
}

RESOURCES = json.loads(fixture.read('resources_list.json'))


@pytest.mark.parametrize("status", map_status_to_route.keys())
def test_http_errors(requests_mock, status):
    route = map_status_to_route[status]
    url = urljoin(URL, route)
    requests_mock.get(url, status_code=int(status))

    with tempfile.TemporaryDirectory() as output:
        with pytest.raises(requests.exceptions.HTTPError):
            download(url, output)


def test_fs_such_dir_error(requests_mock):
    html = fixture.read("expected.html")
    requests_mock.get(URL, text=html)
    with tempfile.TemporaryDirectory() as output:
        with pytest.raises(FileNotFoundError):
            download(URL, os.path.join(output, 'not_dir'))


def test_fs_permission_error(requests_mock):
    html = fixture.read("expected.html")
    requests_mock.get(URL, text=html)
    with tempfile.TemporaryDirectory() as output:
        os.chmod(output, stat.S_ENFMT)
        with pytest.raises(PermissionError):
            download(URL, output)


def test_page_loader(requests_mock):
    """Check that page loader is working correctly."""
    html = fixture.read("expected.html")
    requests_mock.get(URL, text=html)

    for resource in RESOURCES:
        url = RESOURCES[resource]['url']
        resource_content = fixture.read(
            os.path.join("res", resource), "rb"
        )
        requests_mock.get(urljoin(URL, url), content=resource_content)

    with tempfile.TemporaryDirectory() as output:
        html_path = os.path.join(output, HTML_NAME)
        file_folder_path = os.path.join(output, FILES_DIR_NAME)
        output_path = download(URL, output)
        html_content = file.read(html_path)
        expected_html_content = fixture.read("expexted_downloads.html")

        assert output_path == html_path
        assert html_content == expected_html_content
        assert len(os.listdir(file_folder_path)) == len(RESOURCES)

        for resource in RESOURCES:
            file_name_out = RESOURCES[resource]['file_name_out']
            file_path = os.path.join(file_folder_path, file_name_out)
            fixture_resource_path = os.path.join("res", resource)
            resource_content = file.read(file_path, "rb")
            expected_resource_content = fixture.read(
                fixture_resource_path, "rb"
            )
            assert resource_content == expected_resource_content
