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

from PHPUnitKit.lib.runner import PHPUnit


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


class PhpunitEvents(sublime_plugin.EventListener):

    def on_post_save(self, view):
        file_name = view.file_name()
        if not file_name:
            return

        if not file_name.endswith('.php'):
            return

        post_save_commands = view.settings().get('phpunit.on_post_save')
        # 'run_test_file' is deprecated since 3.12.4; use 'phpunit_test_file' instead
        for command in ('phpunit_test_file', 'run_test_file'):
            if command in post_save_commands:
                PHPUnit(view.window()).run_file()
