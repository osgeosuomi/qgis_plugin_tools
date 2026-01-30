"""I18n tools."""

from os.path import join
from typing import Any

from qgis.core import QgsSettings
from qgis.PyQt.QtCore import QFileInfo, QLocale
from qgis.PyQt.QtWidgets import QApplication

from .resources import plugin_name, plugin_path, resources_path, slug_name

__copyright__ = (
    "Copyright 2019, 3Liz, 2020-2021 Gispo Ltd, 2026 qgis_plugin_tools contributors"
)
__license__ = "GPL version 3"
__email__ = "info@3liz.org"
__revision__ = "$Format:%H$"


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
