from PHPUnitKit.tests import unittest

from PHPUnitKit.plugin import refine_switchable_locations
from PHPUnitKit.plugin import Switchable


class TestSwitchable(unittest.TestCase):

    def test_file(self):
        switchable = Switchable((
            '/abs/path/to/File.php',
            'to/File.php',
            (20, 7)
        ))

        self.assertEqual(switchable.file, '/abs/path/to/File.php')


class TestRefineSwitchableLocations(unittest.TestCase):

    def assertLocation(self, file, location):
        self.assertEqual(refine_switchable_locations(locations=[location], file=file), ([location], True))

    def assertNotLocation(self, file, location):
        self.assertEqual(refine_switchable_locations(locations=[location], file=file), ([location], False))

    def test_not_locations(self):
        self.assertNotLocation(None,                        ('/path/to/ATest.php',              'to/ATest.php',                 (0, 0)))  # noqa: E241,E501
        self.assertNotLocation(None,                        ('/path/to/AClas.php',              'to/AClas.php',                 (0, 0)))  # noqa: E241,E501
        self.assertNotLocation('/path/to/Name.php',         ('/foo/bar/NameTest.php',           'bar/NameTest.php',             (0, 0)))  # noqa: E241,E501
        self.assertNotLocation('/path/to/NameTest.php',     ('/foo/bar/Name.php',               'bar/Name.php',                 (0, 0)))  # noqa: E241,E501

    def test_test_case(self):
        self.assertLocation('/path/to/Name.php',    ('/path/to/NameTest.php',                   'to/NameTest.php',              (0, 0)))  # noqa: E241,E501
        self.assertLocation('/path/to/Name.php',    ('/path/to/tests/NameTest.php',             'to/tests/NameTest.php',        (0, 0)))  # noqa: E241,E501
        self.assertLocation('/path/to/Name.php',    ('/path/to/Tests/NameTest.php',             'to/Tests/NameTest.php',        (0, 0)))  # noqa: E241,E501
        self.assertLocation('/path/to/Name.php',    ('/path/to/tests/Unit/NameTest.php',        'to/tests/Unit/NameTest.php',   (0, 0)))  # noqa: E241,E501
        self.assertLocation('/path/to/Name.php',    ('/path/to/tests/unit/NameTest.php',        'to/tests/unit/NameTest.php',   (0, 0)))  # noqa: E241,E501
        self.assertLocation('/path/to/Name.php',    ('/path/to/Tests/Unit/NameTest.php',        'to/Tests/Unit/NameTest.php',   (0, 0)))  # noqa: E241,E501
        self.assertLocation('/path/to/Name.php',    ('/path/to/Tests/unit/NameTest.php',        'to/Tests/unit/NameTest.php',   (0, 0)))  # noqa: E241,E501
        self.assertLocation('/path/to/a/lib/x/y/tests/NameTest.php', ('/path/to/a/lib/x/y/src/Name.php', 'a/lib/x/y/src/Name.php', (5, 13)))  # noqa: E241,E501

    def test_class(self):
        self.assertLocation('/path/to/NameTest.php',                    ('/path/to/Name.php', 'to/Name.php', (0, 0)))  # noqa: E241,E501
        self.assertLocation('/path/to/tests/NameTest.php',              ('/path/to/Name.php', 'to/Name.php', (0, 0)))  # noqa: E241,E501
        self.assertLocation('/path/to/Tests/NameTest.php',              ('/path/to/Name.php', 'to/Name.php', (0, 0)))  # noqa: E241,E501
        self.assertLocation('/path/to/tests/Unit/NameTest.php',         ('/path/to/Name.php', 'to/Name.php', (0, 0)))  # noqa: E241,E501
        self.assertLocation('/path/to/tests/unit/NameTest.php',         ('/path/to/Name.php', 'to/Name.php', (0, 0)))  # noqa: E241,E501
        self.assertLocation('/path/to/Tests/Unit/NameTest.php',         ('/path/to/Name.php', 'to/Name.php', (0, 0)))  # noqa: E241,E501
        self.assertLocation('/path/to/Tests/unit/NameTest.php',         ('/path/to/Name.php', 'to/Name.php', (0, 0)))  # noqa: E241,E501
        self.assertLocation('/path/to/a/lib/x/y/src/Name.php',          ('/path/to/a/lib/x/y/tests/NameTest.php', 'a/lib/x/y/tests/NameTest.php', (5, 13)))  # noqa: E241,E501

    def test_no_match(self):
        expected = ('/vendor/x/y/tests/a/b/FooTest.php', 'x/y/tests/a/b/FooTest.php', (5, 7))
        actual = refine_switchable_locations(locations=[expected], file='/a/y/z/Foo.php')

        self.assertEqual(actual, ([expected], False))

    def test_match(self):
        expected = ('/a/b/tests/Unit/app/x/y/ZTest.php', 'b/tests/Unit/app/x/y/ZTest.php', (7, 7))
        actual = refine_switchable_locations(locations=[expected], file='/a/b/app/x/y/Z.php')

        self.assertEqual(actual, ([expected], True))

    def test_match2(self):
        expected = ('/a/b/x/y/app/X/Y/Name.php', 'app/X/Y/Name.php', (25, 7))
        actual = refine_switchable_locations(locations=[expected], file='/a/b/x/y/tests/Unit/app/X/Y/NameTest.php')

        self.assertEqual(actual, ([expected], True))

    def test_match3(self):
        expected = ('/a/b/c/app/xxx/X.php', 'c/app/xxx/X.php', (60, 13))
        actual = refine_switchable_locations(locations=[
            expected,
            ('/a/b/c/app/xxx/X.php', 'c/app/xxx/X.php', (60, 13)),
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
            ('/a/b/c/vendor/x/y/X.php', 'c/vendor/x/y/X.php', (31, 7))],
            file='/a/b/c/tests/Unit/app/xxx/XTest.php')

        self.assertEqual(actual, ([expected], True))

    def test_match_relative_path_matches(self):
        expected = ('/a/b/c/CTest.php', 'b/c/CTest.php', (3, 5))
        actual = refine_switchable_locations(
            locations=[expected, ('/a/x/y/CTest.php', 'x/y/CTest.php', (7, 11))],
            file='/a/b/c/C.php'
        )

        self.assertEqual(actual, ([expected], True))

    def test_match_Tests_dir(self):
        expected = ('/a/b/c/Tests/CTest.php', 'b/c/Tests/CTest.php', (3, 5))
        actual = refine_switchable_locations(
            locations=[expected, ('/a/x/y/Tests/CTest.php', 'x/y/Tests/CTest.php', (7, 11))],
            file='/a/b/c/C.php'
        )

        self.assertEqual(actual, ([expected], True))

    def test_match_tests_dir(self):
        expected = ('/a/b/c/Tests/CTest.php', 'b/c/Tests/CTest.php', (3, 5))
        actual = refine_switchable_locations(
            locations=[expected, ('/a/x/y/Tests/CTest.php', 'x/y/Tests/CTest.php', (7, 11))],
            file='/a/b/c/C.php'
        )

        self.assertEqual(actual, ([expected], True))
