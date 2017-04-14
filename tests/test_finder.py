import os
import unittest

from phpunitkit.plugin import find_phpunit_configuration_file


def fixtures_path():
    return os.path.join(os.path.dirname(__file__), 'fixtures')


class FindersTest(unittest.TestCase):

    def test_find_none(self):
        self.assertIsNone(find_phpunit_configuration_file(None, None))
        self.assertIsNone(find_phpunit_configuration_file('', ['']))
        self.assertIsNone(find_phpunit_configuration_file(' ', [' ']))

    def test_find_none_with_file(self):
        file = os.path.join(fixtures_path(), 'common_prefix_parent', 'valid', 'file.php')

        self.assertIsNone(find_phpunit_configuration_file(file, None))
        self.assertIsNone(find_phpunit_configuration_file(file, []))
        self.assertIsNone(find_phpunit_configuration_file(file, [' ']))
        self.assertIsNone(find_phpunit_configuration_file(file, ['foobarfoobar']))

    def test_find_none_with_folders(self):
        folders = [
            os.path.join(fixtures_path(), 'common_prefix_parent'),
            os.path.join(fixtures_path(), 'common_prefix_parent', 'has_phpunit_xml'),
            os.path.join(fixtures_path(), 'common_prefix_parent', 'has_phpunit_xml_dist')
        ]

        self.assertIsNone(find_phpunit_configuration_file(None, folders))
        self.assertIsNone(find_phpunit_configuration_file('', folders))
        self.assertIsNone(find_phpunit_configuration_file(' ', folders))
        self.assertIsNone(find_phpunit_configuration_file('foobarfoobar', folders))

    def test_find_phpunit_xml_dist(self):
        project_path = os.path.join(fixtures_path(), 'common_prefix_parent', 'has_phpunit_xml_dist')

        self.assertEqual(
            os.path.join(project_path, 'phpunit.xml.dist'),
            find_phpunit_configuration_file(
                os.path.join(project_path, 'src', 'Has', 'PHPUnitXmlDist.php'),
                [
                    os.path.join(fixtures_path(), 'common_prefix_parent'),
                    os.path.join(fixtures_path(), 'common_prefix_parent', 'has_phpunit_xml'),
                    os.path.join(fixtures_path(), 'common_prefix_parent', 'has_phpunit_xml_dist')
                ]
                )
        )

    def test_find_phpunit_xml_before_phpunit_xml_dist(self):
        project_path = os.path.join(fixtures_path(), 'common_prefix_parent', 'has_phpunit_xml')

        self.assertEqual(
            os.path.join(project_path, 'phpunit.xml'),
            find_phpunit_configuration_file(
                os.path.join(project_path, 'src', 'Has', 'PHPUnitXml.php'),
                [
                    os.path.join(fixtures_path(), 'common_prefix_parent'),
                    os.path.join(fixtures_path(), 'common_prefix_parent', 'has_phpunit_xml'),
                    os.path.join(fixtures_path(), 'common_prefix_parent', 'has_phpunit_xml_dist')
                ]
            )
        )

    def test_find_only_checks_as_far_as_the_nearest_common_prefix_of_folders(self):

        common_prefix_parent = os.path.join(fixtures_path(), 'common_prefix_parent')
        common_prefix = os.path.join(common_prefix_parent, 'common_prefix')
        folder_a = os.path.join(common_prefix, 'folder_a')
        folder_b = os.path.join(common_prefix, 'folder_b')

        php_file = os.path.join(folder_a, 'FileA.php')
        folders = [folder_a, folder_b]

        self.assertIsNone(find_phpunit_configuration_file(php_file, folders))

        # adding the common prefix parent directory should yield success
        folders.append(common_prefix_parent)
        phpunit_xml_file = os.path.join(common_prefix_parent, 'phpunit.xml.dist')
