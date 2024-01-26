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

from PHPUnitKit.lib.utils import _find_switchable_in_lookup_symbols
from PHPUnitKit.lib.utils import Switchable


class TestSwitchable(unittest.TestCase):

    def test_file(self):
        switchable = Switchable((
            '/abs/path/to/File.php',
            'to/File.php',
            (20, 7)
        ))

        self.assertEqual(switchable.file, '/abs/path/to/File.php')


class TestRefineSwitchableLocations(unittest.TestCase):

    def assertLocation(self, file, locations, expected=None):
        if not isinstance(locations, list):
            locations = [locations]

        if expected is None:
            expected = (locations, True)
        else:
            expected = expected

        self.assertEqual(_find_switchable_in_lookup_symbols(file, locations), expected)

    def assertNotLocation(self, file, location):
        self.assertEqual(_find_switchable_in_lookup_symbols(file, [location]), ([location], False))

    def test_not_locations(self):
        self.assertNotLocation(None, ('/path/to/ATest.php', 'to/ATest.php', (0, 0)))  # noqa: E501
        self.assertNotLocation(None, ('/path/to/AClas.php', 'to/AClas.php', (0, 0)))  # noqa: E501
        self.assertNotLocation('/path/to/Name.php', ('/foo/bar/NameTest.php', 'bar/NameTest.php', (0, 0)))  # noqa: E501
        self.assertNotLocation('/path/to/NameTest.php', ('/foo/bar/Name.php', 'bar/Name.php', (0, 0)))  # noqa: E501

    def test_test_case(self):
        self.assertLocation('/path/to/Name.php', ('/path/to/NameTest.php', 'to/NameTest.php', (0, 0)))  # noqa: E501
        self.assertLocation('/path/to/Name.php', ('/path/to/tests/NameTest.php', 'to/tests/NameTest.php', (0, 0)))  # noqa: E501
        self.assertLocation('/path/to/Name.php', ('/path/to/Tests/NameTest.php', 'to/Tests/NameTest.php', (0, 0)))  # noqa: E501
        self.assertLocation('/path/to/Name.php', ('/path/to/tests/Unit/NameTest.php', 'to/tests/Unit/NameTest.php', (0, 0)))  # noqa: E501
        self.assertLocation('/path/to/Name.php', ('/path/to/tests/unit/NameTest.php', 'to/tests/unit/NameTest.php', (0, 0)))  # noqa: E501
        self.assertLocation('/path/to/Name.php', ('/path/to/Tests/Unit/NameTest.php', 'to/Tests/Unit/NameTest.php', (0, 0)))  # noqa: E501
        self.assertLocation('/path/to/Name.php', ('/path/to/Tests/unit/NameTest.php', 'to/Tests/unit/NameTest.php', (0, 0)))  # noqa: E501
        self.assertLocation('/path/to/a/lib/x/y/tests/NameTest.php', ('/path/to/a/lib/x/y/src/Name.php', 'a/lib/x/y/src/Name.php', (5, 13)))  # noqa: E501

    def test_class(self):
        self.assertLocation('/path/to/NameTest.php', ('/path/to/Name.php', 'to/Name.php', (0, 0)))  # noqa: E501
        self.assertLocation('/path/to/tests/NameTest.php', ('/path/to/Name.php', 'to/Name.php', (0, 0)))  # noqa: E501
        self.assertLocation('/path/to/Tests/NameTest.php', ('/path/to/Name.php', 'to/Name.php', (0, 0)))  # noqa: E501
        self.assertLocation('/path/to/tests/Unit/NameTest.php', ('/path/to/Name.php', 'to/Name.php', (0, 0)))  # noqa: E501
        self.assertLocation('/path/to/tests/unit/NameTest.php', ('/path/to/Name.php', 'to/Name.php', (0, 0)))  # noqa: E501
        self.assertLocation('/path/to/Tests/Unit/NameTest.php', ('/path/to/Name.php', 'to/Name.php', (0, 0)))  # noqa: E501
        self.assertLocation('/path/to/Tests/unit/NameTest.php', ('/path/to/Name.php', 'to/Name.php', (0, 0)))  # noqa: E501
        self.assertLocation('/path/to/a/lib/x/y/src/Name.php', ('/path/to/a/lib/x/y/tests/NameTest.php', 'a/lib/x/y/tests/NameTest.php', (5, 13)))  # noqa: E501

    def test_test_complicated(self):
        self.assertLocation(
            file='/p/x/tests/Unit/A/S/T/B/NameTest.php',
            locations=[
                ('/p/x/app/A/B/T/S/Name.php', 'x/app/A/B/T/S/Name.php', (15, 13)),
                ('/p/x/app/A/S/T/B/Name.php', 'x/app/A/S/T/B/Name.php', (15, 13))],
            expected=([
                ('/p/x/app/A/S/T/B/Name.php', 'x/app/A/S/T/B/Name.php', (15, 13))], True))

        self.assertLocation(
            file='/p/x/app/A/S/T/B/Name.php',
            locations=[
                ('/p/x/tests/Unit/A/B/T/S/NameTest.php', 'x/tests/Unit/A/B/T/S/NameTest.php', (18, 13)),
                ('/p/x/tests/Unit/A/S/T/B/NameTest.php', 'x/tests/Unit/A/S/T/B/NameTest.php', (16, 13))],
            expected=([
                ('/p/x/tests/Unit/A/S/T/B/NameTest.php', 'x/tests/Unit/A/S/T/B/NameTest.php', (16, 13))], True))

    def test_no_match(self):
        expected = ('/vendor/x/y/tests/a/b/FooTest.php', 'x/y/tests/a/b/FooTest.php', (5, 7))
        actual = _find_switchable_in_lookup_symbols('/a/y/z/Foo.php', [expected])

        self.assertEqual(actual, ([expected], False))

    def test_match(self):
        expected = ('/a/b/tests/Unit/app/x/y/ZTest.php', 'b/tests/Unit/app/x/y/ZTest.php', (7, 7))
        actual = _find_switchable_in_lookup_symbols('/a/b/app/x/y/Z.php', [expected])

        self.assertEqual(actual, ([expected], True))

    def test_match2(self):
        expected = ('/a/b/x/y/app/X/Y/Name.php', 'app/X/Y/Name.php', (25, 7))
        actual = _find_switchable_in_lookup_symbols('/a/b/x/y/tests/Unit/app/X/Y/NameTest.php', [expected])

        self.assertEqual(actual, ([expected], True))

    def test_match3(self):
        expected = ('/a/b/c/app/xxx/X.php', 'c/app/xxx/X.php', (60, 13))
        actual = _find_switchable_in_lookup_symbols('/a/b/c/tests/Unit/app/xxx/XTest.php', [
            expected,
            ('/a/b/c/vendor/Foobar.php', 'c/vendor/Foobar.php', (4, 31)),
            ('/a/b/c/vendor/x/y/src/E/X.php', 'c/vendor/x/y/src/E/X.php', (33, 7)),
            ('/a/b/c/vendor/x/y/Goutte/X.php', 'c/vendor/x/y/Goutte/X.php', (30, 7)),
            ('/a/b/c/vendor/x/y/src/X.php', 'c/vendor/x/y/src/X.php', (25, 7)),
            ('/a/b/c/vendor/x/y/src/X.php', 'c/vendor/x/y/src/X.php', (7, 7)),
            ('/a/b/c/vendor/x/y/src/B/X.php', 'c/vendor/x/y/src/B/X.php', (9, 7)),
            ('/a/b/c/vendor/x/y/src/X.php', 'c/vendor/x/y/src/X.php', (41, 7)),
            ('/a/b/c/vendor/x/y/lib/D/X.php', 'c/vendor/x/y/lib/D/X.php', (20, 7)),
            ('/a/b/c/vendor/x/y/lib/X.php', 'c/vendor/x/y/lib/X.php', (44, 7)),
            ('/a/b/c/vendor/x/y/X.php', 'c/vendor/x/y/X.php', (29, 16)),
            ('/a/b/c/vendor/x/y/X.php', 'c/vendor/x/y/X.php', (31, 7))
        ])

        self.assertEqual(actual, ([expected], True))

    def test_match_relative_path_matches(self):
        expected = ('/a/b/c/CTest.php', 'b/c/CTest.php', (3, 5))
        actual = _find_switchable_in_lookup_symbols(
            '/a/b/c/C.php',
            [expected, ('/a/x/y/CTest.php', 'x/y/CTest.php', (7, 11))])

        self.assertEqual(actual, ([expected], True))

    def test_match_tests_dir(self):
        expected = ('/a/b/c/Tests/CTest.php', 'b/c/Tests/CTest.php', (3, 5))
        actual = _find_switchable_in_lookup_symbols(
            '/a/b/c/C.php',
            [expected, ('/a/x/y/Tests/CTest.php', 'x/y/Tests/CTest.php', (7, 11))])

        self.assertEqual(actual, ([expected], True))

    def test_match_tests_dir2(self):
        expected = ('/a/b/c/Tests/CTest.php', 'b/c/Tests/CTest.php', (3, 5))
        actual = _find_switchable_in_lookup_symbols(
            '/a/b/c/C.php',
            [expected, ('/a/x/y/Tests/CTest.php', 'x/y/Tests/CTest.php', (7, 11))])

        self.assertEqual(actual, ([expected], True))

    def test_similar_paths_but_single_match(self):
        actual = _find_switchable_in_lookup_symbols('/home/code/x/a/app/app/Models/Account.php', [
            ('/home/code/x/b/other/tests/Integration/Models/AccountTest.php', 'other/tests/Integration/Models/AccountTest.php', (17, 13)),  # noqa: E501
            ('/home/code/x/a/app/tests/Integration/Models/AccountTest.php', 'app/tests/Integration/Models/AccountTest.php', (15, 13))  # noqa: E501
        ])

        self.assertEqual(([
            ('/home/code/x/a/app/tests/Integration/Models/AccountTest.php', 'app/tests/Integration/Models/AccountTest.php', (15, 13))  # noqa: E501
        ], True), actual)
