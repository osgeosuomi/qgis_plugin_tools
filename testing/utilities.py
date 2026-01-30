"""Common functionality used by regression tests."""

import os
import time
import warnings

from qgis.core import QgsApplication, QgsTask
from qgis.PyQt.QtCore import QCoreApplication

from ..tools.exceptions import QgsPluginNotImplementedException
from ..tools.tasks import BaseTask


def get_qgis_app() -> None:
    warnings.warn(
        "get_qgis_app() is deprecated. Use library pytest-qgis instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    raise QgsPluginNotImplementedException(
        "get_qgis_app() is deprecated. Use library pytest-qgis instead."
    )


def is_running_inside_ci() -> bool:
    """Tells whether the plugin is running in CI environment"""
    return int(os.environ.get("QGIS_PLUGIN_IN_CI", "0")) == 1


def is_running_in_tools_module_ci() -> bool:
    return (
        is_running_inside_ci()
        and int(os.environ.get("QGIS_PLUGIN_TOOLS_IN_CI", "0")) == 1
    )


def qgis_supports_temporal() -> bool:
    try:
        from qgis.core import QgsRasterLayerTemporalProperties  # noqa: F401, PLC0415

        return True
    except ImportError:
        return False


class TestTaskRunner:
    """
    This utility class could be used when running tasks in tests.
    """

    success = False
    fail = False
    progress = 0.0

    def completed(self) -> None:
        self.success = True

    def terminated(self) -> None:
        self.fail = True

    def set_progress(self, progress: float) -> None:
        self.progress = progress

    def run_task(
        self,
        task: QgsTask,
        cancel: bool = False,
        sleep_before_cancel: int | float = 0.0,
    ) -> bool:
        """
        Run task and return whether it was successful or not.
        """
        task.taskCompleted.connect(self.completed)
        task.taskTerminated.connect(self.terminated)
        task.progressChanged.connect(self.set_progress)
        QgsApplication.taskManager().addTask(task)

        if cancel:
            time.sleep(sleep_before_cancel)
            task.cancel()

        while not self.success and not self.fail:
            QCoreApplication.processEvents()

        return self.success


class SimpleTask(BaseTask):
    """
    Test task to used in tests needing a simple task.
    """

    def __init__(
        self,
        will_fail: bool = False,
        error_to_raise: type[Exception] = ValueError,
        steps: int = 10,
        sleep_time: float = 0.01,
    ) -> None:
        super().__init__()
        self._will_fail = will_fail
        self._error_to_raise = error_to_raise
        self._steps = steps
        self._sleep_time = sleep_time

    def _run(self) -> bool:
        for i in range(self._steps):
            self.setProgress(i * self._steps)
            if self._will_fail:
                raise self._error_to_raise("custom failure")
            self._check_if_canceled()
            time.sleep(self._sleep_time)
        return True
