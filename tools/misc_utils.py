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


from qgis.core import QgsRectangle


def extent_to_bbox(extent: QgsRectangle, precision: int = 2) -> str:
    """
    Add extent for the query

    :param extent: QgsRectangle expected to be in the right extent
    :param precision: Precision of coordinates
    :return: string representation xmin,ymin,xmax,ymax
    """

    def rnd(c: float) -> float:
        return round(c, precision)

    bbox = (
        rnd(extent.xMinimum()),
        rnd(extent.yMinimum()),
        rnd(extent.xMaximum()),
        rnd(extent.yMaximum()),
    )
    return ",".join(map(str, bbox))
