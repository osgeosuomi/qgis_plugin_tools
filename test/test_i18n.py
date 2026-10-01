# SPDX-License-Identifier: GPL-2.0-or-later
#
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

from pathlib import Path
from types import ModuleType

from pytest_mock import MockerFixture

from qgis_plugin_tools.tools import i18n
from qgis_plugin_tools.tools.i18n import setup_all_translators, tr


def test_tr_formatting():
    string = tr(
        "These are args {} {} and these are kwargs {foo} {bar}", 1, 2, foo=3, bar=4
    )
    assert string == "These are args 1 2 and these are kwargs 3 4"


def test_setup_all_translators_without_translation_file(mocker: MockerFixture):
    mocker.patch.object(i18n, "setup_translation", return_value=("fi", None))
    install = mocker.patch.object(i18n.QCoreApplication, "installTranslator")

    assert setup_all_translators() == []
    install.assert_not_called()


def test_setup_all_translators_installs_translation_file(
    mocker: MockerFixture, tmp_path: Path
):
    qm_file = str(tmp_path / "fi.qm")
    mocker.patch.object(i18n, "setup_translation", return_value=("fi", qm_file))
    load = mocker.patch.object(i18n.QTranslator, "load")
    install = mocker.patch.object(i18n.QCoreApplication, "installTranslator")

    translators = setup_all_translators()

    assert len(translators) == 1
    load.assert_called_once_with(qm_file)
    install.assert_called_once_with(translators[0])


def test_setup_all_translators_installs_library_translation_files(
    mocker: MockerFixture, tmp_path: Path
):
    library = ModuleType("library")
    library.__file__ = str(tmp_path / "library" / "__init__.py")
    library_folder = str(tmp_path / "library" / "resources" / "i18n")
    setup_translation = mocker.patch.object(
        i18n,
        "setup_translation",
        side_effect=[("fi", "main.qm"), ("fi", f"{library_folder}/fi.qm")],
    )
    load = mocker.patch.object(i18n.QTranslator, "load")
    install = mocker.patch.object(i18n.QCoreApplication, "installTranslator")

    translators = setup_all_translators(library)

    assert len(translators) == 2
    setup_translation.assert_called_with(folder=library_folder)
    assert load.call_args_list == [
        mocker.call("main.qm"),
        mocker.call(f"{library_folder}/fi.qm"),
    ]
    assert install.call_count == 2
