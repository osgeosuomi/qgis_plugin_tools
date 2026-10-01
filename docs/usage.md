# Main usage and examples

## Logging

For setting up the logging (usually in the main plugin file):

```python
# Here is a sample plugin.py file

from qgis_plugin_tools.tools.custom_logging import setup_loggers
import qgis_plugin_tools
import MyPluginPackage  # package where plugin.py lies


class MyPlugin:
    def __init__(self) -> None:
        # Save the teardown function to be able to teardown the loggers later
        self._teardown_loggers = lambda: None
        ...

    def initGui(self) -> None:
        # Setup loggers with the plugin package name passed as the root logger namespace
        self._teardown_loggers = setup_loggers(
            MyPluginPackage.__name__,
            qgis_plugin_tools.__name__,
            message_log_name="My Plugin",
        )
        ...

    def unload(self) -> None:
        # Teardown the loggers in plugin unload, works also when reloading plugin with plugin reloader
        self._teardown_loggers()
        self._teardown_loggers = lambda: None
        ...


# In some cases you might want to add a message bar to a dialog and use logging
# from there, this adds message_bar to dialog and uses it with message bar
# logging handler

from qgis_plugin_tools.tools.custom_logging import add_logger_msg_bar_to_widget

dialog = Dialog()
add_logger_msg_bar_to_widget(dialog)
```

To use the logging system in plugin files:

```python
import logging

LOGGER = logging.getLogger(__name__)

# Later in the code
LOGGER.debug("Log some debug messages")
LOGGER.info("Log some info here")
LOGGER.warning("Log a warning here")
LOGGER.error("Log an error here")
LOGGER.critical("Log a critical error here")

# To show a message bar in addition to logging a message use
# either MsgBar helpers

from qgis_plugin_tools.tools.messages import MsgBar

MsgBar.info("Msg bar message", "some details here")
MsgBar.warning("Msg bar message", "some details here", success=True)

# or "extra" kwarg dict with data, creatable also with bar_msg helper

from qgis_plugin_tools.tools.custom_logging import bar_msg

LOGGER.warning("Msg bar message", extra={"details:": "some details here"})
LOGGER.error("Msg bar message", extra=bar_msg("some details here", duration=10))
```

To change the log level of the plugin you can either edit QGIS3.ini file:

```init
[YourPlugin]
log_level/file=WARNING
log_level/stream=DEBUG
```

or change the log level in runtime:

```python
from qgis_plugin_tools.tools.custom_logging import LogTarget, get_log_level_key
from qgis_plugin_tools.tools.settings import set_setting

set_setting(get_log_level_key(LogTarget.STREAM), "WARNING")
set_setting(get_log_level_key(LogTarget.FILE), "CRITICAL")
```

## Exceptions

Use [`QgsPluginException`][exceptions] as a base class for every exception.
This makes it easy to catch all user thrown exceptions at the same time, and
you can even use the bar messages in exceptions.

```python
from qgis_plugin_tools.tools.exceptions import QgsPluginException
from qgis_plugin_tools.tools.messages import MsgBar
from qgis_plugin_tools.tools.i18n import tr

try:
    # do something that might throw exception
    raise QgsPluginNotImplementedException(
        tr("This is not implemented"), bar_msg(tr("Please implement"))
    )
except QgsPluginException as e:
    # Shows bar message
    MsgBar.exception(str(e), **e.bar_msg)
except Exception as e:
    MsgBar.exception(tr("Unhandled exception occurred"), e)
```

Check [tests][test-decorations] for more examples.

## Network tools

Network tools include blocking network utils using QGIS best practices.
Use this instead of `requests` or `urllib` modules.
Check [tests][test-network] for more examples.

```python
from qgis_plugin_tools.tools.network import fetch

contents = fetch("www.examapleurl.com")
```

## Settings tools

[This module][settings] includes tool to save and load QGIS profile settings
easily. Check [tests][test-settings] for examples.

## Resource tools

[This module][resources] provides easy way to get paths to various files in
plugin directories. For example to fetch ui file from resources/ui folder use
`load_ui('resource-file.ui)`.

## Typing tools

[This module][typing-utils] helps to narrow optional or too generic PyQGIS
return types, raising an exception at runtime if the type is not as expected.

```python
from qgis.core import QgsProject, QgsVectorLayer

from qgis_plugin_tools.utils.typing_utils import require, require_type

project = require(QgsProject.instance())  # QgsProject | None -> QgsProject
layer = require_type(
    project.mapLayer(layer_id), QgsVectorLayer
)  # QgsMapLayer | None -> QgsVectorLayer
```

## Translating

### Using translations in code

It is a good practice to use wrap every meaningful log or message string inside `tr`
to make it possibly translatable.

```python
from qgis.PyQt import QtCore

from qgis_plugin_tools.tools.i18n import setup_all_translators

# For setting up the translation file (usually in root __init__.py)
TRANSLATORS: list[QtCore.QTranslator] = []


def classFactory(_):  # noqa: ANN201, ANN001, N802
    """Class factory."""
    import other_plugin  # noqa: PLC0415

    from your_plugin.plugin import Plugin  # noqa: PLC0415

    # Pass libraries with translations in resources/i18n, if any
    TRANSLATORS.extend(setup_all_translators(other_plugin))

    return Plugin()


# Everywhere else in the plugin
from qgis_plugin_tools.tools.i18n import tr

# Wrap translatable string with tr
tr("This will be translated")
tr("Meaning of life is {}?", 42)
tr("{} + {} is definitely {}", 1, 1, 3)
```

### Setting up translations

To set update and create translation files, refer to the
[qgis-plugin-dev-tools translation quide][qpdt-translations].
For doing the translation and compiling translation files, we recommend using
[Qt Linguist](https://doc.qt.io/qt-6/qtlinguist-index.html).

[exceptions]: https://github.com/osgeosuomi/qgis_plugin_tools/blob/main/src/qgis_plugin_tools/tools/exceptions.py
[settings]: https://github.com/osgeosuomi/qgis_plugin_tools/blob/main/src/qgis_plugin_tools/tools/settings.py
[resources]: https://github.com/osgeosuomi/qgis_plugin_tools/blob/main/src/qgis_plugin_tools/tools/resources.py
[typing-utils]: https://github.com/osgeosuomi/qgis_plugin_tools/blob/main/src/qgis_plugin_tools/utils/typing_utils.py
[test-decorations]: https://github.com/osgeosuomi/qgis_plugin_tools/blob/main/test/test_decorations.py
[test-network]: https://github.com/osgeosuomi/qgis_plugin_tools/blob/main/test/test_network.py
[test-settings]: https://github.com/osgeosuomi/qgis_plugin_tools/blob/main/test/test_setings.py
[qpdt-translations]: https://github.com/nlsfi/qgis-plugin-dev-tools?tab=readme-ov-file#updating-translations
