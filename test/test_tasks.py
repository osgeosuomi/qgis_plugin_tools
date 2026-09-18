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
from typing import Any

from qgis.core import Qgis

from ..testing.utilities import SimpleTask, TestTaskRunner
from ..tools.exceptions import QgsPluginException, TaskInterruptedException
from ..tools.tasks import FunctionTask


def fn(*args: Any, **kwargs: Any):  # noqa: ANN003
    for _ in range(10):
        time.sleep(0.01)
    return args, kwargs


def test_run_simple_task(task_runner: TestTaskRunner):
    task = SimpleTask()
    success = task_runner.run_task(task)

    assert success
    assert task_runner.progress == 100


def test_run_simple_task_canceled(task_runner: TestTaskRunner, qgis_iface, qtbot):
    task = SimpleTask()
    success = task_runner.run_task(task, cancel=True)

    # for some reason this randomly fails if the signal is not waited for
    qtbot.waitSignal(task.taskTerminated, timeout=500)

    qtbot.wait(200)
    messages = qgis_iface.messageBar().get_messages(Qgis.MessageLevel.Warning)

    assert not success
    assert task_runner.fail
    if messages:
        assert (
            "Task SimpleTask was not successful:"
            "Task was cancelled by user or some dependency tasks failed" in messages
        )


def test_run_simple_task_canceled_after_a_while(
    task_runner: TestTaskRunner, qgis_iface
):
    task = SimpleTask()
    success = task_runner.run_task(task, cancel=True, sleep_before_cancel=0.01)
    messages = qgis_iface.messageBar().get_messages(Qgis.MessageLevel.Critical)

    assert not success
    assert task_runner.fail
    assert isinstance(task.exception, TaskInterruptedException)
    assert "Task canceled!:" in messages


def test_run_simple_task_failed(task_runner: TestTaskRunner, qgis_iface):
    task = SimpleTask(True)
    success = task_runner.run_task(task)
    messages = qgis_iface.messageBar().get_messages(Qgis.MessageLevel.Critical)

    assert not success
    assert task_runner.fail
    assert "Unhandled exception occurred:custom failure" in messages


def test_run_simple_task_failed_with_qgs_plugin_exception(
    task_runner: TestTaskRunner, qgis_iface
):
    task = SimpleTask(True, QgsPluginException)
    success = task_runner.run_task(task)
    messages = qgis_iface.messageBar().get_messages(Qgis.MessageLevel.Critical)

    assert not success
    assert task_runner.fail
    assert "custom failure:" in messages


def test_function_task_without_params(task_runner: TestTaskRunner):
    task = FunctionTask(fn)
    success = task_runner.run_task(task)

    assert success
    assert task.result == ((), {})


def test_function_task_with_params(task_runner: TestTaskRunner):
    task = FunctionTask(lambda: fn(1, 2, a=1, b=2))
    success = task_runner.run_task(task)

    assert success
    assert task.result == ((1, 2), {"a": 1, "b": 2})
