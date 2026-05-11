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

"""QCombobox with checkbox for selecting multiple items."""

from qgis.core import QgsMapLayer
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QStandardItem, QStandardItemModel
from qgis.PyQt.QtWidgets import QStyledItemDelegate


class CheckableComboBox:
    """Basic QCombobox with selectable items."""

    def __init__(self, combobox, select_all=None):
        """Constructor."""
        self.combo = combobox
        self.combo.setEditable(True)  # noqa: QGS202
        self.combo.lineEdit().setReadOnly(True)
        self.model = QStandardItemModel(self.combo)
        self.combo.setModel(self.model)
        self.combo.setItemDelegate(QStyledItemDelegate())
        self.model.itemChanged.connect(self.combo_changed)
        self.combo.lineEdit().textChanged.connect(self.text_changed)
        if select_all:
            self.select_all = select_all
            self.select_all.clicked.connect(self.select_all_clicked)

    def select_all_clicked(self):
        for item in self.model.findItems("*", Qt.MatchFlag.MatchWildcard):
            item.setCheckState(Qt.CheckState.Checked)

    def append_row(self, item: QStandardItem):
        """Add an item to the combobox."""
        item.setEnabled(True)
        item.setCheckable(True)
        item.setSelectable(False)
        self.model.appendRow(item)  # noqa: QGS202

    def combo_changed(self):
        """Slot when the combo has changed."""
        self.text_changed(None)

    def selected_items(self) -> list:
        checked_items = []
        for item in self.model.findItems("*", Qt.MatchFlag.MatchWildcard):
            if item.checkState() == Qt.CheckState.Checked:
                checked_items.append(item.data())
        return checked_items

    def set_selected_items(self, items):
        for item in self.model.findItems("*", Qt.MatchFlag.MatchWildcard):
            checked = item.data() in items
            item.setCheckState(
                Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked
            )

    def text_changed(self, text):
        """Update the preview with all selected items, separated by a comma."""
        label = ", ".join(self.selected_items())
        if text != label:
            self.combo.setEditText(label)


class CheckableFieldComboBox(CheckableComboBox):
    def __init__(self, combobox, select_all=None):
        self.layer = None
        super().__init__(combobox, select_all)

    def set_layer(self, layer):
        self.model.clear()

        if not layer:
            return
        if layer.type() != QgsMapLayer.LayerType.VectorLayer:
            return

        self.layer = layer

        for i, field in enumerate(self.layer.fields()):
            alias = field.alias()
            name = f"{field.name()} ({alias})" if alias else field.name()
            item = QStandardItem(name)
            item.setData(field.name())
            item.setIcon(self.layer.fields().iconForField(i))
            self.append_row(item)
