"""Tools to work with resource files."""
import configparser
import importlib.resources
import inspect
import sys
from os.path import abspath, dirname, exists, join, pardir
from pathlib import Path
from typing import TYPE_CHECKING, Dict, Iterator, NamedTuple, Optional

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog, QWidget

if TYPE_CHECKING:
    import os
    from typing import Union

__copyright__ = (
    "Copyright 2019, 3Liz, 2020-2021 Gispo Ltd, "
    "2022-2023 National Land Survey of Finland"
)
__license__ = "GPL version 3"
__email__ = "info@3liz.org"
__revision__ = "$Format:%H$"

from qgis.core import QgsApplication

PLUGIN_NAME: str = ""
SLUG_NAME: str = ""


def is_submodule() -> bool:
    """Detects if qgis_plugin_tools is used as a submodule

    Checks if the second level package name is qgis_plugin_tools
    The __name__ is:
    - "myplugin.qgis_plugin_tools.tools.resources" when used as a submodule
    - "myplugin.dependencies.qgis_plugin_tools.tools.resources" when used as embedded
      dependency
    - "qgis_plugin_tools.tools.resources" when used as pip installed package
    """

    try:
        _, second_level_package_name, *_ = __name__.split(".")
    except ValueError:
        return False
    return second_level_package_name == "qgis_plugin_tools"


_IS_SUBMODULE_USAGE = is_submodule()


def _plugin_path_submodule() -> str:
    # assume qgis_plugin_tools is inside the plugin package,
    # use the path to the top level module name

    top_level_package_name = __name__.split(".", maxsplit=1)[0]
    module_file = sys.modules[top_level_package_name].__file__

    if module_file is not None:
        path = str(Path(module_file).parent.resolve())
    else:
        # maybe possible to have __file__ as none? fall back to default
        # structure with qgis_plugin_tools directly under plugin package
        path = dirname(dirname(__file__))
        path = abspath(abspath(join(path, pardir)))

    return path


def _iterate_modules(module_name: str) -> Iterator[str]:
    """Iterates modules bottom up

    >>> list(_iterate_modules("plugin.tools.resources"))
    [
        "plugin.tools.resources",
        "plugin.tools",
        "plugin"
    ]
    """

    modules = module_name.split(".")
    for i in range(len(modules), 0, -1):
        yield ".".join(modules[:i])


class IsPluginResult(NamedTuple):
    is_plugin: bool
    plugin_directory: Optional[str] = None

    def __bool__(self) -> bool:
        return self.is_plugin


def _is_module_qgis_plugin(module_name: str) -> IsPluginResult:
    """Checks if the module is a QGIS plugin

    A plugin module has a classFactory method and a metadata.txt at the package root.

    Returns a IsPluginResult thats compares to True when the module given is a plugin.

    >>> if is_plugin := _is_module_qgis_plugin('myplugin'):
    >>>    print(f"Plugin is installed ad {is_plugin.plugin_directory}")
    """

    module = sys.modules.get(module_name)
    if module is None or not inspect.ismodule(module):
        return IsPluginResult(False)

    class_factory_function = getattr(module, "classFactory", None)
    if class_factory_function is None or not inspect.isfunction(class_factory_function):
        return IsPluginResult(False)

    try:
        source_file = inspect.getsourcefile(module)
    except TypeError:
        # TypeError is thrown for built-in modules. We are only interested in
        # custom modules, so it is safe to ignore the error.
        return IsPluginResult(False)
    if not source_file:
        return IsPluginResult(False)

    source_directory = dirname(source_file)
    if not exists(join(source_directory, "metadata.txt")):
        return IsPluginResult(False)

    return IsPluginResult(True, source_directory)


def _plugin_path_dependency() -> str:
    """Get the path to the plugin package folder.

    Traverses packages of calling modules bottom up and checks if it is a qgis plugin.
    """

    for frame_info in inspect.stack():
        caller_module_name: Optional[str] = frame_info.frame.f_globals.get("__name__")
        if caller_module_name is None or "qgis_plugin_tools" in caller_module_name:
            # We are interested only on calls from outside of qgis_plugin_tools
            continue
        for module_name in _iterate_modules(caller_module_name):
            if is_plugin := _is_module_qgis_plugin(module_name):
                assert is_plugin.plugin_directory
                return is_plugin.plugin_directory

    # fall back to default directory tree
    return _plugin_path_submodule()


def plugin_path(*args: str) -> str:
    """Get the path to plugin package folder.

    :param args List of path elements e.g. ['img', 'logos', 'image.png']
    :type args: str

    :return: Absolute path to the resource.
    :rtype: str
    """
    if _IS_SUBMODULE_USAGE:
        path = _plugin_path_submodule()
    else:
        path = _plugin_path_dependency()

    for item in args:
        path = abspath(join(path, item))

    return path


def root_path(*args: str) -> str:
    """Get the path to plugin root folder.

    NOTE: the assumed root is the parent of the plugin package folder.

    :param args List of path elements e.g. ['img', 'logos', 'image.png']
    :type args: str

    :return: Absolute path to the resource.
    :rtype: str
    """
    return plugin_path(pardir, *args)


def profile_path(*args: str) -> str:
    """
    Get the path inside profile folder.
    return: Absolute path to the resource.
    """
    path = QgsApplication.qgisSettingsDirPath()
    for item in args:
        path = abspath(join(path, item))

    return path


def plugin_name() -> str:
    """Return the plugin name according to metadata.txt but stripped of spaces.
    This is because lots of the code assumes plugin_name returns a string without
    spaces.

    :return: The stripped plugin name.
    :rtype: basestring
    """
    global PLUGIN_NAME, _IS_SUBMODULE_USAGE

    if PLUGIN_NAME != "":
        return PLUGIN_NAME

    try:
        metadata = metadata_config()
        name: str = metadata["general"]["name"]
        name = name.replace(" ", "").strip()
    except KeyError:
        name = "test_plugin"

    # if qgis plugin tools is run as a dependency, global var cannot be set
    # since it might confuse multiple plugins in the same env using this fn
    if _IS_SUBMODULE_USAGE:
        PLUGIN_NAME = name

    return name


def plugin_display_name() -> str:
    """Return the plugin name according to metadata.txt, including spaces,
    for displaying to the end user.

    :return: The original plugin name.
    :rtype: basestring
    """
    try:
        metadata = metadata_config()
        return metadata["general"]["name"]
    except KeyError:
        return "Test plugin"


def slug_name() -> str:
    """Return project slug name in .qgis-plugin.ci"""
    global SLUG_NAME, _IS_SUBMODULE_USAGE

    if SLUG_NAME != "":
        return SLUG_NAME

    try:
        metadata = metadata_config()
        name: str = metadata["general"]["repository"]
        slug = name.split("/")[-1]
    except KeyError:
        slug = plugin_name()

    # if qgis plugin tools is run as a dependency, global var cannot be set
    # since it might confuse multiple plugins in the same env using this fn
    if _IS_SUBMODULE_USAGE:
        SLUG_NAME = slug

    return slug


def task_logger_name() -> str:
    """
    Returns the name for task logger
    """
    return f"{plugin_name()}_task"


def metadata_config() -> configparser.ConfigParser:
    """Get the INI config parser for the metadata file.

    :return: The config parser object.
    :rtype: ConfigParser
    """
    path = plugin_path("metadata.txt")
    config = configparser.ConfigParser()
    config.read(path)
    return config


def qgis_plugin_ci_config() -> Optional[Dict]:
    """
    Get configuration of the ci config or None
    """
    path_str = root_path(".qgis-plugin-ci")
    if not Path(path_str).exists():
        path_str = plugin_path(".qgis-plugin-ci")
    path = Path(path_str)
    if path.exists():
        with open(path) as f:
            config = {}
            for line in f:
                parts = line.split(":")
                config[parts[0]] = ":".join(parts[1:])

        return config
    return None


def plugin_test_data_path(*args: str) -> str:
    """Get the path to the plugin test data path.

    :param args List of path elements e.g. ['img', 'logos', 'image.png']
    :type args: str

    :return: Absolute path to the resources folder.
    :rtype: str
    """

    path = abspath(abspath(join(root_path(), "test", "data")))
    if not exists(path):
        path = abspath(abspath(join(plugin_path(), "test", "data")))
    for item in args:
        path = abspath(join(path, item))

    return path


def resources_path(*args: str) -> str:
    """Get the path to our resources folder.

    :param args List of path elements e.g. ['img', 'logos', 'image.png']
    :type args: str

    :return: Absolute path to the resources folder.
    :rtype: str
    """
    path = abspath(abspath(join(plugin_path(), "resources")))
    for item in args:
        path = abspath(join(path, item))

    return path


def qgis_plugin_tools_resources(*args: str) -> str:
    """Get the path within the qgis_plugin_tools submodule"""
    return str(Path(__file__, "..", "..", "resources", *args).resolve().absolute())


def load_ui(*args: str) -> QWidget:
    """Get compiled UI file.

    :param args List of path elements e.g. ['img', 'logos', 'image.png']
    :type args: str

    :return: Compiled UI file.
    """
    ui_file_path = resources_path("ui", *args)
    return load_ui_from_file(ui_file_path)


def load_ui_from_file(ui_file_path: "Union[str, os.PathLike]") -> QWidget:
    ui_class, _ = uic.loadUiType(ui_file_path)
    return ui_class


def ui_file_dialog(*ui_file_name_parts: str):  # noqa ANN201
    """DRY helper for building classes from a .ui file"""

    class UiFileDialogClass(QDialog, load_ui(*ui_file_name_parts)):  # type: ignore
        def __init__(
            self,
            parent: Optional[QWidget],
        ) -> None:
            super().__init__(parent)
            self.setupUi(self)  # provided by load_ui FORM_CLASS

    return UiFileDialogClass


def package_file(package: importlib.resources.Package, file_name: str) -> Path:
    """
    Safely access a file in the package hierarchy. This will
    ensure the requested file actually exists on the file system
    outside the contextmanager, so that the file can be still
    accessed with the path on demand later.

    Use like importlib.resources, provide a package (module or string)
    and file name/path inside the package.

    >>> package_file('myplugin.resources', 'image.svg')
    C:/Users/me/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/myplugin/resources/image.svg

    >>> import myplugin.resources
    >>> package_file(myplugin.resources, 'image.svg')
    C:/Users/me/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/myplugin/resources/image.svg
    """

    with importlib.resources.path(package, file_name) as requested_path:
        if not requested_path.is_file():
            raise FileNotFoundError(
                f"requested file {file_name} not found in {package}"  # noqa: E713
            )

    if not requested_path.is_file():
        raise FileNotFoundError(
            "requested file would be available only as a temporary resource"
        )

    return requested_path
