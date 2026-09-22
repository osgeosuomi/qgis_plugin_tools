# QGIS Plugin tools

[![PyPI version](https://badge.fury.io/py/qgis_plugin_tools.svg)](https://badge.fury.io/py/qgis_plugin_tools)
[![Downloads](https://img.shields.io/pypi/dm/qgis_plugin_tools.svg)](https://pypistats.org/packages/qgis_plugin_tools)
[![Code on Github](https://img.shields.io/badge/Code-GitHub-brightgreen)](https://github.com/osgeosuomi/pytest-qgis)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/badge/uv-managed-blue)](https://github.com/astral-sh/uv)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

**Warning: The API is not stable yet. Function and files may move between commits.**

The module is helping you with:

* [setting up some logging](docs/usage.md#Logging) (QgsMessageLog, file log, remote logs...)
* [fetching resources](docs/usage.md#Resource-tools) in `resources` or other folders
* [fetching compiled UI file](docs/usage.md#Resource-tools) in `resources/ui` folder
* fetching compiled translation file in `resources/i18n` folder
* removing QRC resources file easily
* translate using the `i18n.tr()` function.
* providing some common widgets/code for plugins

## How to install it

It is recommended to use this library as an external dependency with the help of [qgis-plugin-dev-tools](https://github.com/nlsfi/qgis-plugin-dev-tools).
Or some other tool that can download the library though pip.

The tool can be installed via pip:

```shell
pip install qgis_plugin_tools
```

Remember to add this as a runtime requirement in your pyproject.toml:

```toml
[tool.qgis_plugin_dev_tools]
plugin_package_name = "your_plugin_package_name"
runtime_requires = [
    "qgis_plugin_dev_tools"
]
```

### Setting up development environment

This project uses [uv](https://docs.astral.sh/uv/getting-started/installation/)
to manage python packages. Make sure to have it installed first.

* Create a venv that is aware of system QGIS libraries: `uv venv --system-site-packages`
  * On Windows, maybe use a tool like [qgis-venv-creator](ttps://github.com/GispoCoding/qgis-venv-creator).

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

## Contributing

Contributions are very welcome. Get started by reading OSGeo
Suomi [CONTRIBUTING guidelines](https://github.com/osgeosuomi/.github/blob/main/CONTRIBUTING.md).

## License

qgis_plugin_tools is licensed under the GNU General Public License,
version 2 or (at your option) any later version (`GPL-2.0-or-later`).
See [LICENSE](LICENSE) for the full text of GPLv2. Every source file carries
a license notice.

By contributing to this project you agree that your contributions are
licensed under the same terms.
