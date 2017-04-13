import re


from phpunitkit.tests.helpers import ViewTestCase


from phpunitkit.plugin import find_php_classes
from phpunitkit.plugin import has_test_case
from phpunitkit.plugin import build_cmd_options
from phpunitkit.plugin import is_valid_php_version_file_version


class FunctionsTest(ViewTestCase):

    def test_find_php_classes_returns_array_of_classes_in_view(self):
        self.set_view_content('<?php\nclass x {}\nclass y {}')
        self.assertEquals(['x', 'y'], find_php_classes(self.view))

    def test_find_php_classes_returns_empty_array_when_view_is_empty(self):
        self.set_view_content('a')
        self.assertEquals([], find_php_classes(self.view))

    def test_contains_phpunit_test_case_returns_true_when_view_has_test_case(self):
        self.set_view_content("<?php\nclass ExampleTest {}")
        self.assertTrue(has_test_case(self.view))

    def test_contains_phpunit_test_case_returns_false_when_view_has_no_test_case_classes(self):
        self.set_view_content('<?php\nclass x {}\nclass y {}')
        self.assertFalse(has_test_case(self.view))

    def test_contains_phpunit_test_case_returns_false_when_view_is_empty(self):
        self.set_view_content('')
        self.assertFalse(has_test_case(self.view))

    def test_build_cmd_options(self):
        self.assertEqual([], build_cmd_options({}, []))
        self.assertEqual([], build_cmd_options({'verbose': False}, []))
        self.assertEqual([], build_cmd_options({'v': False}, []))

        self.assertEqual(['-h'], build_cmd_options({'h': True}, []))
        self.assertEqual(['-v'], build_cmd_options({'v': True}, []))

        self.assertEqual(['--verbose'], build_cmd_options({'verbose': True}, []))
        self.assertEqual(['--no-coverage'], build_cmd_options({'no-coverage': True}, []))

        self.assertEqual(['--no-coverage', '--verbose'], sorted(build_cmd_options({'no-coverage': True, 'verbose': True}, [])))
        self.assertEqual(['-h', '-v'], sorted(build_cmd_options({'h': True, 'v': True}, [])))

        self.assertEqual(['-d', 'x', '-d', 'y', '-d', 'z'], build_cmd_options({'d': ['x', 'y', 'z']}, []))

    def test_is_valid_php_version_file_version(self):
        self.assertFalse(is_valid_php_version_file_version(''))
        self.assertFalse(is_valid_php_version_file_version(' '))
        self.assertFalse(is_valid_php_version_file_version('foobar'))

        self.assertTrue(is_valid_php_version_file_version('master'))
        self.assertFalse(is_valid_php_version_file_version('masterfoo'))

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

        self.assertFalse(is_valid_php_version_file_version('.'))
        self.assertFalse(is_valid_php_version_file_version('x'))
        self.assertFalse(is_valid_php_version_file_version('x.x'))
        self.assertFalse(is_valid_php_version_file_version('x.x.x'))
        self.assertFalse(is_valid_php_version_file_version('x'))

        self.assertTrue(is_valid_php_version_file_version('5.x'))
        self.assertTrue(is_valid_php_version_file_version('6.x'))
        self.assertTrue(is_valid_php_version_file_version('7.x'))
        self.assertTrue(is_valid_php_version_file_version('8.x'))

        self.assertTrue(is_valid_php_version_file_version('7.0.x'))
        self.assertTrue(is_valid_php_version_file_version('7.1.x'))
        self.assertTrue(is_valid_php_version_file_version('7.2.x'))

        self.assertTrue(is_valid_php_version_file_version('5.4snapshot'))
        self.assertTrue(is_valid_php_version_file_version('5.5snapshot'))
        self.assertTrue(is_valid_php_version_file_version('5.6snapshot'))
        self.assertTrue(is_valid_php_version_file_version('7.0snapshot'))
        self.assertTrue(is_valid_php_version_file_version('7.1snapshot'))

        self.assertTrue(is_valid_php_version_file_version('7.0.0snapshot'))
        self.assertTrue(is_valid_php_version_file_version('7.1.0snapshot'))
        self.assertTrue(is_valid_php_version_file_version('7.1.1snapshot'))

        self.assertFalse(is_valid_php_version_file_version('snapshot'))
