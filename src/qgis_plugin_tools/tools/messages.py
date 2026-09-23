# SPDX-License-Identifier: GPL-2.0-or-later
#
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

import logging
from typing import Any

from qgis_plugin_tools.tools.custom_logging import bar_msg


class MessageBarLogger:
    """logging.Logger like interface to push messages to the
    message bar where necessary with info/warning/etc methods.

    Setup with a logger name that has a message bar set.
    """

    def __init__(self, logger_name: str, stack_level: int = 2) -> None:
        self._logger = logging.getLogger(logger_name)
        self._logger_kwargs: dict[str, Any] = {"stacklevel": stack_level}

    def info(  # noqa: PLR0913, PLR0917
        self,
        message: Any,
        details: Any = "",
        duration: int | None = None,
        success: bool = False,  # noqa: FBT001, FBT002
        exc_info: Exception | None = None,
        stack_info: bool = False,  # noqa: FBT001, FBT002
    ) -> None:
        """Logs info messages to message bar and to other logging handlers
        :param message: Header of the message
        :param details: Longer body of the message. Can be set to empty string.
        :param duration: can be used to specify the message timeout in seconds. If
            ``duration`` is set to 0, then the message must be manually dismissed
            by the user.
        :param success: Whether the message is success message or not
        :param exc_info: Exception of handled exception for capturing traceback
        :param stack_info: Whether to include stack info
        """
        self._logger.info(
            str(message),
            extra=bar_msg(details, duration, success),
            exc_info=exc_info,
            stack_info=stack_info,
            **self._logger_kwargs,
        )
        if details != "":
            self._logger.info(
                str(details),
                exc_info=exc_info,
                stack_info=stack_info,
                **self._logger_kwargs,
            )

    def warning(  # noqa: PLR0913, PLR0917
        self,
        message: Any,
        details: Any = "",
        duration: int | None = None,
        success: bool = False,  # noqa: FBT001, FBT002
        exc_info: Exception | None = None,
        stack_info: bool = False,  # noqa: FBT001, FBT002
    ) -> None:
        """Logs warning messages to message bar and to other logging handlers
        :param message: Header of the message
        :param details: Longer body of the message. Can be set to empty string.
        :param duration: can be used to specify the message timeout in seconds. If
            ``duration`` is set to 0, then the message must be manually dismissed
            by the user.
        :param success: Whether the message is success message or not
        :param exc_info: Exception of handled exception for capturing traceback
        :param stack_info: Whether to include stack info
        """
        self._logger.warning(
            str(message),
            extra=bar_msg(details, duration, success),
            exc_info=exc_info,
            stack_info=stack_info,
            **self._logger_kwargs,
        )
        if details != "":
            self._logger.warning(
                str(details),
                exc_info=exc_info,
                stack_info=stack_info,
                **self._logger_kwargs,
            )

    def error(  # noqa: PLR0913, PLR0917
        self,
        message: Any,
        details: Any = "",
        duration: int | None = None,
        success: bool = False,  # noqa: FBT001, FBT002
        exc_info: Exception | None = None,
        stack_info: bool = False,  # noqa: FBT001, FBT002
    ) -> None:
        """Logs error of risen exception to message bar and to other logging handlers
        :param message: Header of the message
        :param details: Longer body of the message. Can be set to empty string.
        :param duration: can be used to specify the message timeout in seconds. If
            ``duration`` is set to 0, then the message must be manually dismissed
            by the user.
        :param success: Whether the message is success message or not
        :param exc_info: Exception of handled exception for capturing traceback
        :param stack_info: Whether to include stack info
        """
        self._logger.error(
            str(message),
            extra=bar_msg(details, duration, success),
            exc_info=exc_info,
            stack_info=stack_info,
            **self._logger_kwargs,
        )
        if details != "":
            self._logger.error(
                str(details),
                exc_info=exc_info,
                stack_info=stack_info,
                **self._logger_kwargs,
            )

    def exception(  # noqa: PLR0913, PLR0917
        self,
        message: Any,
        details: Any = "",
        duration: int | None = None,
        success: bool = False,  # noqa: FBT001, FBT002
        exc_info: Exception | None = None,
        stack_info: bool = False,  # noqa: FBT001, FBT002
    ) -> None:
        """Logs error with traceback of risen exception to message bar and to
        other logging handlers
        :param message: Header of the message
        :param details: Longer body of the message. Can be set to empty string.
        :param duration: can be used to specify the message timeout in seconds. If
            ``duration`` is set to 0, then the message must be manually dismissed
            by the user.
        :param success: Whether the message is success message or not
        :param exc_info: Exception of handled exception for capturing traceback
        :param stack_info: Whether to include stack info
        """
        # for some reason using logger.exception will essentially have extra stack level
        # even though its not visible on the printed stack (possibly due to exception
        # being a simple helper which calls error internally). use plain error here to
        # have same effective stacklevel on both actual log records. possibly related
        # https://github.com/python/cpython/issues/89334 has been fixed in 3.11+
        self._logger.error(
            str(message),
            extra=bar_msg(details, duration, success),
            stack_info=stack_info,
            exc_info=True,  # noqa: LOG014 - helper is called from except blocks
            **self._logger_kwargs,
        )
        if details != "":
            self._logger.error(
                str(details),
                exc_info=exc_info,
                stack_info=stack_info,
                **self._logger_kwargs,
            )


# publish the old MsgBar with the default logger name
MsgBar = MessageBarLogger(__name__)
