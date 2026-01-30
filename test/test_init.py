"""Tests QGIS plugin init. Modified from unittest to pytest and using plugin_path"""

__author__ = "Tim Sutton <tim@linfiniti.com>, 2026 qgis_plugin_tools contributors"
__revision__ = "$Format:%H$"
__date__ = "17/10/2010"
__license__ = "GPL"
__copyright__ = "Copyright 2012, Australia Indonesia Facility for "

import configparser

import pytest

from ..testing.utilities import is_running_in_tools_module_ci
from ..tools.resources import plugin_path

__copyright__ += "Disaster Reduction"


@pytest.mark.skipif(is_running_in_tools_module_ci(), reason="In CI")
def test_read_init():
    """Test that the plugin __init__ will validate on plugins.qgis.org."""

    # You should update this list according to the latest in
    # https://github.com/qgis/qgis-django/blob/master/qgis-app/
    #        plugins/validator.py

    required_metadata = [
        "name",
        "description",
        "version",
        "qgisMinimumVersion",
        "email",
        "author",
    ]

    file_path = plugin_path("metadata.txt")
    metadata = []
    parser = configparser.ConfigParser()
    parser.optionxform = str
    parser.read(file_path)
    message = f'Cannot find a section named "general" in {file_path}'
    assert parser.has_section("general"), message
    metadata.extend(parser.items("general"))

    for expectation in required_metadata:
        message = (
            f'Cannot find metadata "{expectation}" in metadata source ({file_path}).'
        )

        assert expectation in dict(metadata), message
