# Copyright (C)
# - 2019-2020 3Liz, info@3liz.org
# - 2020-2025 Gispo OY, info@gispo.fi
# - 2022-2026 qgis_plugin_tools contributors, info@osgeo.fi
#
# This file is part of qgis_plugin_tools.
#
# qgis_plugin_tools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# qgis_plugin_tools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with qgis_plugin_tools.  If not, see <https://www.gnu.org/licenses/>.


import json
from io import BytesIO
from typing import Any

import pytest

from ..tools import network
from ..tools.exceptions import QgsPluginNetworkException
from ..tools.network import download_to_file, fetch, post


def test_fetch(qgis_new_project, mocker):
    def fake_request_raw(*args: Any) -> tuple[bytes, str]:
        url = args[0]
        method = args[1]
        encoding = args[2]
        params = args[4]
        assert method == "get"
        assert url == "https://httpbin.org/get"
        assert params is None
        return json.dumps({"url": url}).encode(encoding), ""

    mocker.patch.object(network, "request_raw", side_effect=fake_request_raw)
    data = fetch("https://httpbin.org/get")
    data = json.loads(data)
    assert data["url"] == "https://httpbin.org/get"


def test_fetch_invalid_url(qgis_new_project):
    with pytest.raises(QgsPluginNetworkException):
        fetch("invalidurl")


def test_fetch_params(qgis_new_project, mocker):
    def fake_request_raw(*args: Any) -> tuple[bytes, str]:
        url = args[0]
        method = args[1]
        encoding = args[2]
        params = args[4]
        assert method == "get"
        assert url == "https://httpbin.org/get"
        assert params == {"foo": "bar"}
        payload = {"url": f"{url}?foo=bar", "args": params}
        return json.dumps(payload).encode(encoding), ""

    mocker.patch.object(network, "request_raw", side_effect=fake_request_raw)
    data = fetch("https://httpbin.org/get", params={"foo": "bar"})
    data = json.loads(data)
    assert data["url"] == "https://httpbin.org/get?foo=bar"
    assert data["args"] == {"foo": "bar"}


def test_post(qgis_new_project, mocker):
    def fake_request_raw(*args: Any) -> tuple[bytes, str]:
        url = args[0]
        method = args[1]
        encoding = args[2]
        params = args[4]
        data = args[5]
        files = args[6]
        assert method == "post"
        assert url == "https://httpbin.org/post"
        assert params is None
        assert data is None
        assert files is None
        return json.dumps({"url": url}).encode(encoding), ""

    mocker.patch.object(network, "request_raw", side_effect=fake_request_raw)
    data = post("https://httpbin.org/post")
    data = json.loads(data)
    assert data["url"] == "https://httpbin.org/post"


def test_post_invalid_url(qgis_new_project):
    with pytest.raises(QgsPluginNetworkException):
        post("invalidurl")


def test_post_data(qgis_new_project, mocker):
    def fake_request_raw(*args: Any) -> tuple[bytes, str]:
        url = args[0]
        method = args[1]
        encoding = args[2]
        params = args[4]
        data = args[5]
        files = args[6]
        assert method == "post"
        assert url == "https://httpbin.org/post"
        assert params is None
        assert data == {"foo": "bar"}
        assert files is None
        payload = {"url": url, "data": json.dumps(data)}
        return json.dumps(payload).encode(encoding), ""

    mocker.patch.object(network, "request_raw", side_effect=fake_request_raw)
    data = post("https://httpbin.org/post", data={"foo": "bar"})
    data = json.loads(data)
    assert data["url"] == "https://httpbin.org/post"
    assert data["data"] == json.dumps({"foo": "bar"})


def test_upload_file(qgis_new_project, file_fixture, mocker):
    file_name, file_content, file_type = file_fixture

    def fake_request_raw(*args: Any) -> tuple[bytes, str]:
        url = args[0]
        method = args[1]
        encoding = args[2]
        params = args[4]
        data = args[5]
        files = args[6]
        assert method == "post"
        assert url == "https://httpbin.org/post"
        assert params is None
        assert data is None
        assert files == [("file", (file_name, file_content, file_type))]
        payload = {"url": url, "files": {"file": files[0][1][1].decode(encoding)}}
        return json.dumps(payload).encode(encoding), ""

    mocker.patch.object(network, "request_raw", side_effect=fake_request_raw)
    data = post(
        "https://httpbin.org/post",
        files=[("file", (file_name, file_content, file_type))],
    )
    data = json.loads(data)
    assert data["url"] == "https://httpbin.org/post"
    assert data["files"]
    assert bytes(data["files"]["file"], "utf-8") == file_content


def test_upload_multiple_files(
    qgis_new_project, file_fixture, another_file_fixture, mocker
):
    file_name, file_content, file_type = file_fixture
    another_file_name, another_file_content, another_file_type = another_file_fixture

    def fake_request_raw(*args: Any) -> tuple[bytes, str]:
        url = args[0]
        method = args[1]
        encoding = args[2]
        params = args[4]
        data = args[5]
        files = args[6]
        assert method == "post"
        assert url == "https://httpbin.org/post"
        assert params is None
        assert data is None
        assert files == [
            ("file", (file_name, file_content, file_type)),
            (
                "another_file",
                (another_file_name, another_file_content, another_file_type),
            ),
        ]
        payload = {
            "url": url,
            "files": {
                "file": files[0][1][1].decode(encoding),
                "another_file": files[1][1][1].decode(encoding),
            },
        }
        return json.dumps(payload).encode(encoding), ""

    mocker.patch.object(network, "request_raw", side_effect=fake_request_raw)
    data = post(
        "https://httpbin.org/post",
        files=[
            ("file", (file_name, file_content, file_type)),
            (
                "another_file",
                (another_file_name, another_file_content, another_file_type),
            ),
        ],
    )
    data = json.loads(data)
    assert data["url"] == "https://httpbin.org/post"
    assert data["files"]
    assert bytes(data["files"]["file"], "utf-8") == file_content
    assert bytes(data["files"]["another_file"], "utf-8") == another_file_content


def test_download_to_file(qgis_new_project, tmpdir, mocker):
    content = b"test response"

    class MockResponse:
        def __init__(self, raw_content: bytes):
            self.status_code = 200
            self.text = ""
            self.headers: dict[str, str] = {}
            self.raw = BytesIO(raw_content)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def raise_for_status(self):
            return None

    class MockRequests:
        @staticmethod
        def get(url: str, stream: bool = False) -> MockResponse:
            assert (
                url
                == "https://twitter.com/gispofinland/status/1324599933337567232/photo/1"
            )
            assert stream
            return MockResponse(content)

    mocker.patch.object(network, "requests", MockRequests())
    path_to_file = download_to_file(
        "https://twitter.com/gispofinland/status/1324599933337567232/photo/1",
        tmpdir,
        "test_file",
    )
    assert path_to_file.exists()
    assert path_to_file.is_file()
    assert path_to_file.read_bytes() == content


def test_download_to_file_without_requests(qgis_new_project, tmpdir, mocker):
    content = b"test response without requests"

    def fake_fetch_raw(url: str, encoding: str = "utf-8") -> tuple[bytes, str]:
        assert (
            url == "https://twitter.com/gispofinland/status/1324599933337567232/photo/1"
        )
        assert encoding == "utf-8"
        return content, ""

    mocker.patch.object(network, "fetch_raw", side_effect=fake_fetch_raw)
    path_to_file = download_to_file(
        "https://twitter.com/gispofinland/status/1324599933337567232/photo/1",
        tmpdir,
        "test_file",
        use_requests_if_available=False,
    )
    assert path_to_file.exists()
    assert path_to_file.is_file()
    assert path_to_file.read_bytes() == content


def test_download_to_file_with_name(qgis_new_project, tmpdir):
    path_to_file = download_to_file(
        "https://raw.githubusercontent.com/GispoCoding/FMI2QGIS/master/FMI2QGIS/test/data/aq_small.nc",
        tmpdir,
    )
    assert path_to_file.exists()
    assert path_to_file.is_file()
    assert path_to_file.name == "aq_small.nc"


def test_download_to_file_invalid_url(qgis_new_project, tmpdir):
    with pytest.raises(QgsPluginNetworkException):
        download_to_file("invalidurl", tmpdir)


def test_download_to_file_invalid_url_without_requests(qgis_new_project, tmpdir):
    with pytest.raises(QgsPluginNetworkException):
        download_to_file("invalidurl", tmpdir)
