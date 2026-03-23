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

"""QListWidget with layers selection."""

from qgis.core import QgsMapLayer, QgsMapLayerModel, QgsProject
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QAbstractItemView, QListWidget, QListWidgetItem, QWidget


class ListLayersSelection(QListWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setSelectionMode(QAbstractItemView.MultiSelection)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.project: QgsProject | None = None

    def set_project(self, project: QgsProject) -> None:
        self.project = project

        self.clear()

        for layer in self.project.mapLayers().values():
            if layer.type() != QgsMapLayer.VectorLayer:
                continue

            if not layer.isSpatial():
                continue

            cell = QListWidgetItem()
            cell.setText(layer.name())
            cell.setData(Qt.UserRole, layer.id())
            cell.setIcon(QgsMapLayerModel.iconForLayer(layer))
            self.addItem(cell)

    def set_selection(self, layers: tuple) -> None:
        for i in range(self.count()):
            item = self.item(i)
            item.setSelected(item.data(Qt.UserRole) in layers)

    def selection(self) -> list:
        selection = []
        for i in range(self.count()):
            item = self.item(i)
            if item.isSelected():
                selection.append(item.data(Qt.UserRole))
        return selection
