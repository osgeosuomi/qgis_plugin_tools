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
from typing import TypeVar

LOGGER = logging.getLogger(__name__)

T = TypeVar("T")


def require[T](value: T | None, msg: str = "Required value is None") -> T:
    """Check that PyQGIS object is not None, satisfying type checkers."""
    if value is None:
        raise TypeError(msg)
    return value


def require_type[T](value: object, cls: type[T], msg: str | None = None) -> T:
    """Check that PyQGIS object is an instance of cls, satisfying type checkers.

    Useful for narrowing base class return values, e.g. QgsMapLayer to QgsVectorLayer.
    """
    if not isinstance(value, cls):
        raise TypeError(msg or f"Expected {cls.__name__}, got {type(value).__name__}")
    return value
