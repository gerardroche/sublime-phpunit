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

from PHPUnitKit.lib.utils import get_phpunit_options


@unittest.mock.patch.dict('PHPUnitKit.lib.utils._session', {}, clear=True)
class TestGetPHPUnitOptions(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.view.settings().set('phpunit.options', {})

    def testget_phpunit_options_has_no_session(self):
        self.assertEquals({}, get_phpunit_options(self.view))
        self.view.settings().set('phpunit.options', {'no-coverage': True})
        self.assertEquals({'no-coverage': True}, get_phpunit_options(self.view))
        self.view.settings().set('phpunit.options', {'no-coverage': False, 'stop-on-defect': True})
        self.assertEquals({'no-coverage': False, 'stop-on-defect': True}, get_phpunit_options(self.view))
        self.view.settings().set('phpunit.options', None)  # type: ignore[arg-type]
        self.assertEquals({}, get_phpunit_options(self.view))

    @unittest.mock.patch.dict('PHPUnitKit.lib.utils._session', {'options': {'no-coverage': True}}, clear=True)
    def testget_phpunit_options_has_session(self):
        self.assertEquals({'no-coverage': True}, get_phpunit_options(self.view))
        self.view.settings().set('phpunit.options', {'no-coverage': True})
        self.assertEquals({'no-coverage': True}, get_phpunit_options(self.view))
        self.view.settings().set('phpunit.options', {'no-coverage': False})
        self.assertEquals({'no-coverage': True}, get_phpunit_options(self.view))
        self.view.settings().set('phpunit.options', {'no-progress': False})
        self.assertEquals({'no-coverage': True, 'no-progress': False}, get_phpunit_options(self.view))

    def test_artisan_should_never_enable_colors(self):
        self.view.settings().set('phpunit.strategy', 'sublime')
        self.view.settings().set('phpunit.artisan', True)
        self.assertEquals({'colors=never': True}, get_phpunit_options(self.view))
        self.view.settings().set('phpunit.strategy', 'sublime')

    def test_pest_and_artisan_only_disable_colors_for_the_basic_strategy(self):
        self.view.settings().set('phpunit.strategy', 'iterm')
        self.view.settings().set('phpunit.pest', True)
        self.view.settings().set('phpunit.artisan', True)
        self.assertEquals({}, get_phpunit_options(self.view))
