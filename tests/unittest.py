# Copyright (C) 2023 Gerard Roche
#
# This file is part of PHPUnitKit.
#
# PHPUnitKit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PHPUnitKit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PHPUnitKit.  If not, see <https://www.gnu.org/licenses/>.

import os
import sys

from unittest import TestCase
from unittest import mock  # noqa: F401
from unittest import skipIf  # noqa: F401
import os
import sys

from sublime import Region
from sublime import Window
from sublime import active_window
from sublime import find_resources
from sublime import platform

from unittesting import DeferrableTestCase


def fixtures_path(*path) -> str:
    if path is None:
        return os.path.join(os.path.dirname(__file__), 'fixtures')  # type: ignore[unreachable]

    return os.path.join(os.path.dirname(__file__), 'fixtures', *path)


class ViewTestCase(TestCase):

    def setUp(self) -> None:
        self.view = active_window().new_file()
        self.view.set_syntax_file(find_resources('PHP.sublime-syntax')[0])

    def run_window_command(self, command: str, args=None) -> None:
        self.view.window().run_command(command, args)  # type: ignore[union-attr]

    def tearDown(self) -> None:
        self.closeView()

    def closeView(self) -> None:
        if self.view:
            self.view.set_scratch(True)
            self.view.close()


    def assertMockNotCalled(self, mock_obj) -> None:
        # https://docs.python.org/3/library/unittest.mock.html
        # Polyfill for a new mock method added in version 3.5.
        if sys.version_info >= (3, 5):  # pragma: no cover
            mock_obj.assert_not_called()
        else:
            self.assertEqual(mock_obj.call_count, 0)

    def openView(self, file):
        view = self.view.window().open_file(file)
        self.closeView()
        self.view = view

    def fixturePath(self, *path) -> str:
        return fixtures_path(*path)

    def fixture(self, text):
        self.view.run_command('phpunit_test_setup_fixture', {'text': text})

    def setSelection(self, point_or_points) -> None:
        self.view.sel().clear()
        if isinstance(point_or_points, int):
            self.view.sel().add(point_or_points)
        else:
            for point in point_or_points:
                self.view.sel().add(point)

    def assertExecContentRegex(self, expected_regex: str, msg: str = None) -> None:
        self.assertRegex(self.getExecContent(), expected_regex, msg=msg)

    def assertExecContentEqual(self, expected: str, msg: str = None) -> None:
        self.assertEqual(self.getExecContent(), expected, msg=msg)

    def assertExecContentEmpty(self, msg: str = None) -> None:
        self.assertEqual(self.getExecContent(), '', msg=msg)

    def getExecContent(self) -> str:
        view = self.getExecOutputPanel()

        return view.substr(Region(0, view.size()))

    def getExecOutputPanel(self):
        return active_window().find_output_panel('exec')


class DeferrableViewTestCase(DeferrableTestCase, ViewTestCase):
    pass


class DeferrableExecViewTestCase(DeferrableViewTestCase):

    def setUp(self) -> None:
        self.clearExecOutput()
        super().setUp()
        self.folder = None

    def tearDown(self) -> None:
        active_window().run_command('show_panel', {'panel': 'output.UnitTesting'})
        if self.folder:
            _remove_folder(active_window(), self.folder)
        super().tearDown()

    def clearExecOutput(self) -> None:
        output_view = active_window().find_output_panel('exec')
        if output_view:
            output_view.run_command('phpunit_test_erase')

    def addFolder(self, folder: str) -> None:
        self.folder = folder
        _add_folder(active_window(), folder)

    def openProjectFile(self, *path):
        folder = self.fixturePath('project')
        file = self.fixturePath('project', *path)

        self.addFolder(folder)
        self.openView(file)

    def getLoadTimeout(self) -> int:
        return 60

    def getWaitTimeout(self) -> int:
        if sys.platform.startswith('linux') and platform() == 'linux':
            return 1400
        else:
            return 1400

    def isEnv(self, name: str) -> bool:
        return bool(os.getenv(name))

    def endToEndTestsEnabled(self) -> bool:
        return self.isEnv('SUBLIME_PHPUNIT_END_TO_END_TESTS') or self.view.settings().get('phpunit.end_to_end_tests')


# Copied from Sesame plugin
def _add_folder(window, folder):
    if not isinstance(window, Window):
        raise ValueError('argument #1 is not a valid window')

    if not folder:
        raise ValueError('argument #2 is not a valid folder')

    if not os.path.isdir(folder):
        raise ValueError('argument #2 is not a valid directory')

    project_data = window.project_data()
    if not project_data:
        project_data = {}

    if 'folders' not in project_data:
        project_data['folders'] = []

    # Normalise folder
    # @todo folder should be normalised to be relative paths to project file
    folder = os.path.normpath(folder)
    project_file_name = window.project_file_name()
    if project_file_name:
        project_file_dir = os.path.dirname(project_file_name)
        if project_file_dir == folder:
            folder = '.'

    for f in project_data['folders']:
        if f['path'] and (folder == f['path']):
            # Already exists.
            return False

    folder_struct = {
        'path': folder
    }

    if folder != '.':
        folder_struct['follow_symlinks'] = True

    project_data['folders'].append(folder_struct)

    window.set_project_data(project_data)

    return True


def _remove_folder(window: Window, folder: str) -> None:
    window.run_command('remove_folder', {
        'dirs': [folder]
    })
