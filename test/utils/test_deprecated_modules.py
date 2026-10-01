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

import pytest


@pytest.mark.parametrize(
    ("old_module", "new_module"),
    [
        ("qgis_plugin_tools.tools.misc_utils", "qgis_plugin_tools.utils.misc_utils"),
        (
            "qgis_plugin_tools.widgets.grid_layout_utils",
            "qgis_plugin_tools.utils.grid_layout_utils",
        ),
    ],
)
def test_deprecated_module_reexports_new_module(old_module: str, new_module: str):
    sys.modules.pop(old_module, None)

    with pytest.deprecated_call(match=new_module):
        old = importlib.import_module(old_module)

    new = importlib.import_module(new_module)
    for name in old.__all__:
        assert getattr(old, name) is getattr(new, name)
