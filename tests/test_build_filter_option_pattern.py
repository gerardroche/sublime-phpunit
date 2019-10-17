from PHPUnitKit.tests import unittest

from PHPUnitKit.plugin import build_filter_option_pattern


class TestBuildFilterOptionPattern(unittest.TestCase):

    def test_single_item(self):
        self.assertEqual('::(a)( with data set .+)?$', build_filter_option_pattern(['a']))

    def test_many_items(self):
        self.assertEqual('::(a|b)( with data set .+)?$', build_filter_option_pattern(['a', 'b']))
        self.assertEqual('::(a|b|c)( with data set .+)?$', build_filter_option_pattern(['a', 'b', 'c']))
        self.assertEqual('::(a|b|c)( with data set .+)?$', build_filter_option_pattern(['b', 'c', 'a']))
        self.assertEqual('::test(a|b)( with data set .+)?$', build_filter_option_pattern(['testa', 'testb']))
