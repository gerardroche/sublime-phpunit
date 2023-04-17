from PHPUnitKit.tests import unittest
from PHPUnitKit.plugin import has_test


class TestHasTest(unittest.ViewTestCase):

    def test_empty(self):
        self.fixture('')
        self.assertFalse(has_test(self.view))

    def test_no_class(self):
        self.fixture('<?php\nfunction foo() {\n}')
        self.assertFalse(has_test(self.view))
        self.fixture('<?php\nfunction foo() {}\n$var = "string";\necho $var\n')
        self.assertFalse(has_test(self.view))

    def test_one_class(self):
        self.fixture("<?php\nclass ExampleTest {}")
        self.assertTrue(has_test(self.view))

    def test_many_classes(self):
        self.fixture('<?php\nclass x {}\nclass y {}\nclass z {}')
        self.assertFalse(has_test(self.view))

    def test_pest_tests(self):
        self.view.settings().set('phpunit.pest', True)
        self.fixture('<?php\ntest(\'sum\', function () {\n})')
        self.assertTrue(has_test(self.view))
        self.fixture('<?php\nit(\'sum\', function () {\n})')
        self.assertTrue(has_test(self.view))
        self.fixture('<?php\nsenario(\'sum\', function () {\n})')
        self.assertTrue(has_test(self.view))

    def test_pest_no_test(self):
        self.view.settings().set('phpunit.pest', True)
        self.fixture('<?php\nfoobar(\'sum\', function () {\n})')
        self.assertFalse(has_test(self.view))

    def test_pest_tests_with_leading_space(self):
        self.view.settings().set('phpunit.pest', True)
        self.fixture('<?php\n    it(\'sum\', function () {\n})')
        self.assertTrue(has_test(self.view))
        self.fixture('<?php\n    test(\'sum\', function () {\n})')
        self.assertTrue(has_test(self.view))
        self.fixture('<?php\n    senario(\'sum\', function () {\n})')
        self.assertTrue(has_test(self.view))

    def test_pest_tests_with_double_quote(self):
        self.view.settings().set('phpunit.pest', True)
        self.fixture('<?php\n    it("sum", function () {\n})')
        self.assertTrue(has_test(self.view))
        self.fixture('<?php\n    test("sum", function () {\n})')
        self.assertTrue(has_test(self.view))
        self.fixture('<?php\n    senario("sum", function () {\n})')
        self.assertTrue(has_test(self.view))
