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

from sublime import find_resources
from sublime import active_window


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
        if self.view:
            self.view.set_scratch(True)
            self.view.close()

    def fixturePath(self, *path) -> str:
        return fixtures_path(*path)

    def fixture(self, text) -> None:
        self.view.run_command('phpunit_test_setup_fixture', {'text': text})

    def assertMockNotCalled(self, mock_obj) -> None:
        # https://docs.python.org/3/library/unittest.mock.html
        # Polyfill for a new mock method added in version 3.5.
        if sys.version_info >= (3, 5):  # pragma: no cover
            mock_obj.assert_not_called()
        else:
            self.assertEqual(mock_obj.call_count, 0)
