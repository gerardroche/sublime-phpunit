from PHPUnitKit.plugin import PHPUnit
from PHPUnitKit.tests import unittest

import sublime


class TestGetPHPUnitExecutable(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()

        self.window = sublime.active_window()
        self.phpunit = PHPUnit(self.window)
        self.phpunit.view.settings().erase('phpunit.composer')

    @unittest.mock.patch('shutil.which')
    @unittest.mock.patch('PHPUnitKit.plugin.platform')
    def test_composer_linux_executable(self, platform, shutil):
        platform.return_value = 'linux'
        expected = unittest.fixtures_path('get_phpunit_executable/vendor/bin/phpunit')
        actual = self.phpunit.get_phpunit_executable(unittest.fixtures_path('get_phpunit_executable'))

        self.assertEqual(expected, actual)
        self.assertEqual(shutil.call_count, 0)

    @unittest.mock.patch('shutil.which')
    @unittest.mock.patch('PHPUnitKit.plugin.platform')
    def test_composer_windows_executable(self, platform, shutil):
        platform.return_value = 'windows'
        expected = unittest.fixtures_path('get_phpunit_executable/vendor/bin/phpunit.bat')
        actual = self.phpunit.get_phpunit_executable(unittest.fixtures_path('get_phpunit_executable'))

        self.assertEqual(expected, actual)
        self.assertEqual(shutil.call_count, 0)

    @unittest.mock.patch('shutil.which')
    def test_system_path_executable(self, shutil_which):
        shutil_which.return_value = 'shutil_which_executable'
        actual = self.phpunit.get_phpunit_executable(unittest.fixtures_path('foobar'))

        self.assertEqual('shutil_which_executable', actual)
        self.assertEqual(shutil_which.call_count, 1)

    @unittest.mock.patch('shutil.which')
    def test_raises_exeption_when_no_executable(self, shutil_which):
        shutil_which.return_value = None
        with self.assertRaisesRegex(ValueError, 'phpunit not found'):
            self.phpunit.get_phpunit_executable(unittest.fixtures_path('foobar'))

        self.assertEqual(shutil_which.call_count, 1)

    @unittest.mock.patch('shutil.which')
    def test_disable_composer_executable_discovery(self, shutil_which):
        self.phpunit.view.settings().set('phpunit.composer', False)
        self.phpunit.get_phpunit_executable(unittest.fixtures_path('get_phpunit_executable'))

        self.assertEqual(shutil_which.call_count, 1)

    @unittest.mock.patch('shutil.which')
    def test_enable_composer_executable_discovery(self, shutil_which):
        self.phpunit.view.settings().set('phpunit.composer', True)
        self.phpunit.get_phpunit_executable(unittest.fixtures_path('get_phpunit_executable'))

        self.assertEqual(shutil_which.call_count, 0)
