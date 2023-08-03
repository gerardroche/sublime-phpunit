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


from PHPUnitKit.lib.runner import PHPUnit


class Listener():

    def on_post_save(self, view):
        file_name = view.file_name()
        if not file_name:
            return

        if not file_name.endswith('.php'):
            return

        # 'run_test_file' is deprecated since 3.12.4; use 'phpunit_test_file' instead
        for command in ('phpunit_test_file', 'run_test_file'):
            post_save_commands = view.settings().get('phpunit.on_post_save')
            if command in post_save_commands:
                PHPUnit(view.window()).run_file()
