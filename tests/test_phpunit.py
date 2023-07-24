from PHPUnitKit.plugin import _get_phpunit_options
from PHPUnitKit.plugin import set_last_run
from PHPUnitKit.tests import unittest


@unittest.mock.patch.dict('PHPUnitKit.plugin._session', {'options': {}}, clear=True)
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


@unittest.mock.patch.dict('PHPUnitKit.plugin._session', {'options': {}}, clear=True)
class TestPHPUnitToggle(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.view.settings().set('phpunit.options', {})

    def test_toggle_boolean_with_no_options_or_session(self):
        self.run_window_command('phpunit_toggle_option', {'option': 'no-coverage'})
        self.assertEquals({'no-coverage': True}, _get_phpunit_options(self.view))
        self.run_window_command('phpunit_toggle_option', {'option': 'no-coverage'})
        self.assertEquals({'no-coverage': False}, _get_phpunit_options(self.view))
        self.run_window_command('phpunit_toggle_option', {'option': 'no-coverage', 'value': True})
        self.assertEquals({'no-coverage': True}, _get_phpunit_options(self.view))
        self.run_window_command('phpunit_toggle_option', {'option': 'no-coverage', 'value': True})
        self.assertEquals({'no-coverage': None}, _get_phpunit_options(self.view))
        self.run_window_command('phpunit_toggle_option', {'option': 'no-coverage', 'value': True})
        self.assertEquals({'no-coverage': True}, _get_phpunit_options(self.view))

    def test_toggle_boolean_with_options_but_no_session(self):
        self.view.settings().set('phpunit.options', {'no-coverage': True})
        self.run_window_command('phpunit_toggle_option', {'option': 'no-coverage'})
        self.assertEquals({'no-coverage': False}, _get_phpunit_options(self.view))
        self.run_window_command('phpunit_toggle_option', {'option': 'no-coverage'})
        self.assertEquals({'no-coverage': True}, _get_phpunit_options(self.view))
        self.run_window_command('phpunit_toggle_option', {'option': 'no-coverage'})
        self.assertEquals({'no-coverage': False}, _get_phpunit_options(self.view))

    @unittest.mock.patch.dict('PHPUnitKit.plugin._session', {'options': {'no-coverage': True}}, clear=True)
    def test_toggle_boolean_with_session(self):
        self.view.settings().set('phpunit.options', {})
        self.run_window_command('phpunit_toggle_option', {'option': 'no-coverage'})
        self.assertEquals({'no-coverage': False}, _get_phpunit_options(self.view))
        self.run_window_command('phpunit_toggle_option', {'option': 'no-coverage'})
        self.assertEquals({'no-coverage': True}, _get_phpunit_options(self.view))
        self.view.settings().set('phpunit.options', {'no-coverage': True})
        self.run_window_command('phpunit_toggle_option', {'option': 'no-coverage'})
        self.assertEquals({'no-coverage': False}, _get_phpunit_options(self.view))
        self.view.settings().set('phpunit.options', {'no-coverage': False})
        self.run_window_command('phpunit_toggle_option', {'option': 'no-coverage'})
        self.assertEquals({'no-coverage': True}, _get_phpunit_options(self.view))

    def test_toggle_string_with_no_options_or_session(self):
        self.run_window_command('phpunit_toggle_option', {'option': 'order-by=', 'value': 'depends,defects'})
        self.assertEquals({'order-by=': 'depends,defects'}, _get_phpunit_options(self.view))
        self.run_window_command('phpunit_toggle_option', {'option': 'order-by=', 'value': 'depends,defects'})
        self.assertEquals({'order-by=': None}, _get_phpunit_options(self.view))
        self.run_window_command('phpunit_toggle_option', {'option': 'order-by=', 'value': 'depends,defects'})
        self.assertEquals({'order-by=': 'depends,defects'}, _get_phpunit_options(self.view))
        self.run_window_command('phpunit_toggle_option', {'option': 'order-by=', 'value': 'default'})
        self.assertEquals({'order-by=': 'default'}, _get_phpunit_options(self.view))
        self.run_window_command('phpunit_toggle_option', {'option': 'order-by=', 'value': 'defects'})
        self.assertEquals({'order-by=': 'defects'}, _get_phpunit_options(self.view))
        self.run_window_command('phpunit_toggle_option', {'option': 'order-by=', 'value': 'defects'})
        self.assertEquals({'order-by=': None}, _get_phpunit_options(self.view))
