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

from PHPUnitKit.plugin import PhpunitListener
from PHPUnitKit.tests import unittest


class TestEvents(unittest.ViewTestCase):

    @unittest.mock.patch('sublime.View.file_name')
    @unittest.mock.patch('PHPUnitKit.plugin.PHPUnit.run_file')
    def test_can_run_test_file_on_post_save(self, phpunit, file_name):
        file_name.return_value = '/tmp/fizz.php'
        self.view.settings().set('phpunit.on_post_save', ['phpunit_test_file'])
        PhpunitListener().on_post_save(self.view)
        phpunit.assert_called()

    @unittest.mock.patch('sublime.View.file_name')
    @unittest.mock.patch('PHPUnitKit.plugin.PHPUnit')
    def test_on_post_save_event_does_not_run_if_file_is_not_a_real_file_on_disk(self, phpunit, file_name):
        file_name.return_value = None
        self.view.settings().set('phpunit.on_post_save', ['phpunit_test_file'])
        PhpunitListener().on_post_save(self.view)
        self.assertMockNotCalled(phpunit)

    @unittest.mock.patch('sublime.View.file_name')
    @unittest.mock.patch('PHPUnitKit.plugin.PHPUnit')
    def test_on_post_save_event_does_not_run_for_non_php_files(self, phpunit, file_name):
        file_name.return_value = '/tmp/fizz.txt'
        self.view.settings().set('phpunit.on_post_save', ['phpunit_test_file'])
        PhpunitListener().on_post_save(self.view)
        self.assertMockNotCalled(phpunit)

    @unittest.mock.patch('sublime.View.file_name')
    @unittest.mock.patch('PHPUnitKit.plugin.PHPUnit')
    def test_on_post_save_event_does_not_run_if_no_event_set(self, phpunit, file_name):
        file_name.return_value = '/tmp/fizz.php'
        self.view.settings().set('phpunit.on_post_save', [])
        PhpunitListener().on_post_save(self.view)
        self.assertMockNotCalled(phpunit)
