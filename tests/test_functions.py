import re
import unittest

import sublime

from phpunitkit.plugin import build_cmd_options
from phpunitkit.plugin import is_valid_php_version_file_version
from phpunitkit.plugin import exec_file_regex


class FunctionsTest(unittest.TestCase):

    def test_build_cmd_options(self):
        self.assertEqual([], build_cmd_options({}, []))
        self.assertEqual([], build_cmd_options({'verbose': False}, []))
        self.assertEqual([], build_cmd_options({'v': False}, []))

        self.assertEqual(['-h'], build_cmd_options({'h': True}, []))
        self.assertEqual(['-v'], build_cmd_options({'v': True}, []))

        self.assertEqual(['--verbose'], build_cmd_options({'verbose': True}, []))
        self.assertEqual(['--no-coverage'], build_cmd_options({'no-coverage': True}, []))

        self.assertEqual(['--no-coverage', '--verbose'], sorted(build_cmd_options({'no-coverage': True, 'verbose': True}, [])))
        self.assertEqual(['-h', '-v'], sorted(build_cmd_options({'h': True, 'v': True}, [])))

        self.assertEqual(['-d', 'x', '-d', 'y', '-d', 'z'], build_cmd_options({'d': ['x', 'y', 'z']}, []))

    def test_is_valid_php_version_file_version(self):
        self.assertFalse(is_valid_php_version_file_version(''))
        self.assertFalse(is_valid_php_version_file_version(' '))
        self.assertFalse(is_valid_php_version_file_version('foobar'))

        self.assertTrue(is_valid_php_version_file_version('master'))
        self.assertFalse(is_valid_php_version_file_version('masterfoo'))

        self.assertTrue(is_valid_php_version_file_version('5.0.0'))
        self.assertTrue(is_valid_php_version_file_version('5.0.1'))
        self.assertTrue(is_valid_php_version_file_version('5.0.7'))
        self.assertTrue(is_valid_php_version_file_version('5.0.30'))
        self.assertTrue(is_valid_php_version_file_version('5.0.32'))
        self.assertTrue(is_valid_php_version_file_version('5.1.0'))
        self.assertTrue(is_valid_php_version_file_version('5.1.1'))
        self.assertTrue(is_valid_php_version_file_version('5.1.3'))
        self.assertTrue(is_valid_php_version_file_version('5.1.27'))
        self.assertTrue(is_valid_php_version_file_version('7.0.0'))
        self.assertTrue(is_valid_php_version_file_version('7.1.19'))

        self.assertFalse(is_valid_php_version_file_version('.'))
        self.assertFalse(is_valid_php_version_file_version('x'))
        self.assertFalse(is_valid_php_version_file_version('x.x'))
        self.assertFalse(is_valid_php_version_file_version('x.x.x'))
        self.assertFalse(is_valid_php_version_file_version('x'))

        self.assertTrue(is_valid_php_version_file_version('5.x'))
        self.assertTrue(is_valid_php_version_file_version('6.x'))
        self.assertTrue(is_valid_php_version_file_version('7.x'))
        self.assertTrue(is_valid_php_version_file_version('8.x'))

        self.assertTrue(is_valid_php_version_file_version('7.0.x'))
        self.assertTrue(is_valid_php_version_file_version('7.1.x'))
        self.assertTrue(is_valid_php_version_file_version('7.2.x'))

        self.assertTrue(is_valid_php_version_file_version('5.4snapshot'))
        self.assertTrue(is_valid_php_version_file_version('5.5snapshot'))
        self.assertTrue(is_valid_php_version_file_version('5.6snapshot'))
        self.assertTrue(is_valid_php_version_file_version('7.0snapshot'))
        self.assertTrue(is_valid_php_version_file_version('7.1snapshot'))

        self.assertTrue(is_valid_php_version_file_version('7.0.0snapshot'))
        self.assertTrue(is_valid_php_version_file_version('7.1.0snapshot'))
        self.assertTrue(is_valid_php_version_file_version('7.1.1snapshot'))

        self.assertFalse(is_valid_php_version_file_version('snapshot'))

    def test_exec_file_regex(self):

        def assert_false(test):
            self.assertFalse(bool(re.match(exec_file_regex(), test)))

        def test_matches_one(test, expected_path, expected_line_number):
            res = re.findall(exec_file_regex(), test)
            self.assertTrue(len(res) == 1)
            self.assertEqual(res[0][0], expected_path)
            self.assertEqual(res[0][1], expected_line_number)

        assert_false('')
        assert_false('  ')
        assert_false('foobar')

        if sublime.platform() == 'windows':
            test_matches_one('C:\\code\\file.php:11', 'C:\\code\\file.php', '11')
            test_matches_one('C:\\code\\file.php:22    ', 'C:\\code\\file.php', '22')
            test_matches_one('    C:\\code\\file.php:33', 'C:\\code\\file.php', '33')
            test_matches_one('  C:\\code\\file.php:44    ', 'C:\\code\\file.php', '44')

            test_matches_one('C:\\code\\test\\DeepThoughtTest.php:9', 'C:\\code\\test\\DeepThoughtTest.php', '9')

            test_matches_one(
                'C:\\home\\user\\code\\tests\\DeepThoughtTest.php on line 20',
                'C:\\home\\user\\code\\tests\\DeepThoughtTest.php',
                '20'
            )

            test_matches_one(
                'PHP Fatal error:  Class \'Vendor\Package\Exception\' not found in C:\\home\\user\\code\\tests\\DeepThoughtTest.php on line 20',
                'C:\\home\\user\\code\\tests\\DeepThoughtTest.php',
                '20'
            )

            test_matches_one(
                'PHP   1. {main}() C:\\home\\user\\code\\vendor\\phpunit\\phpunit\\phpunit:0',
                'C:\\home\\user\\code\\vendor\\phpunit\\phpunit\\phpunit',
                '0'
            )

            test_matches_one(
                '0.3400    4950336   7. PHPUnit_Framework_TestCase->run() C:\\home\\user\\code\\project\\vendor\\phpunit\\phpunit\\src\\Framework\\TestSuite.php:722',
                'C:\\home\\user\\code\\project\\vendor\\phpunit\\phpunit\\src\\Framework\\TestSuite.php',
                '722'
            )

            test_matches_one(
                'PHP Warning:  require(C:\\home\\user\\code\\test\\..\\src\\PHP.php): failed to open stream: No such file or directory in C:\\home\\user\\code\\test\\bootstrap.php on line 6',
                'C:\\home\\user\\code\\test\\bootstrap.php',
                '6',
            )
        else:

            test_matches_one('/code/file.php:11', '/code/file.php', '11')
            test_matches_one('/code/file.php:22    ', '/code/file.php', '22')
            test_matches_one('    /code/file.php:33', '/code/file.php', '33')
            test_matches_one('  /code/file.php:44    ', '/code/file.php', '44')

            test_matches_one('/code/test/DeepThoughtTest.php:9', '/code/test/DeepThoughtTest.php', '9')

            test_matches_one(
                '/home/user/code/tests/DeepThoughtTest.php on line 20',
                '/home/user/code/tests/DeepThoughtTest.php',
                '20'
            )

            test_matches_one(
                'PHP Fatal error:  Class \'Vendor\Package\Exception\' not found in /home/user/code/tests/DeepThoughtTest.php on line 20',
                '/home/user/code/tests/DeepThoughtTest.php',
                '20'
            )

            test_matches_one(
                'PHP   1. {main}() /home/user/code/vendor/phpunit/phpunit/phpunit:0',
                '/home/user/code/vendor/phpunit/phpunit/phpunit',
                '0'
            )

            test_matches_one(
                '0.3400    4950336   7. PHPUnit_Framework_TestCase->run() /home/user/code/project/vendor/phpunit/phpunit/src/Framework/TestSuite.php:722',
                '/home/user/code/project/vendor/phpunit/phpunit/src/Framework/TestSuite.php',
                '722'
            )

            test_matches_one(
                'PHP Warning:  require(/home/user/code/test/../src/PHP.php): failed to open stream: No such file or directory in /home/user/code/test/bootstrap.php on line 6',
                '/home/user/code/test/bootstrap.php',
                '6',
            )
