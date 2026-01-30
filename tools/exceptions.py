__copyright__ = "Copyright 2020-2021, Gispo Ltd, 2026 qgis_plugin_tools contributors"
__license__ = "GPL version 2"
__email__ = "info@gispo.fi"
__revision__ = "$Format:%H$"

from typing import Any

from qgis.PyQt.QtNetwork import QNetworkReply

from .i18n import tr


class QgsPluginException(Exception):  # noqa: N818
    """Use this as a base exception class in custom exceptions"""

    # Override default_msg to set default message in inherited classes
    default_msg = ""

    def __init__(
        self, message: str | None = None, bar_msg: dict[str, Any] | None = None
    ) -> None:
        """
        Initializes the exception with custom bar_msg to be shown in message bar
        :param message: Title of the message
        :param bar_msg: dictionary formed by tools.custom_logging.bar_msg
        """
        if message is None:
            message = self.default_msg
        self.message = message
        super().__init__(message)
        self.bar_msg: dict[str, Any] = bar_msg if bar_msg is not None else {}


class QgsPluginNetworkException(QgsPluginException):
    default_msg = tr("A network error occurred.")

    def __init__(
        self,
        *args: Any,
        error: QNetworkReply.NetworkError | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Initializes the exception with error details so the plugin may process
        different network exceptions differently.
        :param status: The QNetworkReply error type
        """
        self.error = error
        super().__init__(*args, **kwargs)


class QgsPluginNotImplementedException(QgsPluginException):
    pass


class QgsPluginVersionInInvalidFormat(QgsPluginException):
    pass


class QgsPluginInvalidProjectSetting(QgsPluginException):
    pass


class QgsPluginExpressionException(QgsPluginException):
    default_msg = tr("There is an error in the expression")


class TaskInterruptedException(QgsPluginException):
    pass
