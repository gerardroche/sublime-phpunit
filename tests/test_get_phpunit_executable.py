import os

from PHPUnitKit.plugin import _get_phpunit_executable
from PHPUnitKit.tests import unittest


class TestGetPHPUnitExecutable(unittest.TestCase):

    @unittest.mock.patch('shutil.which')
    @unittest.mock.patch('PHPUnitKit.plugin.platform')
    def test_composer_linux_executable(self, platform, shutil_which):
        platform.return_value = 'linux'
        expected = unittest.fixtures_path(os.path.join('get_phpunit_executable', 'vendor', 'bin', 'phpunit'))
        actual = _get_phpunit_executable(unittest.fixtures_path('get_phpunit_executable'))

        self.assertEqual(expected, actual)
        self.assertEqual(shutil_which.call_count, 0)

    @unittest.mock.patch('shutil.which')
    @unittest.mock.patch('PHPUnitKit.plugin.platform')
    def test_composer_windows_executable(self, platform, shutil_which):
        platform.return_value = 'windows'
        expected = unittest.fixtures_path(os.path.join('get_phpunit_executable', 'vendor', 'bin', 'phpunit.bat'))
        actual = _get_phpunit_executable(unittest.fixtures_path('get_phpunit_executable'))

        self.assertEqual(expected, actual)
        self.assertEqual(shutil_which.call_count, 0)

    @unittest.mock.patch('shutil.which')
    def test_system_path_executable(self, shutil_which):
        shutil_which.return_value = 'shutil_which_executable'
        actual = _get_phpunit_executable(unittest.fixtures_path('foobar'))

        self.assertEqual('shutil_which_executable', actual)
        self.assertEqual(shutil_which.call_count, 1)

    @unittest.mock.patch('shutil.which')
    def test_raises_exeption_when_no_executable(self, shutil_which):
        shutil_which.return_value = None
        with self.assertRaisesRegex(ValueError, 'phpunit not found'):
            _get_phpunit_executable(unittest.fixtures_path('foobar'))

        self.assertEqual(shutil_which.call_count, 1)

    @unittest.mock.patch('shutil.which')
    def test_disable_composer_executable_discovery(self, shutil_which):
        _get_phpunit_executable(unittest.fixtures_path('get_phpunit_executable'), include_composer_vendor_dir=False)

        self.assertEqual(shutil_which.call_count, 1)

    @unittest.mock.patch('shutil.which')
    def test_enable_composer_executable_discovery(self, shutil_which):
        _get_phpunit_executable(unittest.fixtures_path('get_phpunit_executable'), include_composer_vendor_dir=True)

        self.assertEqual(shutil_which.call_count, 0)
