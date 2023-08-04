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

from PHPUnitKit.lib.utils import set_last_run
from PHPUnitKit.lib.utils import get_phpunit_options


@unittest.mock.patch.dict('PHPUnitKit.lib.utils._session', {'options': {}}, clear=True)
class TestPHPUnitVisit(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.view.settings().set('phpunit.options', {})

    @unittest.mock.patch('sublime.Window.open_file')
    def test_visit_known_file(self, open_file):
        set_last_run({
            'working_dir': self.fixturePath('visit'),
            'file': 'file.txt',
            'options': {'no-coverage': True}
        })

        self.run_window_command('phpunit_test_visit')

        open_file.assert_called_once_with(self.fixturePath('visit', 'file.txt'))

    @unittest.mock.patch('sublime.Window.open_file')
    def test_visit_is_noop_if_not_found(self, open_file):
        set_last_run({
            'working_dir': self.fixturePath('visit'),
            'file': 'not_found.txt',
            'options': {'no-coverage': True}
        })

        self.run_window_command('phpunit_test_visit')

        open_file.assert_not_called()


@unittest.mock.patch.dict('PHPUnitKit.lib.utils._session', {'options': {}}, clear=True)
class TestPHPUnitToggle(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.view.settings().set('phpunit.options', {})

    def test_toggle_boolean_with_no_options_or_session(self):
        self.run_window_command('phpunit_toggle_option', {'option': 'no-coverage'})
        self.assertEquals({'no-coverage': True}, get_phpunit_options(self.view))
        self.run_window_command('phpunit_toggle_option', {'option': 'no-coverage'})
        self.assertEquals({'no-coverage': False}, get_phpunit_options(self.view))
        self.run_window_command('phpunit_toggle_option', {'option': 'no-coverage', 'value': True})
        self.assertEquals({'no-coverage': True}, get_phpunit_options(self.view))
        self.run_window_command('phpunit_toggle_option', {'option': 'no-coverage', 'value': True})
        self.assertEquals({'no-coverage': None}, get_phpunit_options(self.view))
        self.run_window_command('phpunit_toggle_option', {'option': 'no-coverage', 'value': True})
        self.assertEquals({'no-coverage': True}, get_phpunit_options(self.view))

    def test_toggle_boolean_with_options_but_no_session(self):
        self.view.settings().set('phpunit.options', {'no-coverage': True})
        self.run_window_command('phpunit_toggle_option', {'option': 'no-coverage'})
        self.assertEquals({'no-coverage': False}, get_phpunit_options(self.view))
        self.run_window_command('phpunit_toggle_option', {'option': 'no-coverage'})
        self.assertEquals({'no-coverage': True}, get_phpunit_options(self.view))
        self.run_window_command('phpunit_toggle_option', {'option': 'no-coverage'})
        self.assertEquals({'no-coverage': False}, get_phpunit_options(self.view))

    @unittest.mock.patch.dict('PHPUnitKit.lib.utils._session', {'options': {'no-coverage': True}}, clear=True)
    def test_toggle_boolean_with_session(self):
        self.view.settings().set('phpunit.options', {})
        self.run_window_command('phpunit_toggle_option', {'option': 'no-coverage'})
        self.assertEquals({'no-coverage': False}, get_phpunit_options(self.view))
        self.run_window_command('phpunit_toggle_option', {'option': 'no-coverage'})
        self.assertEquals({'no-coverage': True}, get_phpunit_options(self.view))
        self.view.settings().set('phpunit.options', {'no-coverage': True})
        self.run_window_command('phpunit_toggle_option', {'option': 'no-coverage'})
        self.assertEquals({'no-coverage': False}, get_phpunit_options(self.view))
        self.view.settings().set('phpunit.options', {'no-coverage': False})
        self.run_window_command('phpunit_toggle_option', {'option': 'no-coverage'})
        self.assertEquals({'no-coverage': True}, get_phpunit_options(self.view))

    def test_toggle_string_with_no_options_or_session(self):
        self.run_window_command('phpunit_toggle_option', {'option': 'order-by=', 'value': 'depends,defects'})
        self.assertEquals({'order-by=': 'depends,defects'}, get_phpunit_options(self.view))
        self.run_window_command('phpunit_toggle_option', {'option': 'order-by=', 'value': 'depends,defects'})
        self.assertEquals({'order-by=': None}, get_phpunit_options(self.view))
        self.run_window_command('phpunit_toggle_option', {'option': 'order-by=', 'value': 'depends,defects'})
        self.assertEquals({'order-by=': 'depends,defects'}, get_phpunit_options(self.view))
        self.run_window_command('phpunit_toggle_option', {'option': 'order-by=', 'value': 'default'})
        self.assertEquals({'order-by=': 'default'}, get_phpunit_options(self.view))
        self.run_window_command('phpunit_toggle_option', {'option': 'order-by=', 'value': 'defects'})
        self.assertEquals({'order-by=': 'defects'}, get_phpunit_options(self.view))
        self.run_window_command('phpunit_toggle_option', {'option': 'order-by=', 'value': 'defects'})
        self.assertEquals({'order-by=': None}, get_phpunit_options(self.view))
