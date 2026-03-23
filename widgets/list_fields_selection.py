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

"""QListWidget with fields selection."""

from qgis.core import QgsVectorLayer
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QAbstractItemView, QListWidget, QListWidgetItem


class ListFieldsSelection(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSelectionMode(QAbstractItemView.MultiSelection)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.layer = None

    def set_layer(self, layer: QgsVectorLayer):
        self.layer = layer

        self.clear()

        for field in self.layer.fields():
            cell = QListWidgetItem()
            alias = field.alias()
            if not alias:
                cell.setText(field.name())
            else:
                cell.setText(f"{field.name()} ({alias})")
            cell.setData(Qt.UserRole, field.name())
            index = layer.fields().indexFromName(field.name())
            if index >= 0:
                cell.setIcon(self.layer.fields().iconForField(index))
            self.addItem(cell)

    def set_selection(self, fields: tuple):
        for i in range(self.count()):
            item = self.item(i)
            item.setSelected(item.data(Qt.UserRole) in fields)

    def selection(self) -> list:
        selection = []
        for i in range(self.count()):
            item = self.item(i)
            if item.isSelected():
                selection.append(item.data(Qt.UserRole))
        return selection
