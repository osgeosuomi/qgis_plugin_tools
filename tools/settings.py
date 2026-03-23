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

from typing import Any

from qgis.core import QgsExpressionContextUtils, QgsProject, QgsSettings
from qgis.PyQt.QtCore import QVariant

from .exceptions import QgsPluginInvalidProjectSetting
from .resources import plugin_name


def setting_key(*args: str) -> str:
    """
    Get QGIS setting key

    :param args List of path elements e.g. ['img', 'logos', 'image.png']
    """
    return "/" + "/".join((plugin_name(), *map(str, args)))


def get_setting(
    key: str,
    default: Any | None = None,
    typehint: type | None = None,
    internal: bool = True,
    section: int = QgsSettings.NoSection,
) -> QVariant | str:
    """
    Get QGIS setting value plugin

    :param key: Key for the setting
    :param default: Optional default value
    :param typehint: Type hint
    :param internal: Whether to search from only plugin settings or all
    :param section: Section argument can be used to get a value from
    a specific Section.
    """
    s = QgsSettings()
    kwargs = {"defaultValue": default, "section": section}

    if typehint is not None:
        kwargs["type"] = typehint
    return s.value(setting_key(key) if internal else key, **kwargs)


def set_setting(
    key: str,
    value: str | int | float | bool,
    internal: bool = True,
    section: int = QgsSettings.NoSection,
) -> bool:
    """
    Set a value in the QgsSetting

    :param key: Key for the setting
    :param value: Value for the setting
    :param internal: Whether to search from only plugin settings or all
    :param section: Section argument can be used to set a value to a specific Section
    """
    qs = QgsSettings()
    return qs.setValue(setting_key(key) if internal else key, value, section)


def get_project_setting(
    key: str,
    default: Any | None = None,
    typehint: type | None = None,
    internal: bool = True,
) -> QVariant | str | None:
    """
    Get QGIS project setting value

    :param key: Key for the setting
    :param default: Optional default value
    :param typehint: Type hint
    :param internal: Whether to search from only plugin settings or all
    :return: Value if conversion is successful, else None
    """
    proj = QgsProject.instance()

    if not internal:
        value = QgsExpressionContextUtils.projectScope(proj).variable(key)
        return value if value is not None else default

    args = [plugin_name(), key]
    if default is not None:
        args.append(default)

    value = None
    conversion_ok = False
    if typehint is not None and typehint is not str:
        try:
            if typehint is int:
                value, conversion_ok = proj.readNumEntry(*args)
            elif typehint is bool:
                value, conversion_ok = proj.readBoolEntry(*args)
            elif typehint is list:
                value, conversion_ok = proj.readListEntry(*args)
        except TypeError as e:
            raise QgsPluginInvalidProjectSetting(str(e)) from e
    else:
        value, conversion_ok = proj.readEntry(*args)
    return value if conversion_ok else default


def set_project_setting(
    key: str, value: str | int | float | bool, internal: bool = True
) -> bool:
    """
    Set a value in the QGIS project settings

    :param key: Key for the setting
    :param value: Value for the setting
    :param internal: Whether to search from only plugin settings or all
    """
    proj = QgsProject.instance()
    if internal:
        return proj.writeEntry(plugin_name(), key, value)
    else:
        QgsExpressionContextUtils.setProjectVariable(proj, key, value)
        return True


def parse_value(value: QVariant | str) -> None | str | bool:
    """
    Parse QSettings value

    :param value: QVariant
    """
    str_value = str(value)
    val: None | str | bool = str_value
    if str_value == "NULL":
        val = None
    elif str_value == "true":
        val = True
    elif str_value == "false":
        val = False
    return val
