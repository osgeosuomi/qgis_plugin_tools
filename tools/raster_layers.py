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


from typing import TYPE_CHECKING

from qgis.core import (
    QgsContrastEnhancement,
    QgsDateTimeRange,
    QgsRasterBandStats,
    QgsRasterDataProvider,
    QgsRasterLayer,
    QgsSingleBandGrayRenderer,
)
from qgis.PyQt.QtCore import Qt

try:
    from qgis.core import QgsRasterLayerTemporalProperties
except ImportError:
    QgsRasterLayerTemporalProperties = None

if TYPE_CHECKING:
    import datetime


def set_raster_renderer_to_singleband(layer: QgsRasterLayer, band: int = 1) -> None:
    """
    Set raster renderer to singleband
    :param layer: raster layer
    :param band: band number starting from 1
    """
    # https://gis.stackexchange.com/a/377631/123927 and
    # https://gis.stackexchange.com/a/157573/123927
    provider: QgsRasterDataProvider = layer.dataProvider()
    renderer: QgsSingleBandGrayRenderer = QgsSingleBandGrayRenderer(
        layer.dataProvider(), band
    )

    stats: QgsRasterBandStats = provider.bandStatistics(
        band, QgsRasterBandStats.Stats.All, layer.extent(), 0
    )
    min_val = max(stats.minimumValue, 0)
    max_val = max(stats.maximumValue, 0)

    enhancement = QgsContrastEnhancement(renderer.dataType(band))
    contrast_enhancement = (
        QgsContrastEnhancement.ContrastEnhancementAlgorithm.StretchToMinimumMaximum
    )
    enhancement.setContrastEnhancementAlgorithm(contrast_enhancement, True)
    enhancement.setMinimumValue(min_val)
    enhancement.setMaximumValue(max_val)
    layer.setRenderer(renderer)
    layer.renderer().setContrastEnhancement(enhancement)
    layer.triggerRepaint()


def set_fixed_temporal_range(layer: QgsRasterLayer, t_range: QgsDateTimeRange) -> None:
    """
    Set fixed temporal range for raster layer
    :param layer: raster layer
    :param t_range: fixed temporal range
    """
    mode = QgsRasterLayerTemporalProperties.TemporalMode.ModeFixedTemporalRange
    tprops: QgsRasterLayerTemporalProperties = layer.temporalProperties()
    tprops.setMode(mode)
    if t_range.begin().timeSpec() == 0 or t_range.end().timeSpec() == 0:
        begin = t_range.begin()
        end = t_range.end()
        begin.setTimeSpec(Qt.TimeSpec(1))
        end.setTimeSpec(Qt.TimeSpec(1))
        t_range = QgsDateTimeRange(begin, end)
    tprops.setFixedTemporalRange(t_range)
    tprops.setIsActive(True)


def set_band_based_on_range(layer: QgsRasterLayer, t_range: QgsDateTimeRange) -> int:
    """
    Set raster layer band based on temporal range
    :param layer: Raster layer
    :param t_range: temporal range
    :return: band number
    """
    band_num = 1
    tprops: QgsRasterLayerTemporalProperties = layer.temporalProperties()
    if (
        (
            tprops.isVisibleInTemporalRange(t_range)
            and t_range.begin().isValid()
            and t_range.end().isValid()
        )
        and tprops.mode()
        == QgsRasterLayerTemporalProperties.TemporalMode.ModeFixedTemporalRange
    ):
        layer_t_range: QgsDateTimeRange = tprops.fixedTemporalRange()
        start: datetime.datetime = layer_t_range.begin().toPyDateTime()
        end: datetime.datetime = layer_t_range.end().toPyDateTime()
        delta = (end - start) / layer.bandCount()
        band_num = int((t_range.begin().toPyDateTime() - start) / delta) + 1
        set_raster_renderer_to_singleband(layer, band_num)
    return band_num
