from phpunitkit.tests.helpers import ViewTestCase


from phpunitkit.plugin import find_php_classes
from phpunitkit.plugin import has_test_case
from phpunitkit.plugin import build_cmd_options


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
