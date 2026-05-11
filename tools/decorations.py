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


from collections.abc import Callable
from functools import wraps
from typing import Any

from .exceptions import QgsPluginException
from .i18n import tr
from .messages import MessageBarLogger
from .tasks import FunctionTask


def log_if_fails(
    fn: Callable | None = None, /, *, logger_name: str = __name__
) -> Callable:
    """
    Use this as a decorator with functions and methods that
    might throw uncaught exceptions.
    """

    # caller is at depth 3 (MessageBarLogger log call, this function, actual call)
    message_bar = MessageBarLogger(logger_name, stack_level=3)

    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> None:
            try:
                # Qt injects False into some signals
                if args[1:] != (False,):
                    fn(*args, **kwargs)
                else:
                    fn(*args[:-1], **kwargs)
            except QgsPluginException as e:
                message_bar.exception(e, **e.bar_msg, stack_info=True)
            except Exception as e:
                message_bar.exception(
                    tr("Unhandled exception occurred"), e, stack_info=True
                )

        return wrapper

    if fn is None:
        return decorator

    return decorator(fn)


def taskify(fn: Callable) -> Callable:
    """
    Decoration used to turn any function or method into a FunctionTask task.
    """

    @wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> FunctionTask:
        return FunctionTask(lambda: fn(*args, **kwargs))

    return wrapper
