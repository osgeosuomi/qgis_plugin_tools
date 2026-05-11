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


from qgis.core import QgsWkbTypes

from ..tools.layers import LayerType


def test_layer_type():
    assert LayerType.from_wkb_type(QgsWkbTypes.Type.CurvePolygonZM) == LayerType.Polygon
    assert LayerType.from_wkb_type(QgsWkbTypes.Type.MultiPoint) == LayerType.Point
    assert (
        LayerType.from_wkb_type(QgsWkbTypes.Type.MultiLineString25D) == LayerType.Line
    )
