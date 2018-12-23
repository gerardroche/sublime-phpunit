import os

import sublime

from PHPUnitKit.plugin import _get_php_executable
from PHPUnitKit.tests import unittest


class TestGetPHPExecutable(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.versions_path = unittest.fixtures_path(os.path.join('get_php_executable', 'versions'))

    def test_returns_none_when_no_executable_found(self):
        self.assertIsNone(_get_php_executable(unittest.fixtures_path('foobar'), self.versions_path))

    def test_can_retrieve_from_setting(self):
        expected = unittest.fixtures_path(os.path.join('get_php_executable', 'php'))
        actual = _get_php_executable(unittest.fixtures_path('foobar'), self.versions_path, expected)

        self.assertEqual(actual, expected)

    def test_setting_not_found_raises_exeption(self):
        with self.assertRaisesRegex(ValueError, 'phpunit\\.php_executable.*is not an executable file'):
            _get_php_executable(
                unittest.fixtures_path('foobar'),
                self.versions_path,
                unittest.fixtures_path(os.path.join('get_php_executable', 'foobar'))
            )

    @unittest.mock.patch('PHPUnitKit.plugin.platform')
    def test_linux_get_from_php_version_file(self, platform):
        platform.return_value = 'linux'
        expected = unittest.fixtures_path(os.path.join('get_php_executable', 'versions', '7.3.0', 'bin', 'php'))
        actual = _get_php_executable(
            unittest.fixtures_path('get_php_executable'),
            self.versions_path,
            unittest.fixtures_path('get_php_executable')
        )

        self.assertEqual(actual, expected)

    @unittest.mock.patch('PHPUnitKit.plugin.platform')
    def test_windows_get_from_php_version_file(self, platform):
        platform.return_value = 'windows'
        expected = unittest.fixtures_path(os.path.join('get_php_executable', 'versions', '7.3.0', 'php.exe'))
        actual = _get_php_executable(
            unittest.fixtures_path('get_php_executable'),
            self.versions_path,
            unittest.fixtures_path('get_php_executable')
        )

        self.assertEqual(actual, expected)

    def test_invalid_version_file_number_raises_exception(self):
        with self.assertRaisesRegex(ValueError, 'not a valid version number'):
            _get_php_executable(unittest.fixtures_path('get_php_executable/invalid'), self.versions_path)

    def test_no_versions_path_raises_exception(self):
        with self.assertRaisesRegex(ValueError, 'is not set'):
            _get_php_executable(unittest.fixtures_path('get_php_executable'), None)

    def test_invalid_versions_path_raises_exception(self):
        with self.assertRaisesRegex(ValueError, 'does not exist or is not a valid directory'):
            _get_php_executable(unittest.fixtures_path('get_php_executable'), unittest.fixtures_path('foobar'))

    def test_non_executable_raises_exeption(self):
        if sublime.platform() == 'windows':
            actual = _get_php_executable(
                unittest.fixtures_path(os.path.join('get_php_executable', 'not_executable')),
                self.versions_path)
            expected = unittest.fixtures_path(os.path.join('get_php_executable', 'versions', '7.2.0', 'php.exe'))
            self.assertEqual(actual, expected)
        else:
            with self.assertRaisesRegex(ValueError, 'is not an executable file'):
                _get_php_executable(
                    unittest.fixtures_path(os.path.join('get_php_executable', 'not_executable')),
                    self.versions_path)
