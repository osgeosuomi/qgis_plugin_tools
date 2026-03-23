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


import pytest

from ..tools.exceptions import QgsPluginInvalidProjectSetting
from ..tools.settings import (
    get_project_setting,
    get_setting,
    set_project_setting,
    set_setting,
)


def test_set_setting(qgis_new_project):
    set_setting("test_setting", "test_value")
    assert get_setting("test_setting") == "test_value"


def test_get_setting(qgis_new_project):
    assert get_setting("non-existent", 2, int) == 2


def test_get_setting2(qgis_new_project):
    assert get_setting("non-existent", 2, str) == "2"


def test_get_setting3(qgis_new_project):
    assert get_setting("non-existent", 2, bool) is True


def test_set_project_setting(qgis_new_project):
    set_project_setting("test_setting", "test_value")
    assert get_project_setting("test_setting") == "test_value"


def test_get_project_setting(qgis_new_project):
    assert get_project_setting("non-existent", 2, int) == 2


def test_get_project_setting2(qgis_new_project):
    assert get_project_setting("non-existent", "2", str) == "2"


def test_get_project_setting3(qgis_new_project):
    assert get_project_setting("non-existent", True, bool) is True


def test_get_project_setting_throws_error(qgis_new_project):
    with pytest.raises(QgsPluginInvalidProjectSetting):
        get_project_setting("non-existent", 2, list)
