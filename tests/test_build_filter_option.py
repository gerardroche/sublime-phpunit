from PHPUnitKit.tests import unittest

from PHPUnitKit.plugin import build_filter_option


class TestBuildFilterOption(unittest.ViewTestCase):

    def test_single_item(self):
        self.assertEqual('::(a)( with data set .+)?$', build_filter_option(self.view, ['a']))

    def test_many_items(self):
        self.assertEqual('::(a|b)( with data set .+)?$', build_filter_option(self.view, ['a', 'b']))
        self.assertEqual('::(a|b|c)( with data set .+)?$', build_filter_option(self.view, ['a', 'b', 'c']))
        self.assertEqual('::(a|b|c)( with data set .+)?$', build_filter_option(self.view, ['b', 'c', 'a']))
        self.assertEqual('::test(a|b)( with data set .+)?$', build_filter_option(self.view, ['testa', 'testb']))

    def test_pest(self):
        self.view.settings().set('phpunit.pest', True)
        self.assertEqual('(fizz)', build_filter_option(self.view, ['fizz']))
        self.assertEqual('(fizz|buzz)', build_filter_option(self.view, ['fizz', 'buzz']))
