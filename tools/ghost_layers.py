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

"""Tools for layers."""

from qgis.core import QgsLayerTreeUtils, QgsMapLayer, QgsProject


def is_ghost_layer(layer: QgsMapLayer) -> bool:
    """Check if the given layer is a ghost layer or not.

    A ghost layer is included in the QgsProject list of layers
    but is not present in the layer tree.

    :param layer: QgsMapLayer coming from the QgsProject.mapLayers.
    :type layer: QgsMapLayer

    :return: If the layer is ghost, IE not found in the legend layer tree.
    :rtype: bool
    """
    # noinspection PyArgumentList
    project = QgsProject.instance()
    # noinspection PyArgumentList
    count = QgsLayerTreeUtils.countMapLayerInTree(project.layerTreeRoot(), layer)
    return count == 0


def remove_all_ghost_layers() -> list[QgsMapLayer]:
    """Remove all ghost layers from project.

    :return: The list of layers name which have been removed.
    :rtype: list
    """
    # noinspection PyArgumentList
    project = QgsProject.instance()
    ghosts = []
    for layer in project.mapLayers().values():
        if is_ghost_layer(layer):
            ghosts.append(layer.name())
            project.removeMapLayer(layer.id())

    project.setDirty(True)
    return ghosts
