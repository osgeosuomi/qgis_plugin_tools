# SPDX-License-Identifier: GPL-2.0-or-later
#
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

import importlib
import sys
from pathlib import Path
from types import ModuleType

import pytest
from qgis.core import QgsApplication

from qgis_plugin_tools.tools.exceptions import PluginNotFoundError
from qgis_plugin_tools.tools.resources import (
    load_ui,
    plugin_name,
    plugin_path,
    profile_path,
    resources_path,
    root_path,
)


@pytest.fixture
def plugin_directory(dummy_plugin: ModuleType) -> Path:
    assert dummy_plugin.__file__ is not None
    return Path(dummy_plugin.__file__).parent


def test_plugin_path_from_outside_of_plugin_uses_loaded_plugin(
    plugin_directory: Path,
):
    assert plugin_path() == str(plugin_directory)
    assert plugin_path("resources", "ui") == str(plugin_directory / "resources" / "ui")


def test_plugin_path_from_plugin(dummy_plugin: ModuleType, plugin_directory: Path):
    assert dummy_plugin.path_from_plugin("metadata.txt") == str(
        plugin_directory / "metadata.txt"
    )


def test_load_ui_at_module_level_during_plugin_import(dummy_plugin: ModuleType):
    try:
        early_ui_plugin = importlib.import_module("early_ui_plugin")
        assert early_ui_plugin.FORM_CLASS.__name__ == "Ui_EarlyDialog"
    finally:
        for module_name in [*sys.modules]:
            if module_name.split(".")[0] == "early_ui_plugin":
                del sys.modules[module_name]


def test_plugin_path_raises_if_no_plugin_is_loaded(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delitem(sys.modules, "dummy_plugin")

    with pytest.raises(PluginNotFoundError, match="Could not determine the plugin"):
        plugin_path()


def test_plugin_name():
    assert plugin_name() == "Dummyplugin"


def test_root_path(plugin_directory: Path):
    assert root_path() == str(plugin_directory.parent)
    assert root_path("test") == str(plugin_directory.parent / "test")


def test_resources_path_points_to_a_plugin_file(plugin_directory: Path):
    assert resources_path("ui", "dialog.ui") == str(
        plugin_directory / "resources" / "ui" / "dialog.ui"
    )


def test_resources_path_raises_if_resource_is_not_found():
    with pytest.raises(FileNotFoundError, match=r"missing\.ui"):
        resources_path("ui", "missing.ui")


def test_load_ui():
    assert load_ui("dialog.ui").__name__ == "Ui_Dialog"


def test_profile_path():
    settings_path = QgsApplication.qgisSettingsDirPath()
    assert profile_path() == settings_path
    assert profile_path("python", "plugins") == str(
        Path(settings_path, "python", "plugins")
    )
