from PHPUnitKit.plugin import _get_phpunit_options
from PHPUnitKit.tests import unittest


@unittest.mock.patch.dict('PHPUnitKit.plugin._session', {}, clear=True)
class TestGetPHPUnitOptions(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.view.settings().set('phpunit.options', {})

    def test_get_phpunit_options_has_no_session(self):
        self.assertEquals({}, _get_phpunit_options(self.view))
        self.view.settings().set('phpunit.options', {'no-coverage': True})
        self.assertEquals({'no-coverage': True}, _get_phpunit_options(self.view))
        self.view.settings().set('phpunit.options', {'no-coverage': False, 'stop-on-defect': True})
        self.assertEquals({'no-coverage': False, 'stop-on-defect': True}, _get_phpunit_options(self.view))
        self.view.settings().set('phpunit.options', None)  # type: ignore[arg-type]
        self.assertEquals({}, _get_phpunit_options(self.view))

    @unittest.mock.patch.dict('PHPUnitKit.plugin._session', {'options': {'no-coverage': True}}, clear=True)
    def test_get_phpunit_options_has_session(self):
        self.assertEquals({'no-coverage': True}, _get_phpunit_options(self.view))
        self.view.settings().set('phpunit.options', {'no-coverage': True})
        self.assertEquals({'no-coverage': True}, _get_phpunit_options(self.view))
        self.view.settings().set('phpunit.options', {'no-coverage': False})
        self.assertEquals({'no-coverage': True}, _get_phpunit_options(self.view))
        self.view.settings().set('phpunit.options', {'no-progress': False})
        self.assertEquals({'no-coverage': True, 'no-progress': False}, _get_phpunit_options(self.view))

    def test_artisan_should_never_enable_colors(self):
        self.view.settings().set('phpunit.strategy', 'basic')
        self.view.settings().set('phpunit.artisan', True)
        self.assertEquals({'colors=never': True}, _get_phpunit_options(self.view))
        self.view.settings().set('phpunit.strategy', 'basic')

    def test_pest_and_artisan_only_disable_colors_for_the_basic_strategy(self):
        self.view.settings().set('phpunit.strategy', 'iterm')
        self.view.settings().set('phpunit.pest', True)
        self.view.settings().set('phpunit.artisan', True)
        self.assertEquals({}, _get_phpunit_options(self.view))
