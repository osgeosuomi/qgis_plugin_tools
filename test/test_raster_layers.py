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



import pytest
from qgis.core import QgsDateTimeRange, QgsRasterLayer, QgsSingleBandGrayRenderer
from qgis.PyQt.QtCore import QDate, QDateTime, Qt, QTime

from ..testing.utilities import qgis_supports_temporal
from ..tools.network import download_to_file
from ..tools.raster_layers import (
    set_band_based_on_range,
    set_fixed_temporal_range,
    set_raster_renderer_to_singleband,
)


@pytest.fixture
def netcdf_layer(tmpdir) -> QgsRasterLayer:
    path = download_to_file(
        "https://raw.githubusercontent.com/GispoCoding/FMI2QGIS/master/FMI2QGIS/test/data/aq_small.nc",
        tmpdir,
    )
    return QgsRasterLayer(str(path))


@pytest.fixture
def t_range() -> QgsDateTimeRange:
    return QgsDateTimeRange(
        QDateTime(QDate(2020, 11, 2), QTime(15, 0, 0, 0)),
        QDateTime(QDate(2020, 11, 3), QTime(11, 0, 0, 0)),
    )


@pytest.fixture
def configured_layer(netcdf_layer, t_range) -> QgsRasterLayer:
    set_raster_renderer_to_singleband(netcdf_layer)
    set_fixed_temporal_range(netcdf_layer, t_range)
    return netcdf_layer


def test_set_raster_renderer_to_singleband(netcdf_layer):
    set_raster_renderer_to_singleband(netcdf_layer)
    assert isinstance(netcdf_layer.renderer(), QgsSingleBandGrayRenderer)


@pytest.mark.skipif(
    not qgis_supports_temporal(), reason="QGIS version does not support temporal utils"
)
def test_set_fixed_temporal_range(netcdf_layer, t_range):
    set_fixed_temporal_range(netcdf_layer, t_range)
    tprops = netcdf_layer.temporalProperties()
    assert tprops.isActive()
    assert tprops.fixedTemporalRange() == QgsDateTimeRange(
        QDateTime(QDate(2020, 11, 2), QTime(15, 0), Qt.TimeSpec(1)),
        QDateTime(QDate(2020, 11, 3), QTime(11, 0), Qt.TimeSpec(1)),
    )


@pytest.mark.skipif(
    not qgis_supports_temporal(), reason="QGIS version does not support temporal utils"
)
def test_set_band_based_on_range(configured_layer):
    t_range2 = QgsDateTimeRange(
        QDateTime(QDate(2020, 11, 2), QTime(15, 0)),
        QDateTime(QDate(2020, 11, 2), QTime(16, 0)),
    )
    band_number = set_band_based_on_range(configured_layer, t_range2)
    assert band_number == 1


@pytest.mark.skipif(
    not qgis_supports_temporal(), reason="QGIS version does not support temporal utils"
)
def test_set_band_based_on_range2(configured_layer):
    t_range2 = QgsDateTimeRange(
        QDateTime(QDate(2020, 11, 2), QTime(17, 0)),
        QDateTime(QDate(2020, 11, 2), QTime(18, 0)),
    )
    band_number = set_band_based_on_range(configured_layer, t_range2)
    assert band_number == 3


@pytest.mark.skipif(
    not qgis_supports_temporal(), reason="QGIS version does not support temporal utils"
)
def test_set_band_based_on_range3(configured_layer):
    t_range2 = QgsDateTimeRange(
        QDateTime(QDate(2020, 11, 2), QTime(18, 0)),
        QDateTime(QDate(2020, 11, 2), QTime(22, 0)),
    )
    band_number = set_band_based_on_range(configured_layer, t_range2)
    assert band_number == 4


@pytest.mark.skipif(
    not qgis_supports_temporal(), reason="QGIS version does not support temporal utils"
)
def test_set_band_based_on_range4(configured_layer):
    t_range2 = QgsDateTimeRange(
        QDateTime(QDate(2020, 11, 3), QTime(10, 0), Qt.TimeSpec(1)),
        QDateTime(QDate(2020, 11, 3), QTime(11, 0), Qt.TimeSpec(1)),
    )
    band_number = set_band_based_on_range(configured_layer, t_range2)
    assert band_number == 20
