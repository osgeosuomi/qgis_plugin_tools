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

"""Tools about version."""

from osgeo import osr

from .exceptions import QgsPluginVersionInInvalidFormat
from .resources import metadata_config

EXPECTED_VERSION_LENGTH = 3


def format_version_integer(version_string: str) -> int:
    """Transform version string to integers to allow comparing versions.

    Transform "0.1.2" into "000102"
    Transform "10.9.12" into "100912"
    """
    return int("".join([a.zfill(2) for a in version_string.strip().split(".")]))


def version(remove_v_prefix: bool = True) -> str:
    """Return the version defined in metadata.txt."""
    v = metadata_config()["general"]["version"]
    if v.startswith("v") and remove_v_prefix:
        v = v[1:]
    return v


def proj_version() -> tuple[int, int]:
    """Returns PROJ library version"""
    major: int = osr.GetPROJVersionMajor()
    minor: int = osr.GetPROJVersionMinor()
    return major, minor


def version_from_string(version: str) -> tuple[int, int, int]:
    """
    Transforms version string in format 'x.y.z' to tuple (x,y,z) for comparisons
    :param version:
    :return:
    """
    parts = version.split(".")
    if len(parts) != EXPECTED_VERSION_LENGTH:
        raise QgsPluginVersionInInvalidFormat()
    return int(parts[0]), int(parts[1]), int(parts[2])


def string_from_version(version: tuple[int, int, int]) -> str:
    """
    Transforms version tuple in format (x,y,z) to string in format 'x.y.z'
    :param version:
    :return:
    """
    if len(version) != EXPECTED_VERSION_LENGTH:
        raise QgsPluginVersionInInvalidFormat()
    return ".".join(map(str, version))
