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

from PHPUnitKit.lib.utils import build_cmd_options


class TestBuildCmdOptions(unittest.TestCase):

    def test_empty(self):
        self.assertEqual([], build_cmd_options({}, []))

    def test_long_option_when_false(self):
        self.assertEqual([], build_cmd_options({'verbose': False}, []))

    def test_long_option_when_true(self):
        self.assertEqual(['--verbose'], build_cmd_options({'verbose': True}, []))
        self.assertEqual(['--no-coverage'], build_cmd_options({'no-coverage': True}, []))

    def test_short_option_when_false(self):
        self.assertEqual([], build_cmd_options({'v': False}, []))

    def test_short_option_when_true(self):
        self.assertEqual(['-h'], build_cmd_options({'h': True}, []))
        self.assertEqual(['-v'], build_cmd_options({'v': True}, []))

    def test_long_options_when_true(self):
        self.assertEqual(
            ['--no-coverage', '--verbose'],
            sorted(build_cmd_options({'no-coverage': True, 'verbose': True}, []))
        )

    def test_short_options_when_true(self):
        self.assertEqual(['-h', '-v'], sorted(build_cmd_options({'h': True, 'v': True}, [])))

    def test_list_of_short_options(self):
        self.assertEqual(['-d', 'x', '-d', 'y', '-d', 'z'], build_cmd_options({'d': ['x', 'y', 'z']}, []))

    def test_long_option_with_value(self):
        self.assertEqual(
            ['--configuration', 'path/to/phpunit.xml'],
            sorted(build_cmd_options({'configuration': 'path/to/phpunit.xml'}, []))
        )

    def test_short_option_with_value(self):
        self.assertEqual(
            ['-c', 'path/to/phpunit.xml'],
            sorted(build_cmd_options({'c': 'path/to/phpunit.xml'}, []))
        )

    def test_key_equals_value_options(self):
        self.assertEqual(['--colors=always'], build_cmd_options({'colors=always': True}, []))
        self.assertEqual(['--colors=always'], build_cmd_options({'colors=': 'always'}, []))

    def test_required_string_value_option_imits_option_if_value_is_none(self):
        self.assertEqual([], build_cmd_options({'colors=always': False}, []))
        self.assertEqual([], build_cmd_options({'colors=': None}, []))
        self.assertEqual([], build_cmd_options({'colors': None}, []))
        self.assertEqual(['--colors=always'], build_cmd_options({'colors=': "always"}, []))
        self.assertEqual(['--colors', 'always'], build_cmd_options({'colors': 'always'}, []))
