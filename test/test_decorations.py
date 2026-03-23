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
    def method_that_fails(self, arg, arg2, kwarg1=None, kwarg2=None):  # noqa: ARG002
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
    messages = qgis_iface.messageBar().get_messages(Qgis.Critical)
    assert "Error message:Please implement" in messages


def test_logging_if_fails_method(initialize_logger, qgis_iface):
    MockClass().method_that_shows_msg()

    messages = qgis_iface.messageBar().get_messages(Qgis.Critical)
    assert "M: Error message:Please implement" in messages


def test_logging_if_fails_without_details(initialize_logger, qgis_iface):
    function_that_fails(1, 2, 3, kwarg2=4)

    messages = qgis_iface.messageBar().get_messages(Qgis.Critical)
    assert "Unhandled exception occurred:Error message" in messages


def test_logging_if_fails_without_details_method(initialize_logger, qgis_iface):
    MockClass().method_that_fails(1, 2, 3, kwarg2=4)

    messages = qgis_iface.messageBar().get_messages(Qgis.Critical)
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
