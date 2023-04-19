from PHPUnitKit.tests import unittest
from PHPUnitKit.plugin import find_nearest_tests


class TestFindSelectedTestMethods(unittest.ViewTestCase):

    def test_find_one_method(self):
        self.view.settings().set('phpunit.pest', True)
        self.fixture("""<?php
            it('fi|zz', function () {
                expect(3)->toBe(3);
            });
        """)
        self.assertEqual(['fizz'], find_nearest_tests(self.view))

    def test_find_returns_none_if_pest_is_disable(self):
        self.view.settings().set('phpunit.pest', False)
        self.fixture("""<?php
            it('fi|zz', function () {
                expect(3)->toBe(3);
            });
        """)
        self.assertEqual([], find_nearest_tests(self.view))

    def test_find_two_methods(self):
        self.view.settings().set('phpunit.pest', True)
        self.fixture("""<?php
            it('fi|zz', function () {
                expect(3)->toBe(3);
            });
            it('bu|zz', function () {
                expect(3)->toBe(3);
            });
        """)
        self.assertEqual(['fizz', 'buzz'], find_nearest_tests(self.view))

    def test_find_one_method_when_cursor_within_test(self):
        self.view.settings().set('phpunit.pest', True)
        self.fixture("""<?php
            it('fizz', function () {
                |expect(3)->toBe(3);
            });
        """)

        self.assertEqual(['fizz'], find_nearest_tests(self.view))
