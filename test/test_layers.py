__copyright__ = "Copyright 2020-2021, Gispo Ltd"
__license__ = "GPL version 3"
__email__ = "info@gispo.fi"
__revision__ = "$Format:%H$"

from qgis.core import QgsWkbTypes

from ..tools.layers import LayerType


def test_layer_type():
    assert LayerType.from_wkb_type(QgsWkbTypes.Type.CurvePolygonZM) == LayerType.Polygon
    assert LayerType.from_wkb_type(QgsWkbTypes.Type.MultiPoint) == LayerType.Point
    assert (
        LayerType.from_wkb_type(QgsWkbTypes.Type.MultiLineString25D) == LayerType.Line
    )
