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

import sublime

from PHPUnitKit.tests import unittest

from PHPUnitKit.lib.utils import get_php_executable


class TestGetPHPExecutable(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.versions_path = unittest.fixtures_path(os.path.join('get_php_executable', 'versions'))

    def test_returns_none_when_no_executable_found(self):
        self.view.settings().set('phpunit.php_versions_path', self.versions_path)
        self.assertIsNone(get_php_executable(self.view, unittest.fixtures_path('foobar')))

    def test_can_retrieve_from_setting(self):
        self.view.settings().set('phpunit.php_versions_path', self.versions_path)
        expected = unittest.fixtures_path(os.path.join('get_php_executable', 'php'))
        self.view.settings().set('phpunit.php_executable', expected)
        self.assertEqual(expected, get_php_executable(self.view, unittest.fixtures_path('foobar')))

    def test_setting_not_found_raises_exeption(self):
        self.view.settings().set('phpunit.php_versions_path', self.versions_path)
        executable = unittest.fixtures_path(os.path.join('get_php_executable', 'foobar'))
        self.view.settings().set('phpunit.php_executable', executable)
        with self.assertRaisesRegex(ValueError, 'phpunit\\.php_executable.*is not an executable file'):
            get_php_executable(
                self.view,
                unittest.fixtures_path('foobar')
            )

    @unittest.mock.patch('PHPUnitKit.lib.utils.platform')
    def test_linux_get_from_php_version_file(self, platform):
        platform.return_value = 'linux'
        self.view.settings().set('phpunit.php_versions_path', self.versions_path)
        self.view.settings().set('phpunit.php_executable', unittest.fixtures_path('get_php_executable'))
        expected = unittest.fixtures_path(os.path.join('get_php_executable', 'versions', '7.3.0', 'bin', 'php'))
        actual = get_php_executable(self.view, unittest.fixtures_path('get_php_executable'))
        self.assertEqual(actual, expected)

    @unittest.mock.patch('PHPUnitKit.lib.utils.platform')
    def test_windows_get_from_php_version_file(self, platform):
        platform.return_value = 'windows'
        self.view.settings().set('phpunit.php_versions_path', self.versions_path)
        self.view.settings().set('phpunit.php_executable', unittest.fixtures_path('get_php_executable'))
        expected = unittest.fixtures_path(os.path.join('get_php_executable', 'versions', '7.3.0', 'php.exe'))
        self.assertEqual(expected, get_php_executable(self.view, unittest.fixtures_path('get_php_executable')))

    def test_invalid_version_file_number_raises_exception(self):
        self.view.settings().set('phpunit.php_versions_path', self.versions_path)
        with self.assertRaisesRegex(ValueError, 'not a valid version number'):
            get_php_executable(self.view, unittest.fixtures_path('get_php_executable/invalid'))

    def test_no_versions_path_raises_exception(self):
        self.view.settings().set('phpunit.php_versions_path', None)  # type: ignore[arg-type]
        with self.assertRaisesRegex(ValueError, 'is not set'):
            get_php_executable(self.view, unittest.fixtures_path('get_php_executable'))

    def test_invalid_versions_path_raises_exception(self):
        self.view.settings().set('phpunit.php_versions_path', unittest.fixtures_path('foobar'))
        with self.assertRaisesRegex(ValueError, 'does not exist or is not a valid directory'):
            get_php_executable(self.view, unittest.fixtures_path('get_php_executable'))

    def test_non_executable_raises_exeption(self):
        self.view.settings().set('phpunit.php_versions_path', self.versions_path)
        if sublime.platform() == 'windows':
            actual = get_php_executable(
                self.view,
                unittest.fixtures_path(os.path.join('get_php_executable', 'not_executable')))
            expected = unittest.fixtures_path(os.path.join('get_php_executable', 'versions', '7.2.0', 'php.exe'))
            self.assertEqual(actual, expected)
        else:
            with self.assertRaisesRegex(ValueError, 'is not an executable file'):
                get_php_executable(
                    self.view,
                    unittest.fixtures_path(os.path.join('get_php_executable', 'not_executable')))
