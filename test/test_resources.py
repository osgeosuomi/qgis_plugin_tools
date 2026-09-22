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

from pathlib import Path

from qgis.core import QgsApplication

import qgis_plugin_tools
from qgis_plugin_tools.tools.resources import (
    plugin_path,
    profile_path,
    resources_path,
    root_path,
)

PACKAGE_PATH = Path(qgis_plugin_tools.__file__).parent


def test_plugin_path():
    assert plugin_path() == str(PACKAGE_PATH)
    assert plugin_path("resources", "ui") == str(PACKAGE_PATH / "resources" / "ui")


def test_root_path():
    assert root_path() == str(PACKAGE_PATH.parent)
    assert root_path("test") == str(PACKAGE_PATH.parent / "test")


def test_resources_path_points_to_a_packaged_file():
    assert Path(resources_path("ui", "progress_dialog.ui")).is_file()


def test_profile_path():
    settings_path = QgsApplication.qgisSettingsDirPath()
    assert profile_path() == settings_path
    assert profile_path("python", "plugins") == str(
        Path(settings_path, "python", "plugins")
    )
