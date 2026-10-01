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

import pytest
from qgis.core import QgsMapLayer, QgsRasterLayer, QgsVectorLayer

from qgis_plugin_tools.utils.typing_utils import require, require_type


def test_require_returns_value():
    value = object()
    assert require(value) is value


def test_require_raises_on_none():
    with pytest.raises(TypeError, match="Layer missing"):
        require(None, "Layer missing")


def test_require_type_returns_narrowed_value():
    layer: QgsMapLayer = QgsVectorLayer("Point?crs=EPSG:4326", "points", "memory")
    assert require_type(layer, QgsVectorLayer) is layer


def test_require_type_raises_on_wrong_type():
    layer = QgsVectorLayer("Point?crs=EPSG:4326", "points", "memory")
    with pytest.raises(TypeError, match="Expected QgsRasterLayer, got QgsVectorLayer"):
        require_type(layer, QgsRasterLayer)


def test_require_type_raises_on_none():
    with pytest.raises(TypeError, match="Layer missing"):
        require_type(None, QgsVectorLayer, "Layer missing")
