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

from qgis.core import QgsProcessingFeedback

LOGGER = logging.getLogger(__name__)


class LoggerProcessingFeedBack(QgsProcessingFeedback):
    def __init__(self, use_logger=False):
        super().__init__()
        self._last = None
        self.use_logger = use_logger
        self.last_progress_text = None
        self.last_push_info = None
        self.last_command_info = None
        self.last_debug_info = None
        self.last_console_info = None
        self.last_report_error = None

    @property
    def last(self):
        return self._last

    @last.setter
    def last(self, text):
        self._last = text

    def setProgressText(self, text):
        self._last = text
        self.last_progress_text = text
        if self.use_logger:
            LOGGER.info(text)

    def pushInfo(self, text):
        self._last = text
        self.last_push_info = text
        if self.use_logger:
            LOGGER.info(text)

    def pushCommandInfo(self, text):
        self._last = text
        self.last_command_info = text
        if self.use_logger:
            LOGGER.info(text)

    def pushDebugInfo(self, text):
        self._last = text
        self.last_debug_info = text
        if self.use_logger:
            LOGGER.warning(text)

    def pushConsoleInfo(self, text):
        self._last = text
        self.last_console_info = text
        if self.use_logger:
            LOGGER.info(text)

    def reportError(self, text, fatalError=False):
        self._last = text
        self.last_report_error = text
        if self.use_logger:
            LOGGER.exception(text)
