from PHPUnitKit.tests import unittest
from PHPUnitKit.plugin import _DEBUG
from PHPUnitKit.plugin import is_debug


class TestIsDebug(unittest.ViewTestCase):

    def test_is_debug(self):
        self.view.settings().set('phpunit.debug', False)
        self.view.settings().set('debug', False)

        self.assertEqual(_DEBUG, is_debug(self.view))

        self.view.settings().set('phpunit.debug', True)
        self.assertTrue(is_debug(self.view))

        self.view.settings().set('phpunit.debug', False)
        self.assertFalse(is_debug(self.view))

        self.view.settings().set('phpunit.debug', False)
        self.assertFalse(is_debug(self.view))

        self.view.settings().set('debug', True)
        self.view.settings().set('phpunit.debug', True)
        self.assertTrue(is_debug(self.view))

        self.view.settings().set('debug', False)
        self.view.settings().set('phpunit.debug', True)
        self.assertTrue(is_debug(self.view))

        self.view.settings().set('debug', False)
        self.view.settings().set('phpunit.debug', False)
        self.assertFalse(is_debug(self.view))

        self.view.settings().set('debug', True)
        self.view.settings().set('phpunit.debug', False)
        self.assertFalse(is_debug(self.view))
