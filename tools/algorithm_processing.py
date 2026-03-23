"""Base class algorithm."""

from os.path import isfile

from qgis.core import QgsProcessingAlgorithm
from qgis.PyQt.QtGui import QIcon

from .resources import resources_path

__copyright__ = "Copyright 2020, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"
__revision__ = "$Format:%H$"


class BaseProcessingAlgorithm(QgsProcessingAlgorithm):
    def __init__(self):
        super().__init__()

    def createInstance(self):
        return type(self)()

    def flags(self):
        return super().flags() | QgsProcessingAlgorithm.Flag.FlagHideFromModeler

    def icon(self):
        icon = resources_path("icons", "icon.png")
        if isfile(icon):
            return QIcon(icon)
        else:
            return super().icon()

    def shortHelpString(self):
        raise NotImplementedError
