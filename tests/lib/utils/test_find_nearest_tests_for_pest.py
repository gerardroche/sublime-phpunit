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

from PHPUnitKit.lib.utils import find_nearest_tests


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
