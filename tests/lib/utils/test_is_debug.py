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

from PHPUnitKit.lib.utils import is_debug
from PHPUnitKit.tests import unittest


class TestIsDebug(unittest.ViewTestCase):

    def test_is_debug(self):
        self.view.settings().set('phpunit.debug', False)
        self.view.settings().set('debug', False)

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
