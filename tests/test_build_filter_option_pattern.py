from unittest import TestCase

from phpunitkit.plugin import build_filter_option_pattern


class TestBuildFilterOptionPattern(TestCase):

    def test_single_item(self):
        self.assertEqual('::(a)( with data set .+)?$', build_filter_option_pattern(['a']))

    def test_many_items(self):
        self.assertEqual('::(a|b)( with data set .+)?$', build_filter_option_pattern(['a', 'b']))
        self.assertEqual('::(a|b|c)( with data set .+)?$', build_filter_option_pattern(['a', 'b', 'c']))
        self.assertEqual('::(a|b|c)( with data set .+)?$', build_filter_option_pattern(['b', 'c', 'a']))
