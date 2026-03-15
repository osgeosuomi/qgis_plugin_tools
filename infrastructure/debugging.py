# ruff: noqa E501
__copyright__ = "Copyright 2020-2021 Gispo Ltd, 2026 qgis_plugin_tools contributors"
__license__ = "GPL version 3"
__email__ = "info@gispo.fi"
__revision__ = "$Format:%H$"

import os
import shutil
import sys

import warnings

warnings.warn(
    "This module will be deprecated in the future."
    "Use qgis-plugin-dev-tools (https://github.com/nlsfi/qgis-plugin-dev-tools) "
    "to configure debugging.",
    DeprecationWarning,
    2,
)


def _check_if_should_setup() -> bool:
    """Check whether to connect to debug server or not"""
    return "pytest" not in sys.modules and not os.environ.get("QGIS_PLUGIN_IN_CI")


def setup_pydevd(host: str = "localhost", port: int = 5678) -> bool:
    """
    Setup pydevd debugging service

    Here is a sample (GlobeBuilder) Intellij Idea / PyCharm configuration for setting up the debug server in workspace.xml:

    <configuration name="Debug Server" type="PyRemoteDebugConfigurationType" factoryName="Python Remote Debug">
      <module name="QGIS Debug Server" />
      <option name="PORT" value="5678" />
      <option name="HOST" value="localhost" />
      <PathMappingSettings>
        <option name="pathMappings">
          <list>
            <mapping local-root="$PROJECT_DIR$/<plugin_name>" remote-root="/home/user/.local/share/QGIS/QGIS3/profiles/default/python/plugins/<plugin_name>" />
          </list>
        </option>
      </PathMappingSettings>
      <option name="REDIRECT_OUTPUT" value="true" />
      <option name="SUSPEND_AFTER_CONNECT" value="true" />
      <method v="2" />
    </configuration>

    :param host: host of the debug server
    :param port: port of the debug server
    :return: Whether debugger was initialized properly or not
    """
    succeeded = False
    if _check_if_should_setup():
        try:
            import pydevd

            pydevd.settrace(host, port=port, stdoutToServer=True, stderrToServer=True)
            succeeded = True
        except Exception as e:
            print(f"Unable to create pydevd debugger: {e}")

    return succeeded


def setup_ptvsd(host: str = "localhost", port: int = 5678) -> bool:
    """
    Setup ptvsd degugging service

    Here is a sample VSCode configuration for connecting to the debug server in launch.json:

    {
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Remote Attach",
            "type": "python",
            "request": "attach",
            "connect": {
                "host": "localhost",
                "port": 5678
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}/<plugin_name>",
                    "remoteRoot": "/Users/<user_name>/Library/Application Support/QGIS/QGIS3/profiles/edplanning/python/plugins/<plugin_name>"
                }
            ]
        }
      ]
    }

    :param host: host of the debug server
    :param port: port of the debug server
    :return: Whether debugger was initialized properly or not
    """
    succeeded = False
    if _check_if_should_setup():
        try:
            import ptvsd

            ptvsd.enable_attach((host, port))
            succeeded = True
        except Exception as e:
            print(f"Unable to create ptvsd debugger: {e}")
    return succeeded


def setup_debugpy(host: str = "localhost", port: int = 5678) -> bool:
    """
    Setup debugpy debugging service

    Here is a sample VSCode configuration for connecting to the debug server in launch.json:

    {
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Remote Attach",
            "type": "python",
            "request": "attach",
            "connect": {
                "host": "localhost",
                "port": 5678
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}/<plugin_name>",
                    "remoteRoot": "/Users/<user_name>/Library/Application Support/QGIS/QGIS3/profiles/edplanning/python/plugins/<plugin_name>"
                }
            ]
        }
      ]
    }

    :param host: host of the debug server
    :param port: port of the debug server
    :return: Whether debugger was initialized properly or not
    """
    succeeded = False
    if _check_if_should_setup() and not os.environ.get("QGIS_DEBUGPY_HAS_LOADED"):
        try:
            import debugpy  # noqa: PLC0415, T100

            debugpy.configure(python=shutil.which("python"))
            debugpy.listen((host, port))  # noqa: T100
            succeeded = True
        except Exception as e:
            print(f"Unable to create debugpy debugger: {e}")  # noqa: T201
        else:
            # extra guard for debugpy not to setup it twice
            # (causes debugging session to hang)
            os.environ["QGIS_DEBUGPY_HAS_LOADED"] = "1"

    return succeeded
