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

import re

from sublime import platform

from PHPUnitKit.tests import unittest

from PHPUnitKit.lib.strategy import _exec_file_regex


class TestExecFileRegex(unittest.TestCase):

    def assertNotMatch(self, test):
        self.assertFalse(bool(re.match(_exec_file_regex(), test)))

    def assertMatchesOne(self, test, expected_path, expected_line_number):
        res = re.findall(_exec_file_regex(), test)
        self.assertTrue(len(res) == 1)
        self.assertEqual(res[0][0], expected_path)
        self.assertEqual(res[0][1], expected_line_number)

    def test_basic_no_matches(self):
        self.assertNotMatch('')
        self.assertNotMatch('  ')
        self.assertNotMatch('foobar')

    def test_file_paths(self):
        if platform() == 'windows':
            self.assertMatchesOne('C:\\code\\file.php:11', 'C:\\code\\file.php', '11')
            self.assertMatchesOne('C:\\code\\file.php:22    ', 'C:\\code\\file.php', '22')
            self.assertMatchesOne('    C:\\code\\file.php:33', 'C:\\code\\file.php', '33')
            self.assertMatchesOne('  C:\\code\\file.php:44    ', 'C:\\code\\file.php', '44')

            self.assertMatchesOne('C:\\code\\test\\DeepThoughtTest.php:9', 'C:\\code\\test\\DeepThoughtTest.php', '9')

            self.assertMatchesOne(
                'C:\\home\\user\\code\\tests\\DeepThoughtTest.php on line 20',
                'C:\\home\\user\\code\\tests\\DeepThoughtTest.php',
                '20'
            )

            self.assertMatchesOne(
                'PHP Fatal error:  Class \'Vendor\\Package\\Exception\' not found'
                ' in C:\\home\\user\\code\\tests\\DeepThoughtTest.php on line 20',
                'C:\\home\\user\\code\\tests\\DeepThoughtTest.php',
                '20'
            )

            self.assertMatchesOne(
                'PHP   1. {main}() C:\\home\\user\\code\\vendor\\phpunit\\phpunit\\phpunit:0',
                'C:\\home\\user\\code\\vendor\\phpunit\\phpunit\\phpunit',
                '0'
            )

            self.assertMatchesOne(
                '0.3400    4950336   7. PHPUnit_Framework_TestCase->run()'
                ' C:\\home\\user\\code\\project\\vendor\\phpunit\\phpunit\\src\\Framework\\TestSuite.php:722',
                'C:\\home\\user\\code\\project\\vendor\\phpunit\\phpunit\\src\\Framework\\TestSuite.php',
                '722'
            )

            self.assertMatchesOne(
                'PHP Warning:  require(C:\\home\\user\\code\\test\\..\\src\\PHP.php): failed to open stream:'
                ' No such file or directory in C:\\home\\user\\code\\test\\bootstrap.php on line 6',
                'C:\\home\\user\\code\\test\\bootstrap.php',
                '6',
            )
        else:

            self.assertMatchesOne('/code/file.php:11', '/code/file.php', '11')
            self.assertMatchesOne('/code/file.php:22    ', '/code/file.php', '22')
            self.assertMatchesOne('    /code/file.php:33', '/code/file.php', '33')
            self.assertMatchesOne('  /code/file.php:44    ', '/code/file.php', '44')

            self.assertMatchesOne('/code/test/DeepThoughtTest.php:9', '/code/test/DeepThoughtTest.php', '9')

            self.assertMatchesOne(
                '/home/user/code/tests/DeepThoughtTest.php on line 20',
                '/home/user/code/tests/DeepThoughtTest.php',
                '20'
            )

            self.assertMatchesOne(
                'PHP Fatal error:  Class \'Vendor\\Package\\Exception\''
                ' not found in /home/user/code/tests/DeepThoughtTest.php on line 20',
                '/home/user/code/tests/DeepThoughtTest.php',
                '20'
            )

            self.assertMatchesOne(
                'PHP   1. {main}() /home/user/code/vendor/phpunit/phpunit/phpunit:0',
                '/home/user/code/vendor/phpunit/phpunit/phpunit',
                '0'
            )

            self.assertMatchesOne(
                '0.3400    4950336   7. PHPUnit_Framework_TestCase->run()'
                ' /home/user/code/project/vendor/phpunit/phpunit/src/Framework/TestSuite.php:722',
                '/home/user/code/project/vendor/phpunit/phpunit/src/Framework/TestSuite.php',
                '722'
            )

            self.assertMatchesOne(
                'PHP Warning:  require(/home/user/code/test/../src/PHP.php): failed to open stream:'
                ' No such file or directory in /home/user/code/test/bootstrap.php on line 6',
                '/home/user/code/test/bootstrap.php',
                '6',
            )
