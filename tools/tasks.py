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
from collections.abc import Callable
from typing import Any

from qgis.core import QgsTask

from .exceptions import QgsPluginException, TaskInterruptedException
from .i18n import tr
from .messages import MsgBar

LOGGER = logging.getLogger(__name__)


class BaseTask(QgsTask):
    """
    Base class for writing QgsTask classes.
    Provides some utility functionality, like error handling and
    easy canceling.
    """

    def __init__(self) -> None:
        super().__init__(self.name, QgsTask.CanCancel)
        self.exception: Exception | None = None

    @property
    def name(self) -> str:
        return self.__class__.__name__

    def run(self) -> bool:
        """
        Run the task.

        :return: whether task finished successfully or not.
        """

        LOGGER.debug(f"Started task {self.name}")
        try:
            self._check_if_canceled()
            return self._run()
        except Exception as e:
            self.exception = e
            return False

    def finished(self, result: bool) -> None:
        """
        This function is automatically called when the task has completed
        (successfully or not).

        finished is always called from the main thread, so it's safe
        to do GUI operations and raise Python exceptions here.
        :param result: the return value from self.run
        """
        if result:
            LOGGER.debug(
                f"Task {self.name} ended successfully in "
                f"{self.elapsedTime() / 1000:.2f}!"
            )
        elif self.exception is None:
            MsgBar.warning(
                tr("Task {} was not successful", self.name),
                tr("Task was cancelled by user or some dependency tasks failed"),
            )
        else:
            try:
                raise self.exception
            except QgsPluginException as e:
                MsgBar.exception(str(e), **e.bar_msg)
            except Exception as e:
                MsgBar.exception(tr("Unhandled exception occurred"), e)

    def setProgress(self, progress: int | float) -> None:  # noqa: N802
        self._check_if_canceled()
        super().setProgress(progress)

    def _run(self) -> bool:
        """
        Common pitfalls:

        - Do not create and add layers to the project!

        - Do not connect or emit any PyQtSignals

        - Do not use print function!

        - Do not do anything related to GUI!
        """
        raise NotImplementedError()

    def _check_if_canceled(self) -> None:
        """Check if the task has been canceled"""
        if self.isCanceled():
            raise TaskInterruptedException(tr("Task canceled!"))


class FunctionTask(BaseTask):
    """
    Utility class for creating a task out of a function.
    """

    def __init__(self, callback_function: Callable) -> None:
        super().__init__()
        self._callback_function = callback_function
        self.result: Any = None

    def _run(self) -> bool:
        self.result = self._callback_function()
        return True
