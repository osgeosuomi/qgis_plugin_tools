# QGIS Plugin tools
[![PyPI version](https://badge.fury.io/py/qgis_plugin_tools.svg)](https://badge.fury.io/py/qgis_plugin_tools)
[![Downloads](https://img.shields.io/pypi/dm/qgis_plugin_tools.svg)](https://pypistats.org/packages/qgis_plugin_tools)
![CI](https://github.com/osgeosuomi/qgis_plugin_tools/workflows/Tests/badge.svg)
[![Code on Github](https://img.shields.io/badge/Code-GitHub-brightgreen)](https://github.com/osgeosuomi/pytest-qgis)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/badge/uv-managed-blue)](https://github.com/astral-sh/uv)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)



**Warning: The API is not stable yet. Function and files may move between commits.**

As it's a submodule, you can configure your GIT to auto update the submodule commit by running:

`git config --global submodule.recurse true`

The module is helping you with:
* [setting up some logging](docs/usage.md#Logging) (QgsMessageLog, file log, remote logs...)
* [fetching resources](docs/usage.md#Resource-tools) in `resources` or other folders
* [fetching compiled UI file](docs/usage.md#Resource-tools) in `resources/ui` folder
* fetching compiled translation file in `resources/i18n` folder
* removing QRC resources file easily
* translate using the `i18n.tr()` function.
* managing the release process : zip, upload on plugins.qgis.org, tag, GitHub release
* providing some common widgets/code for plugins
* [setting up a debug server](docs/usage.md#Debug-server)

## How to install it

### For a new plugin
This will create needed structure for your plugin

1. Create new plugin using [cookiecutter-qgis-plugin](https://github.com/osgeosuomi/cookiecutter-qgis-plugin).
   This will automatically initialize git and add qgis_plugin_tools as a submodule for the plugin.
1. Next set up the [development environment](https://github.com/osgeosuomi/cookiecutter-qgis-plugin/blob/main/%7B%7Bcookiecutter.project_directory%7D%7D/docs/development.md#setting-up-development-environment),
   edit metadata.txt with description etc. and commit changes.

### For existing plugin
1. Go to the root folder of your plugin code source
1. `git submodule add https://github.com/osgeosuomi/qgis_plugin_tools.git`
1. To get most out of the submodule, try to refactor the plugin to use the default [plugin tree](#Plugin-tree-example)

### As external dependency
This project can also be used as an external dependency. It can be installed via pip:
```shell
pip install qgis_plugin_tools
```

The project can also be installed in editable mode, but you must use setuptool's strict mode
because of the submodule nature of the project:
```
pip install -e /path/to/qgis_plugin_tools --use-pep517 --config-settings editable_mode=strict
```

### Setting up development environment

This project uses [uv](https://docs.astral.sh/uv/getting-started/installation/)
to manage python packages. Make sure to have it installed first.

- Create a venv that is aware of system QGIS libraries: `uv venv --system-site-packages`
    - On Windows, maybe use a tool like [qgis-venv-creator](ttps://github.com/GispoCoding/qgis-venv-creator).

```shell
# Activate the virtual environment
$ source .venv/bin/activate
# Install dependencies
$ uv sync
# Install pre-commit hooks
$ pre-commit install
```
#### Updating dependencies

`uv lock --upgrade`

## How to use it

Refer to [usage](docs/usage.md) documentation.


## Plugin tree example

The plugin should follow the following file tree to get most out of this module.

Plugin `Foo` root folder:
* `plugin_repo` # **no '-' character!**
    * **`.gitmodules`**
    * `.pre-commit-config.yaml`
    * `.gitattributes`
    * `.gitignore`
    * `.qgis-plugin-ci` # to use [qgis-plugin-ci](https://github.com/opengisch/qgis-plugin-ci)
    * `pluginname` # **no '-' character!**
        * `.gitignore`
      * `qgis_plugins_tools/` # submodule
      * **`resources/`**
        * `i18n/` # Alternatively translations could use [Transifex](infrastructure/template/root/docs/development.md#Translating)
          * `fi.ts`
          * `fi.qm`
        * `ui/`
          * `main_dialog.ui`
        * `icons/`
          * `my_icon.svg`
      * `__init__.py`
      * `foo.py`
      * `metadata.txt`
      * `build.py`
    * `test/`
