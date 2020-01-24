from PHPUnitKit.tests import unittest

from PHPUnitKit.plugin import is_valid_php_version_file_version


class TestIsValidPhpVersionFileVersion(unittest.TestCase):

    def test_invalid_values(self):
        self.assertFalse(is_valid_php_version_file_version(''))
        self.assertFalse(is_valid_php_version_file_version(' '))
        self.assertFalse(is_valid_php_version_file_version('foobar'))
        self.assertFalse(is_valid_php_version_file_version('masterfoo'))
        self.assertFalse(is_valid_php_version_file_version('.'))
        self.assertFalse(is_valid_php_version_file_version('x'))
        self.assertFalse(is_valid_php_version_file_version('x.x'))
        self.assertFalse(is_valid_php_version_file_version('x.x.x'))
        self.assertFalse(is_valid_php_version_file_version('x'))
        self.assertFalse(is_valid_php_version_file_version('snapshot'))

    def test_master_branch_version(self):
        self.assertTrue(is_valid_php_version_file_version('master'))

    def test_specific_semver_versions(self):
        self.assertTrue(is_valid_php_version_file_version('5.0.0'))
        self.assertTrue(is_valid_php_version_file_version('5.0.1'))
        self.assertTrue(is_valid_php_version_file_version('5.0.7'))
        self.assertTrue(is_valid_php_version_file_version('5.0.30'))
        self.assertTrue(is_valid_php_version_file_version('5.0.32'))
        self.assertTrue(is_valid_php_version_file_version('5.1.0'))
        self.assertTrue(is_valid_php_version_file_version('5.1.1'))
        self.assertTrue(is_valid_php_version_file_version('5.1.3'))
        self.assertTrue(is_valid_php_version_file_version('5.1.27'))
        self.assertTrue(is_valid_php_version_file_version('7.0.0'))
        self.assertTrue(is_valid_php_version_file_version('7.1.19'))

    def test_minor_versions(self):
        self.assertTrue(is_valid_php_version_file_version('5.6'))
        self.assertTrue(is_valid_php_version_file_version('7.1'))
        self.assertTrue(is_valid_php_version_file_version('7.2'))

    def test_major_dot_x_versions(self):
        self.assertTrue(is_valid_php_version_file_version('5.x'))
        self.assertTrue(is_valid_php_version_file_version('6.x'))
        self.assertTrue(is_valid_php_version_file_version('7.x'))
        self.assertTrue(is_valid_php_version_file_version('8.x'))

    def test_major_dot_minor_dot_x_versions(self):
        self.assertTrue(is_valid_php_version_file_version('7.0.x'))
        self.assertTrue(is_valid_php_version_file_version('7.1.x'))
        self.assertTrue(is_valid_php_version_file_version('7.2.x'))

    def test_snapshot_versions(self):
        self.assertTrue(is_valid_php_version_file_version('5.4snapshot'))
        self.assertTrue(is_valid_php_version_file_version('5.5snapshot'))
        self.assertTrue(is_valid_php_version_file_version('5.6snapshot'))
        self.assertTrue(is_valid_php_version_file_version('7.0snapshot'))
        self.assertTrue(is_valid_php_version_file_version('7.1snapshot'))
        self.assertTrue(is_valid_php_version_file_version('7.0.0snapshot'))
        self.assertTrue(is_valid_php_version_file_version('7.1.0snapshot'))
        self.assertTrue(is_valid_php_version_file_version('7.1.1snapshot'))
