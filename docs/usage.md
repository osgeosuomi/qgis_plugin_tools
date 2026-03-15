# Main usage and examples

## Logging

For setting up the logging (usually in the main plugin file):

```python
# Here is a sample plugin.py file

from qgis_plugin_tools.tools.custom_logging import setup_loggers
import qgis_plugin_tools
import MyPluginPackage # package where plugin.py lies

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
LOGGER.debug('Log some debug messages')
LOGGER.info('Log some info here')
LOGGER.warning('Log a warning here')
LOGGER.error('Log an error here')
LOGGER.critical('Log a critical error here')

# To show a message bar in addition to logging a message use
# either MsgBar helpers

from qgis_plugin_tools.tools.messages import MsgBar

MsgBar.info("Msg bar message", "some details here")
MsgBar.warning('Msg bar message', "some details here", success=True)

# or "extra" kwarg dict with data, creatable also with bar_msg helper

from qgis_plugin_tools.tools.custom_logging import bar_msg

LOGGER.warning('Msg bar message', extra={'details:': "some details here"})
LOGGER.error('Msg bar message', extra=bar_msg("some details here", duration=10))
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

Use [`QgsPluginException`](../tools/exceptions.py) as a base class for every exception. This makes it easy to catch
all user thrown exceptions at the same time, and you can even use the bar messages in exceptions.

```python
from .qgis_plugin_tools.tools.exceptions import QgsPluginException
from .qgis_plugin_tools.tools.messages import MsgBar
from .qgis_plugin_tools.tools.i18n import tr

try:
    # do something that might throw exception
    raise QgsPluginNotImplementedException(tr('This is not implemented'), bar_msg(tr('Please implement')))
except QgsPluginException as e:
    # Shows bar message
    MsgBar.exception(str(e), **e.bar_msg)
except Exception as e:
    MsgBar.exception(tr('Unhandled exception occurred'), e)
```

Check [tests](../testing/test_decorations.py) for more examples.

## Network tools

Network tools include blocking network utils using QGIS best practices.
Use this instead of `requests` or `urllib` modules.
Check [tests](../testing/test_network.py) for more examples.

```python
from .qgis_plugin_tools.tools.network import fetch

contents = fetch('www.examapleurl.com')
```

## Settings tools

[This module](../tools/settings.py) includes tool to save and load QGIS profile settings easily.
Check [tests](../testing/test_settings.py) for examples.

## Resource tools

[This module](../tools/resources.py) provides easy way to get paths to various files in
plugin directories. For example to fetch ui file from resources/ui folder use
`load_ui('resource-file.ui)`.

## Translating

### Using translations in code

It is a good practice to use wrap every meaningful log or message string inside `tr`
to make it possibly translatable.

```python
from qgis.PyQt.QtCore import QCoreApplication, QTranslator

from .qgis_plugin_tools.tools.i18n import setup_translation, tr

# For setting up the translation file (usually in plugin.py __init__)
locale, file_path = setup_translation()
if file_path:
    self.translator = QTranslator()
    self.translator.load(file_path)
    QCoreApplication.installTranslator(self.translator)

# Wrap translatable string with tr
tr('This will be translated')
tr('Meaning of life is {}?', 42)
tr('{} + {} is definitely {}', 1,1,3)
```

### Setting up translations

Check out [translation guide](../infrastructure/template/root/docs/development.md#Translating).

## Debug server

Plugin can connect to already running debug server with following code in the plugin's `__init__.py` file.
Check out comments in [debugging.py](../infrastructure/debugging.py).

```python
from .qgis_plugin_tools.infrastructure.debugging import setup_pydevd, setup_debugpy

# It is a good idea to set up an environment variable to control this. Like:
# if os.environ.get('QGIS_PLUGIN_USE_DEBUGGER') == 'pydevd':
setup_pydevd()
```

## Using PluginMaker

There is a script [plugin_maker.py](infrastructure/plugin_maker.py), which can
be used to replace Makefile and pb_tool in plugin build, deployment, translation and packaging processes.
To use it, create a python script (eg. build.py) in the root of the plugin and
populate it like following:

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob

from qgis_plugin_tools.infrastructure.plugin_maker import PluginMaker

'''
#################################################
# Edit the following to match the plugin
#################################################
'''

locales = ['fi']
profile = 'foo'
py_files = [fil for fil in glob.glob("**/*.py", recursive=True) if "test/" not in fil]
ui_files = list(glob.glob("**/*.ui", recursive=True))
resources = list(glob.glob("**/*.qrc", recursive=True))
extra_dirs = ["resources"]
compiled_resources = ["resources.py"]


PluginMaker(py_files=py_files, ui_files=ui_files, resources=resources, extra_dirs=extra_dirs,
            compiled_resources=compiled_resources, locales=locales, profile=profile)
```

And use it like:

```shell script
python build.py -h # Show available commands
python build.py deploy
python build.py transup
# etc.
```
