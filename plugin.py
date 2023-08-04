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

import sublime_plugin

from PHPUnitKit.lib.events import Listener
from PHPUnitKit.lib.runner import PHPUnit
from PHPUnitKit.lib.utils import toggle_on_post_save


class PhpunitTestSuiteCommand(sublime_plugin.WindowCommand):

    def run(self, **options):
        PHPUnit(self.window).run(options=options)


class PhpunitTestFileCommand(sublime_plugin.WindowCommand):

    def run(self, **options):
        PHPUnit(self.window).run_file(options=options)


class PhpunitTestLastCommand(sublime_plugin.WindowCommand):

    def run(self):
        PHPUnit(self.window).run_last()


class PhpunitTestNearestCommand(sublime_plugin.WindowCommand):

    def run(self, **options):
        PHPUnit(self.window).run_nearest(options=options)


class PhpunitTestResultsCommand(sublime_plugin.WindowCommand):

    def run(self):
        PHPUnit(self.window).show()


class PhpunitTestCancelCommand(sublime_plugin.WindowCommand):

    def run(self):
        PHPUnit(self.window).cancel()


class PhpunitTestVisitCommand(sublime_plugin.WindowCommand):

    def run(self):
        PHPUnit(self.window).visit()


class PhpunitTestSwitchCommand(sublime_plugin.WindowCommand):

    def run(self):
        PHPUnit(self.window).switch()


class PhpunitToggleOptionCommand(sublime_plugin.WindowCommand):

    def run(self, option, value=None):
        PHPUnit(self.window).toggle(option, value)


class PhpunitTestCoverageCommand(sublime_plugin.WindowCommand):

    def run(self):
        PHPUnit(self.window).coverage()


class PhpunitListener(sublime_plugin.EventListener):

    def on_post_save(self, view):
        Listener().on_post_save(view)


class PhpunitToggleCommand(sublime_plugin.WindowCommand):

    def run(self, action):
        view = self.window.active_view()
        if not view:
            return

        if action == 'test_file_on_post_save':
            toggle_on_post_save(view, 'phpunit_test_file')


class PhpunitSideBarTestFileCommand(sublime_plugin.WindowCommand):

    def run(self, files):
        file = self._getTestableFile(files)
        if file:
            PHPUnit(self.window).run_file(file)
        else:
            PHPUnit(self.window).run_file()

    def is_enabled(self, files):
        return len(files) == 0 or bool(self._getTestableFile(files))

    def _getTestableFile(self, files):
        if files and len(files) == 1 and files[0].endswith('.php'):
            return files[0]

        return None
