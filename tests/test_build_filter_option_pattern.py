from PHPUnitKit.tests import unittest

from PHPUnitKit.plugin import build_filter_option_pattern


class TestBuildFilterOptionPattern(unittest.ViewTestCase):

    def test_single_item(self):
        self.assertEqual('::(a)( with data set .+)?$', build_filter_option_pattern(self.view, ['a']))

    def test_many_items(self):
        self.assertEqual('::(a|b)( with data set .+)?$', build_filter_option_pattern(self.view, ['a', 'b']))
        self.assertEqual('::(a|b|c)( with data set .+)?$', build_filter_option_pattern(self.view, ['a', 'b', 'c']))
        self.assertEqual('::(a|b|c)( with data set .+)?$', build_filter_option_pattern(self.view, ['b', 'c', 'a']))
        self.assertEqual('::test(a|b)( with data set .+)?$', build_filter_option_pattern(self.view, ['testa', 'testb']))

    def test_pest(self):
        self.view.settings().set('phpunit.pest', True)
        self.assertEqual('(fizz)', build_filter_option_pattern(self.view, ['fizz']))
        self.assertEqual('(fizz|buzz)', build_filter_option_pattern(self.view, ['fizz', 'buzz']))
