# Copyright (C) 2023 Gerard Roche
#
# This file is part of PHPUnitKit.
#
# PHPUnitKit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PHPUnitKit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PHPUnitKit.  If not, see <https://www.gnu.org/licenses/>.

from PHPUnitKit.tests import unittest

from PHPUnitKit.lib.utils import build_filter_option


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
