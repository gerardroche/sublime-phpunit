import os
from PHPUnitKit.tests import unittest

from PHPUnitKit.plugin import find_phpunit_configuration_file
from PHPUnitKit.plugin import find_phpunit_working_directory


class TestFinders(unittest.TestCase):

    def test_find_none(self):
        self.assertIsNone(find_phpunit_configuration_file(None, None))
        self.assertIsNone(find_phpunit_configuration_file('', ['']))
        self.assertIsNone(find_phpunit_configuration_file(' ', [' ']))
        self.assertIsNone(find_phpunit_configuration_file([], []))
        self.assertIsNone(find_phpunit_configuration_file('foo', ''))

        self.assertIsNone(find_phpunit_working_directory(None, None))
        self.assertIsNone(find_phpunit_working_directory('', ['']))
        self.assertIsNone(find_phpunit_working_directory(' ', [' ']))

    def test_find_none_with_file(self):
        file = os.path.join(unittest.fixtures_path(), 'common_prefix_parent', 'valid', 'file.php')

        self.assertIsNone(find_phpunit_configuration_file(file, None))
        self.assertIsNone(find_phpunit_configuration_file(file, []))
        self.assertIsNone(find_phpunit_configuration_file(file, [' ']))
        self.assertIsNone(find_phpunit_configuration_file(file, ['foobarfoobar']))

    def test_find_none_with_folders(self):
        folders = [
            os.path.join(unittest.fixtures_path(), 'common_prefix_parent'),
            os.path.join(unittest.fixtures_path(), 'common_prefix_parent', 'has_phpunit_xml'),
            os.path.join(unittest.fixtures_path(), 'common_prefix_parent', 'has_phpunit_xml_dist')
        ]

        self.assertIsNone(find_phpunit_configuration_file(None, folders))
        self.assertIsNone(find_phpunit_configuration_file('', folders))
        self.assertIsNone(find_phpunit_configuration_file(' ', folders))
        self.assertIsNone(find_phpunit_configuration_file('foobarfoobar', folders))

    def test_find_phpunit_xml_dist(self):
        base_file_dir = os.path.join(unittest.fixtures_path(), 'common_prefix_parent', 'has_phpunit_xml_dist')

        file = os.path.join(base_file_dir, 'src', 'Has', 'PHPUnitXmlDist.php')

        folders = [
            os.path.join(unittest.fixtures_path(), 'common_prefix_parent'),
            os.path.join(unittest.fixtures_path(), 'common_prefix_parent', 'has_phpunit_xml'),
            os.path.join(unittest.fixtures_path(), 'common_prefix_parent', 'has_phpunit_xml_dist')
        ]

        expected = os.path.join(base_file_dir, 'phpunit.xml.dist')
        self.assertEqual(expected, find_phpunit_configuration_file(file, folders))

        expected = os.path.dirname(expected)
        self.assertEqual(expected, find_phpunit_working_directory(file, folders))

    def test_find_phpunit_xml_before_phpunit_xml_dist(self):
        base_file_dir = os.path.join(unittest.fixtures_path(), 'common_prefix_parent', 'has_phpunit_xml')

        file = os.path.join(base_file_dir, 'src', 'Has', 'PHPUnitXml.php')

        folders = [
            os.path.join(unittest.fixtures_path(), 'common_prefix_parent'),
            os.path.join(unittest.fixtures_path(), 'common_prefix_parent', 'has_phpunit_xml'),
            os.path.join(unittest.fixtures_path(), 'common_prefix_parent', 'has_phpunit_xml_dist')
        ]

        expected = os.path.join(base_file_dir, 'phpunit.xml')
        self.assertEqual(expected, find_phpunit_configuration_file(file, folders))

        expected = os.path.dirname(expected)
        self.assertEqual(expected, find_phpunit_working_directory(file, folders))

    def test_find_only_checks_as_far_as_the_nearest_common_prefix_of_folders(self):
        common_base_dir = os.path.join(unittest.fixtures_path(), 'common_prefix_parent')

        base_file_dir = os.path.join(common_base_dir, 'common_prefix', 'folder_a')

        file = os.path.join(base_file_dir, 'FileA.php')

        folders = [
            base_file_dir,
            os.path.join(common_base_dir, 'common_prefix', 'folder_b')
        ]

        self.assertIsNone(find_phpunit_configuration_file(file, folders))

        # adding the common prefix parent directory should yield success
        folders.append(common_base_dir)

        expected = os.path.join(common_base_dir, 'phpunit.xml.dist')
        self.assertEqual(expected, find_phpunit_configuration_file(file, folders))

        expected = os.path.dirname(expected)
        self.assertEqual(expected, find_phpunit_working_directory(file, folders))
