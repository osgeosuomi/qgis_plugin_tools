__copyright__ = "Copyright 2020-2021, Gispo Ltd"
__license__ = "GPL version 3"
__email__ = "info@gispo.fi"
__revision__ = "$Format:%H$"

import time

from qgis.core import Qgis

from ..testing.utilities import TestTaskRunner
from ..tools.custom_logging import bar_msg
from ..tools.decorations import log_if_fails, taskify
from ..tools.exceptions import QgsPluginNotImplementedException


@log_if_fails
def function_that_fails(arg, arg2, kwarg1=None, kwarg2=None):
    raise ValueError("Error message")


@log_if_fails
def function_that_shows_msg():
    raise QgsPluginNotImplementedException("Error message", bar_msg("Please implement"))


@taskify
def function_that_runs_as_a_task(arg, kwarg=None):
    for _ in range(10):
        time.sleep(0.01)
    return arg, kwarg


class MockClass:
    @log_if_fails
    def method_that_fails(self, arg, arg2, kwarg1=None, kwarg2=None):
        raise ValueError("M: Error message")

    @log_if_fails
    def method_that_shows_msg(self):
        raise QgsPluginNotImplementedException(
            "M: Error message", bar_msg("Please implement")
        )

    @taskify
    def method_that_runs_as_a_task(self):
        for _ in range(10):
            time.sleep(0.01)
        return True


def test_logging_if_fails(initialize_logger, qgis_iface):
    function_that_shows_msg()
    messages = qgis_iface.messageBar().get_messages(Qgis.MessageLevel.Critical)
    assert "Error message:Please implement" in messages


def test_logging_if_fails_method(initialize_logger, qgis_iface):
    MockClass().method_that_shows_msg()

    messages = qgis_iface.messageBar().get_messages(Qgis.MessageLevel.Critical)
    assert "M: Error message:Please implement" in messages


def test_logging_if_fails_without_details(initialize_logger, qgis_iface):
    function_that_fails(1, 2, 3, kwarg2=4)

    messages = qgis_iface.messageBar().get_messages(Qgis.MessageLevel.Critical)
    assert "Unhandled exception occurred:Error message" in messages


def test_logging_if_fails_without_details_method(initialize_logger, qgis_iface):
    MockClass().method_that_fails(1, 2, 3, kwarg2=4)

    messages = qgis_iface.messageBar().get_messages(Qgis.MessageLevel.Critical)
    assert "Unhandled exception occurred:M: Error message" in messages


def test_taskify(task_runner: TestTaskRunner):
    task = function_that_runs_as_a_task(1, kwarg=2)
    success = task_runner.run_task(task)

    assert success
    assert task.result == (1, 2)


def test_taskify_method(task_runner: TestTaskRunner):
    task = MockClass().method_that_runs_as_a_task()
    success = task_runner.run_task(task)

    assert success
    assert task.result is True
