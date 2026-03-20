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

import importlib.resources
from typing import Any

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget

from .resources import package_file


class CompiledUI:
    # provided by pyuic .ui file compilation
    def setupUi(self, instance: QWidget) -> None:  # noqa: N802
        ...


def load_ui_file(package: importlib.resources.Package, ui_file_name: str) -> Any:
    """
    Use like importlib.resources to load a single ui file from a package to a class:

    ```
    MyUi: Type[QDockWidget] = load_ui_file(my.imported.module, "dock_widget.ui")
    ```

    Type the return as a type of the ui file subclass, and build the class with
    type-ignore on the inheritance. Mypy cannot statically determine the dynamic
    base class without a plugin, but for example Pylance can still provide
    autocomplete for the implementation methods:

    ```
    class MyImplementation(MyUi):  # type: ignore
        def __init__(self):
            super().__init__()  # Pylance will show QDockWidget init signature
    ```
    """
    # TODO: add mypy plugin to support usage without type-ignores?

    ui_file_path = package_file(package, ui_file_name)

    ui_class: type[CompiledUI]
    base_class: type[QWidget]
    ui_class, base_class = uic.loadUiType(str(ui_file_path))

    class UiFileWidget(base_class, ui_class):  # type: ignore
        def __init__(
            self,
            *args: Any,
            **kwargs: dict[str, Any],
        ) -> None:
            super().__init__(*args, **kwargs)
            self.setupUi(self)

    return UiFileWidget
