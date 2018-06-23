from PHPUnitKit.tests import unittest
from PHPUnitKit.plugin import has_test_case


class TestHasTestCase(unittest.ViewTestCase):

    def test_empty(self):
        self.fixture('')
        self.assertFalse(has_test_case(self.view))

    def test_no_class(self):
        self.fixture('<?php\nfunction foo() {}\n$var = "string";\necho $var\n')
        self.assertFalse(has_test_case(self.view))

    def test_one_class(self):
        self.fixture("<?php\nclass ExampleTest {}")
        self.assertTrue(has_test_case(self.view))

    def test_many_classes(self):
        self.fixture('<?php\nclass x {}\nclass y {}\nclass z {}')
        self.assertFalse(has_test_case(self.view))
