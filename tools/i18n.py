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

"""I18n tools."""

from os.path import join
from typing import Any

from qgis.core import QgsSettings
from qgis.PyQt.QtCore import QFileInfo, QLocale
from qgis.PyQt.QtWidgets import QApplication

from .resources import plugin_name, plugin_path, resources_path, slug_name


def setup_translation(
    file_pattern: str = "{}.qm", folder: str | None = None
) -> tuple[str, str | None]:
    """Find the translation file according to locale.

    :param file_pattern: Custom file pattern to use to find QM files.
    :type file_pattern: basestring

    :param folder: Optional folder to look in if it's not the default.
    :type folder: basestring

    :return: The locale and the file path to the QM file, or None.
    :rtype: (basestring, basestring)
    """
    locale = QgsSettings().value("locale/userLocale", QLocale().name())

    for prefix in ["", f"{plugin_name()}_", f"{slug_name()}_"]:
        for fldr in [folder, plugin_path("i18n"), resources_path("i18n")]:
            prefixed_locale = prefix + locale
            if fldr:
                ts_file = QFileInfo(join(fldr, file_pattern.format(prefixed_locale)))
                if ts_file.exists():
                    return locale, ts_file.absoluteFilePath()

            prefixed_locale = prefix + locale[0:2]
            if fldr:
                ts_file = QFileInfo(join(fldr, file_pattern.format(prefixed_locale)))
                if ts_file.exists():
                    return locale, ts_file.absoluteFilePath()

    return locale, None


def tr(
    text: str,
    *args: Any,
    context: str = "@default",
    **kwargs: Any,
) -> str:
    """Get the translation for a string using Qt translation API.

    We implement this ourselves since we do not inherit QObject.

    :param text: String for translation.
    :param args: arguments to use in formatting.
    :param context: Context of the translation.
    :param kwargs: keyword arguments to use in formatting.

    :returns: Translated version of message.
    """
    # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
    return QApplication.translate(context, text).format(*args, **kwargs)
