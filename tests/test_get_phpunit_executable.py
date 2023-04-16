import os

import sublime

from PHPUnitKit.plugin import _get_phpunit_executable
from PHPUnitKit.tests import unittest


class TestGetPHPUnitExecutable(unittest.ViewTestCase):

    @unittest.mock.patch('shutil.which')
    @unittest.mock.patch('PHPUnitKit.plugin.platform')
    def test_composer_linux_executable(self, platform, shutil_which):
        platform.return_value = 'linux'
        expected = unittest.fixtures_path(os.path.join('get_phpunit_executable', 'vendor', 'bin', 'phpunit'))
        actual = _get_phpunit_executable(self.view, unittest.fixtures_path('get_phpunit_executable'))

        self.assertEqual([expected], actual)
        self.assertEqual(shutil_which.call_count, 0)

    @unittest.mock.patch('shutil.which')
    @unittest.mock.patch('PHPUnitKit.plugin.platform')
    def test_composer_windows_executable(self, platform, shutil_which):
        platform.return_value = 'windows'
        expected = unittest.fixtures_path(os.path.join('get_phpunit_executable', 'vendor', 'bin', 'phpunit.bat'))
        actual = _get_phpunit_executable(self.view, unittest.fixtures_path('get_phpunit_executable'))

        self.assertEqual([expected], actual)
        self.assertEqual(shutil_which.call_count, 0)

    @unittest.mock.patch('shutil.which')
    def test_system_path_executable(self, shutil_which):
        shutil_which.return_value = 'shutil_which_executable'
        actual = _get_phpunit_executable(self.view, unittest.fixtures_path('foobar'))

        self.assertEqual(['shutil_which_executable'], actual)
        self.assertEqual(shutil_which.call_count, 1)

    @unittest.mock.patch('shutil.which')
    def test_raises_exeption_when_no_executable(self, shutil_which):
        shutil_which.return_value = None
        with self.assertRaisesRegex(ValueError, 'phpunit not found'):
            _get_phpunit_executable(self.view, unittest.fixtures_path('foobar'))

        self.assertEqual(shutil_which.call_count, 1)

    @unittest.mock.patch('shutil.which')
    def test_disable_composer_executable_discovery(self, shutil_which):
        self.view.settings().set('phpunit.composer', False)
        _get_phpunit_executable(self.view, unittest.fixtures_path('get_phpunit_executable'))

        self.assertEqual(shutil_which.call_count, 1)

    @unittest.mock.patch('shutil.which')
    def test_enable_composer_executable_discovery(self, shutil_which):
        self.view.settings().set('phpunit.composer', True)
        _get_phpunit_executable(self.view, unittest.fixtures_path('get_phpunit_executable'))

        self.assertEqual(shutil_which.call_count, 0)

    def test_get_user_phpunit_executable(self):
        self.view.settings().set('phpunit.executable', 'fizz')
        self.assertEqual(['fizz'], _get_phpunit_executable(self.view, working_dir='foo'))

    @unittest.skipIf(sublime.platform() == 'windows', 'Test is flaky on Windows')
    def test_get_user_phpunit_executable_is_filtered(self):
        home = os.path.expanduser('~')
        self.view.settings().set('phpunit.executable', '~')
        self.assertEqual([home], _get_phpunit_executable(self.view, working_dir='foo'))
        self.view.settings().set('phpunit.executable', '$HOME')
        self.assertEqual([home], _get_phpunit_executable(self.view, working_dir='foo'))

    def test_get_user_phpunit_executable_allows_executable_as_list(self):
        self.view.settings().set('phpunit.executable', ['fizz', 'buzz'])
        self.assertEqual(['fizz', 'buzz'], _get_phpunit_executable(self.view, working_dir='foo'))

    @unittest.skipIf(sublime.platform() == 'windows', 'Test is flaky on Windows')
    def test_get_user_phpunit_executable_as_list_is_filtered(self):
        home = os.path.expanduser('~')
        self.view.settings().set('phpunit.executable', ['~'])
        self.assertEqual([home], _get_phpunit_executable(self.view, working_dir='foo'))
        self.view.settings().set('phpunit.executable', ['~', '~'])
        self.assertEqual([home, home], _get_phpunit_executable(self.view, working_dir='foo'))  # noqa: E501
        self.view.settings().set('phpunit.executable', ['$HOME'])
        self.assertEqual([home], _get_phpunit_executable(self.view, working_dir='foo'))
        self.view.settings().set('phpunit.executable', ['$HOME', '$HOME'])
        self.assertEqual([home, home], _get_phpunit_executable(self.view, working_dir='foo'))  # noqa: E501

    @unittest.mock.patch('shutil.which')
    @unittest.mock.patch('PHPUnitKit.plugin.platform')
    def test_enable_pest(self, platform, shutil_which):
        platform.return_value = 'linux'
        self.view.settings().set('phpunit.pest', True)
        working_dir = unittest.fixtures_path('get_phpunit_executable')
        self.assertEqual(
            [unittest.fixtures_path(os.path.join(working_dir, 'vendor', 'bin', 'pest'))],
            _get_phpunit_executable(self.view, working_dir))
        self.assertEqual(shutil_which.call_count, 0)

    @unittest.mock.patch('shutil.which')
    @unittest.mock.patch('PHPUnitKit.plugin.platform')
    def test_enable_pest_windows(self, platform, shutil_which):
        platform.return_value = 'windows'
        self.view.settings().set('phpunit.pest', True)
        working_dir = unittest.fixtures_path('get_phpunit_executable')
        self.assertEqual(
            [unittest.fixtures_path(os.path.join(working_dir, 'vendor', 'bin', 'pest.bat'))],
            _get_phpunit_executable(self.view, working_dir))
        self.assertEqual(shutil_which.call_count, 0)

    @unittest.mock.patch('shutil.which')
    @unittest.mock.patch('PHPUnitKit.plugin.platform')
    def test_enable_artisan(self, platform, shutil_which):
        platform.return_value = 'linux'
        self.view.settings().set('phpunit.artisan', True)
        working_dir = unittest.fixtures_path('get_phpunit_executable')
        self.assertEqual(
            [unittest.fixtures_path(os.path.join(working_dir, 'artisan')), 'test'],
            _get_phpunit_executable(self.view, working_dir))
        self.assertEqual(shutil_which.call_count, 0)

    @unittest.mock.patch('shutil.which')
    @unittest.mock.patch('PHPUnitKit.plugin.platform')
    def test_enable_artisan_on_windows_platform(self, platform, shutil_which):
        platform.return_value = 'windows'
        self.view.settings().set('phpunit.artisan', True)
        working_dir = unittest.fixtures_path('get_phpunit_executable')
        self.assertEqual(
            [unittest.fixtures_path(os.path.join(working_dir, 'artisan.bat')), 'test'],
            _get_phpunit_executable(self.view, working_dir))
        self.assertEqual(shutil_which.call_count, 0)

    @unittest.mock.patch('shutil.which')
    @unittest.mock.patch('PHPUnitKit.plugin.platform')
    def test_enable_artisan_if_exists(self, platform, shutil_which):
        platform.return_value = 'linux'
        working_dir = unittest.fixtures_path('get_phpunit_executable_only')
        expected = [unittest.fixtures_path(os.path.join(working_dir, 'vendor', 'bin', 'phpunit'))]
        self.view.settings().set('phpunit.pest', True)
        self.assertEqual(expected, _get_phpunit_executable(self.view, working_dir))
        self.view.settings().set('phpunit.artisan', True)
        self.assertEqual(expected, _get_phpunit_executable(self.view, working_dir))
        self.view.settings().set('phpunit.paratest', True)
        self.assertEqual(expected, _get_phpunit_executable(self.view, working_dir))
        self.assertEqual(shutil_which.call_count, 0)

    @unittest.mock.patch('shutil.which')
    @unittest.mock.patch('PHPUnitKit.plugin.platform')
    def test_enable_artisan_if_exists_on_windows_platform(self, platform, shutil_which):
        platform.return_value = 'windows'
        working_dir = unittest.fixtures_path('get_phpunit_executable_only')
        expected = [unittest.fixtures_path(os.path.join(working_dir, 'vendor', 'bin', 'phpunit.bat'))]
        self.view.settings().set('phpunit.pest', True)
        self.assertEqual(expected, _get_phpunit_executable(self.view, working_dir))
        self.view.settings().set('phpunit.artisan', True)
        self.assertEqual(expected, _get_phpunit_executable(self.view, working_dir))
        self.view.settings().set('phpunit.paratest', True)
        self.assertEqual(expected, _get_phpunit_executable(self.view, working_dir))
        self.assertEqual(shutil_which.call_count, 0)

    @unittest.mock.patch('shutil.which')
    @unittest.mock.patch('PHPUnitKit.plugin.platform')
    def test_enable_paratest(self, platform, shutil_which):
        platform.return_value = 'linux'
        working_dir = unittest.fixtures_path('get_phpunit_executable')
        self.view.settings().set('phpunit.paratest', True)
        self.assertEqual([unittest.fixtures_path(os.path.join(working_dir, 'vendor', 'bin', 'paratest'))],
                         _get_phpunit_executable(self.view, working_dir))
        self.assertEqual(shutil_which.call_count, 0)

    @unittest.mock.patch('shutil.which')
    @unittest.mock.patch('PHPUnitKit.plugin.platform')
    def test_enable_paratest_on_windows_platform(self, platform, shutil_which):
        platform.return_value = 'windows'
        working_dir = unittest.fixtures_path('get_phpunit_executable')
        self.view.settings().set('phpunit.paratest', True)
        self.assertEqual([unittest.fixtures_path(os.path.join(working_dir, 'vendor', 'bin', 'paratest.bat'))],
                         _get_phpunit_executable(self.view, working_dir))
        self.assertEqual(shutil_which.call_count, 0)
