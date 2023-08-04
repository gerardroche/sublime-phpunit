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

from PHPUnitKit.lib.utils import get_phpunit_executable


class TestGetPHPUnitExecutable(unittest.ViewTestCase):

    @unittest.mock.patch('shutil.which')
    @unittest.mock.patch('PHPUnitKit.lib.utils.platform')
    def test_composer_linux_executable(self, platform, shutil_which):
        platform.return_value = 'linux'
        expected = unittest.fixtures_path(os.path.join('get_phpunit_executable', 'vendor', 'bin', 'phpunit'))
        actual = get_phpunit_executable(self.view, unittest.fixtures_path('get_phpunit_executable'))

        self.assertEqual([expected], actual)
        self.assertEqual(shutil_which.call_count, 0)

    @unittest.mock.patch('shutil.which')
    @unittest.mock.patch('PHPUnitKit.lib.utils.platform')
    def test_composer_windows_executable(self, platform, shutil_which):
        platform.return_value = 'windows'
        expected = unittest.fixtures_path(os.path.join('get_phpunit_executable', 'vendor', 'bin', 'phpunit.bat'))
        actual = get_phpunit_executable(self.view, unittest.fixtures_path('get_phpunit_executable'))

        self.assertEqual([expected], actual)
        self.assertEqual(shutil_which.call_count, 0)

    @unittest.mock.patch('shutil.which')
    def test_system_path_executable(self, shutil_which):
        shutil_which.return_value = 'shutil_which_executable'
        actual = get_phpunit_executable(self.view, unittest.fixtures_path('foobar'))

        self.assertEqual(['shutil_which_executable'], actual)
        self.assertEqual(shutil_which.call_count, 1)

    @unittest.mock.patch('shutil.which')
    def test_raises_exeption_when_no_executable(self, shutil_which):
        shutil_which.return_value = None
        with self.assertRaisesRegex(ValueError, 'phpunit not found'):
            get_phpunit_executable(self.view, unittest.fixtures_path('foobar'))

        self.assertEqual(shutil_which.call_count, 1)

    @unittest.mock.patch('shutil.which')
    def test_disable_composer_executable_discovery(self, shutil_which):
        self.view.settings().set('phpunit.composer', False)
        get_phpunit_executable(self.view, unittest.fixtures_path('get_phpunit_executable'))

        self.assertEqual(shutil_which.call_count, 1)

    @unittest.mock.patch('shutil.which')
    def test_enable_composer_executable_discovery(self, shutil_which):
        self.view.settings().set('phpunit.composer', True)
        get_phpunit_executable(self.view, unittest.fixtures_path('get_phpunit_executable'))

        self.assertEqual(shutil_which.call_count, 0)

    def test_get_user_phpunit_executable(self):
        self.view.settings().set('phpunit.executable', 'fizz')
        self.assertEqual(['fizz'], get_phpunit_executable(self.view, working_dir='foo'))

    @unittest.skipIf(sublime.platform() == 'windows', 'Test is flaky on Windows')
    def test_get_user_phpunit_executable_is_filtered(self):
        home = os.path.expanduser('~')
        self.view.settings().set('phpunit.executable', '~')
        self.assertEqual([home], get_phpunit_executable(self.view, working_dir='foo'))
        self.view.settings().set('phpunit.executable', '$HOME')
        self.assertEqual([home], get_phpunit_executable(self.view, working_dir='foo'))

    def test_get_user_phpunit_executable_allows_executable_as_list(self):
        self.view.settings().set('phpunit.executable', ['fizz', 'buzz'])
        self.assertEqual(['fizz', 'buzz'], get_phpunit_executable(self.view, working_dir='foo'))

    @unittest.skipIf(sublime.platform() == 'windows', 'Test is flaky on Windows')
    def test_get_user_phpunit_executable_as_list_is_filtered(self):
        home = os.path.expanduser('~')
        self.view.settings().set('phpunit.executable', ['~'])
        self.assertEqual([home], get_phpunit_executable(self.view, working_dir='foo'))
        self.view.settings().set('phpunit.executable', ['~', '~'])
        self.assertEqual([home, home], get_phpunit_executable(self.view, working_dir='foo'))  # noqa: E501
        self.view.settings().set('phpunit.executable', ['$HOME'])
        self.assertEqual([home], get_phpunit_executable(self.view, working_dir='foo'))
        self.view.settings().set('phpunit.executable', ['$HOME', '$HOME'])
        self.assertEqual([home, home], get_phpunit_executable(self.view, working_dir='foo'))  # noqa: E501

    @unittest.mock.patch('shutil.which')
    @unittest.mock.patch('PHPUnitKit.lib.utils.platform')
    def test_enable_pest(self, platform, shutil_which):
        platform.return_value = 'linux'
        self.view.settings().set('phpunit.pest', True)
        working_dir = unittest.fixtures_path('get_phpunit_executable')
        self.assertEqual(
            [unittest.fixtures_path(os.path.join(working_dir, 'vendor', 'bin', 'pest'))],
            get_phpunit_executable(self.view, working_dir))
        self.assertEqual(shutil_which.call_count, 0)

    @unittest.mock.patch('shutil.which')
    @unittest.mock.patch('PHPUnitKit.lib.utils.platform')
    def test_enable_pest_windows(self, platform, shutil_which):
        platform.return_value = 'windows'
        self.view.settings().set('phpunit.pest', True)
        working_dir = unittest.fixtures_path('get_phpunit_executable')
        self.assertEqual(
            [unittest.fixtures_path(os.path.join(working_dir, 'vendor', 'bin', 'pest.bat'))],
            get_phpunit_executable(self.view, working_dir))
        self.assertEqual(shutil_which.call_count, 0)

    @unittest.mock.patch('shutil.which')
    @unittest.mock.patch('PHPUnitKit.lib.utils.platform')
    def test_enable_artisan(self, platform, shutil_which):
        platform.return_value = 'linux'
        self.view.settings().set('phpunit.artisan', True)
        working_dir = unittest.fixtures_path('get_phpunit_executable')
        self.assertEqual(
            [unittest.fixtures_path(os.path.join(working_dir, 'artisan')), 'test'],
            get_phpunit_executable(self.view, working_dir))
        self.assertEqual(shutil_which.call_count, 0)

    @unittest.mock.patch('shutil.which')
    @unittest.mock.patch('PHPUnitKit.lib.utils.platform')
    def test_enable_artisan_on_windows_platform(self, platform, shutil_which):
        platform.return_value = 'windows'
        self.view.settings().set('phpunit.artisan', True)
        working_dir = unittest.fixtures_path('get_phpunit_executable')
        self.assertEqual(
            [unittest.fixtures_path(os.path.join(working_dir, 'artisan.bat')), 'test'],
            get_phpunit_executable(self.view, working_dir))
        self.assertEqual(shutil_which.call_count, 0)

    @unittest.mock.patch('shutil.which')
    @unittest.mock.patch('PHPUnitKit.lib.utils.platform')
    def test_enable_artisan_if_exists(self, platform, shutil_which):
        platform.return_value = 'linux'
        working_dir = unittest.fixtures_path('get_phpunit_executable_only')
        expected = [unittest.fixtures_path(os.path.join(working_dir, 'vendor', 'bin', 'phpunit'))]
        self.view.settings().set('phpunit.pest', True)
        self.assertEqual(expected, get_phpunit_executable(self.view, working_dir))
        self.view.settings().set('phpunit.artisan', True)
        self.assertEqual(expected, get_phpunit_executable(self.view, working_dir))
        self.view.settings().set('phpunit.paratest', True)
        self.assertEqual(expected, get_phpunit_executable(self.view, working_dir))
        self.assertEqual(shutil_which.call_count, 0)

    @unittest.mock.patch('shutil.which')
    @unittest.mock.patch('PHPUnitKit.lib.utils.platform')
    def test_enable_artisan_if_exists_on_windows_platform(self, platform, shutil_which):
        platform.return_value = 'windows'
        working_dir = unittest.fixtures_path('get_phpunit_executable_only')
        expected = [unittest.fixtures_path(os.path.join(working_dir, 'vendor', 'bin', 'phpunit.bat'))]
        self.view.settings().set('phpunit.pest', True)
        self.assertEqual(expected, get_phpunit_executable(self.view, working_dir))
        self.view.settings().set('phpunit.artisan', True)
        self.assertEqual(expected, get_phpunit_executable(self.view, working_dir))
        self.view.settings().set('phpunit.paratest', True)
        self.assertEqual(expected, get_phpunit_executable(self.view, working_dir))
        self.assertEqual(shutil_which.call_count, 0)

    @unittest.mock.patch('shutil.which')
    @unittest.mock.patch('PHPUnitKit.lib.utils.platform')
    def test_enable_paratest(self, platform, shutil_which):
        platform.return_value = 'linux'
        working_dir = unittest.fixtures_path('get_phpunit_executable')
        self.view.settings().set('phpunit.paratest', True)
        self.assertEqual([unittest.fixtures_path(os.path.join(working_dir, 'vendor', 'bin', 'paratest'))],
                         get_phpunit_executable(self.view, working_dir))
        self.assertEqual(shutil_which.call_count, 0)

    @unittest.mock.patch('shutil.which')
    @unittest.mock.patch('PHPUnitKit.lib.utils.platform')
    def test_enable_paratest_on_windows_platform(self, platform, shutil_which):
        platform.return_value = 'windows'
        working_dir = unittest.fixtures_path('get_phpunit_executable')
        self.view.settings().set('phpunit.paratest', True)
        self.assertEqual([unittest.fixtures_path(os.path.join(working_dir, 'vendor', 'bin', 'paratest.bat'))],
                         get_phpunit_executable(self.view, working_dir))
        self.assertEqual(shutil_which.call_count, 0)
