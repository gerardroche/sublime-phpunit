import os
import unittest
from unittest.mock import patch
from phpunitkit.tests.sublime_mock import sublime
from phpunitkit.tests.sublime_mock import sublime_plugin
with patch.dict('sys.modules', sublime=sublime, sublime_plugin=sublime_plugin):
    from phpunitkit.plugin import PHPUnitConfigurationFileFinder

class PHPUnitConfigurationFileFinderTest(unittest.TestCase):

    def setUp(self):
        self.finder = PHPUnitConfigurationFileFinder()
        self.fixtures_path = os.path.join(os.path.dirname(__file__), 'fixtures')
        self.file_name = os.path.join(self.fixtures_path, 'common_prefix_parent', 'valid', 'file.php')
        self.configuration_file = os.path.join(self.fixtures_path, 'common_prefix_parent', 'phpunit.xml.dist')
        self.folders = [
            os.path.join(self.fixtures_path, 'common_prefix_parent'),
            os.path.join(self.fixtures_path, 'common_prefix_parent', 'has_phpunit_xml'),
            os.path.join(self.fixtures_path, 'common_prefix_parent', 'has_phpunit_xml_dist')
        ]

    def test_find_none(self):

        # dirty tests

        self.assertIsNone(self.finder.find(None, None))
        self.assertIsNone(self.finder.find('', ['']))
        self.assertIsNone(self.finder.find(' ', [' ']))
        self.assertIsNone(self.finder.find(self.file_name, None))
        self.assertIsNone(self.finder.find(self.file_name, []))
        self.assertIsNone(self.finder.find(self.file_name, [' ']))
        self.assertIsNone(self.finder.find(self.file_name, ['foobarfoobar']))
        self.assertIsNone(self.finder.find(None, self.folders))
        self.assertIsNone(self.finder.find('', self.folders))
        self.assertIsNone(self.finder.find(' ', self.folders))
        self.assertIsNone(self.finder.find('foobarfoobar', self.folders))

    def test_find_phpunit_xml_dist(self):
        project_path = os.path.join(self.fixtures_path, 'common_prefix_parent', 'has_phpunit_xml_dist')
        file_name = os.path.join(project_path, 'src', 'Has', 'PHPUnitXmlDist.php')
        configuration_file = os.path.join(project_path, 'phpunit.xml.dist')
        self.assertEqual(configuration_file, self.finder.find(file_name, self.folders))

    def test_find_phpunit_xml_before_phpunit_xml_dist(self):
        project_path = os.path.join(self.fixtures_path, 'common_prefix_parent', 'has_phpunit_xml')
        file_name = os.path.join(project_path, 'src', 'Has', 'PHPUnitXml.php')
        configuration_file = os.path.join(project_path, 'phpunit.xml')
        self.assertEqual(configuration_file, self.finder.find(file_name, self.folders))

    def test_find_only_checks_as_far_as_the_nearest_common_prefix_of_folders(self):

        common_prefix_parent = os.path.join(self.fixtures_path, 'common_prefix_parent')
        common_prefix = os.path.join(common_prefix_parent, 'common_prefix')
        folder_a = os.path.join(common_prefix, 'folder_a')
        folder_b = os.path.join(common_prefix, 'folder_b')

        file_name = os.path.join(folder_a, 'FileA.php')
        folders =  [folder_a, folder_b]

        self.assertIsNone(self.finder.find(file_name, folders))

        # adding the common prefix parent directory should yield success
        folders.append(common_prefix_parent)
        configuration_file = os.path.join(common_prefix_parent, 'phpunit.xml.dist')

        self.assertEqual(configuration_file, self.finder.find(file_name, folders))
