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

from threading import Thread
from unittest.mock import MagicMock

from qgis.PyQt.QtCore import QCoreApplication

from ..tools.custom_logging import SimpleMessageBarProxy


def test_message_log_proxies_between_threads():
    mock_msg_bar = MagicMock()
    proxy = SimpleMessageBarProxy(mock_msg_bar)

    def mock_thread():
        proxy.emit_message("title", "text", 1, 2)

    thread = Thread(target=mock_thread)
    thread.start()

    mock_msg_bar.pushMessage.assert_not_called()
    thread.join(5)
    assert not thread.is_alive()

    QCoreApplication.processEvents()
    mock_msg_bar.pushMessage.assert_called_once_with(
        title="title", text="text", level=1, duration=2
    )
