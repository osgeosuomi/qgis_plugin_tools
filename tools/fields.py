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

from qgis.core import QgsApplication, QgsFields
from qgis.gui import QgsDateTimeEdit, QgsDoubleSpinBox, QgsSpinBox
from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QCheckBox, QComboBox, QDateEdit, QWidget


# noinspection PyCallByClass,PyArgumentList
def variant_type_icon(field_type: QVariant) -> QIcon:  # noqa: PLR0911
    if field_type == QVariant.Bool:
        return QgsApplication.getThemeIcon("/mIconFieldBool.svg")
    elif field_type in [
        QVariant.Int,
        QVariant.UInt,
        QVariant.LongLong,
        QVariant.ULongLong,
    ]:
        return QgsApplication.getThemeIcon("/mIconFieldInteger.svg")
    elif field_type == QVariant.Double:
        return QgsApplication.getThemeIcon("/mIconFieldFloat.svg")
    elif field_type == QVariant.String:
        return QgsApplication.getThemeIcon("/mIconFieldText.svg")
    elif field_type == QVariant.Date:
        return QgsApplication.getThemeIcon("/mIconFieldDate.svg")
    elif field_type == QVariant.DateTime:
        return QgsApplication.getThemeIcon("/mIconFieldDateTime.svg")
    elif field_type == QVariant.Time:
        return QgsApplication.getThemeIcon("/mIconFieldTime.svg")
    elif field_type == QVariant.ByteArray:
        return QgsApplication.getThemeIcon("/mIconFieldBinary.svg")
    else:
        return QIcon()


def widget_for_field(field_type: QVariant) -> QWidget:  # noqa: PLR0911
    q_combo_box = QComboBox()
    q_combo_box.setEditable(True)

    if field_type == QVariant.Bool:
        return QCheckBox()
    elif field_type in [
        QVariant.Int,
        QVariant.UInt,
        QVariant.LongLong,
        QVariant.ULongLong,
    ]:
        spin_box = QgsSpinBox()
        spin_box.setMaximum(2147483647)
        return spin_box
    elif field_type == QVariant.Double:
        spin_box = QgsDoubleSpinBox()
        spin_box.setMaximum(2147483647)
        return spin_box
    elif field_type == QVariant.String:
        return q_combo_box
    elif field_type == QVariant.Date:
        return QDateEdit()
    elif field_type in (QVariant.DateTime, QVariant.Time):
        return QgsDateTimeEdit()
    elif field_type == QVariant.ByteArray:
        return q_combo_box
    else:
        return q_combo_box


def value_for_widget(widget: type[QWidget]) -> str | bool | float | int:
    if isinstance(widget, QComboBox):
        return widget.currentText()
    elif isinstance(widget, QCheckBox):
        return widget.isChecked()
    elif isinstance(widget, QgsDateTimeEdit):
        return widget.dateTime().toString("yyyy-MM-dd hh:mm:ss")
    elif isinstance(widget, (QgsSpinBox, QgsDoubleSpinBox)):
        return widget.value()
    else:
        return str(widget.text())


def provider_fields(fields: QgsFields) -> QgsFields:
    flds = QgsFields()
    for i in range(fields.count()):
        if fields.fieldOrigin(i) == QgsFields.OriginProvider:
            flds.append(fields.at(i))
    return flds
