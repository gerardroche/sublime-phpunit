import unittest
from phpunitkit.tests.test_case import ViewTestCase
from phpunitkit.plugin import ViewHelpers

class ViewHelpersTest(ViewTestCase):

    def setUp(self):
        super().setUp()
        self.helpers = ViewHelpers(self.view)

    def test_find_php_classes_returns_array_of_classes_in_view(self):
        self.set_view_content('<?php\nclass x {}\nclass y {}')
        self.assertEquals(['x', 'y'], self.helpers.find_php_classes())

    def test_find_php_classes_returns_empty_array_when_view_is_empty(self):
        self.set_view_content('')
        self.assertEquals([], self.helpers.find_php_classes())

    def test_contains_phpunit_test_case_returns_true_when_view_has_test_case(self):
        self.set_view_content("<?php\nclass ExampleTest {}")
        self.assertTrue(self.helpers.contains_phpunit_test_case())

    def test_contains_phpunit_test_case_returns_false_when_view_has_no_test_case_classes(self):
        self.set_view_content('<?php\nclass x {}\nclass y {}')
        self.assertFalse(self.helpers.contains_phpunit_test_case())

    def test_contains_phpunit_test_case_returns_false_when_view_is_empty(self):
        self.set_view_content('')
        self.assertFalse(self.helpers.contains_phpunit_test_case())
