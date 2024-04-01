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

import os
import webbrowser

from sublime import ENCODED_POSITION
from sublime import status_message

from PHPUnitKit.lib import strategy
from PHPUnitKit.lib.utils import build_cmd_options
from PHPUnitKit.lib.utils import build_filter_option
from PHPUnitKit.lib.utils import debug_message
from PHPUnitKit.lib.utils import debug_settings
from PHPUnitKit.lib.utils import find_nearest_tests
from PHPUnitKit.lib.utils import find_phpunit_working_directory
from PHPUnitKit.lib.utils import find_switchable
from PHPUnitKit.lib.utils import get_active_view
from PHPUnitKit.lib.utils import get_last_run
from PHPUnitKit.lib.utils import get_osx_term_script_path
from PHPUnitKit.lib.utils import get_php_executable
from PHPUnitKit.lib.utils import get_phpunit_executable
from PHPUnitKit.lib.utils import get_phpunit_options
from PHPUnitKit.lib.utils import get_setting
from PHPUnitKit.lib.utils import has_test
from PHPUnitKit.lib.utils import is_debug
from PHPUnitKit.lib.utils import kill_any_running_tests
from PHPUnitKit.lib.utils import put_views_side_by_side
from PHPUnitKit.lib.utils import resolve_path_mapping
from PHPUnitKit.lib.utils import resolve_working_dir
from PHPUnitKit.lib.utils import save_views
from PHPUnitKit.lib.utils import set_last_run
from PHPUnitKit.lib.utils import set_session


class PHPUnit():

    def __init__(self, window):
        self.window = window
        self.view = get_active_view(window)

    def run(self, working_dir=None, file=None, options=None) -> None:
        debug_message('run working_dir=%s, file=%s, options=%s', working_dir, file, options)
        debug_settings(self.view)

        kill_any_running_tests(self.window)

        env = {}

        try:
            working_dir = resolve_working_dir(self.view, working_dir)
            php_executable = get_php_executable(self.view, working_dir)
            if php_executable:
                env['PATH'] = os.path.dirname(php_executable) + os.pathsep + os.environ['PATH']
            phpunit_executable = get_phpunit_executable(self.view, working_dir)
            options = get_phpunit_options(self.view, options)

            cmd = []

            try:
                cmd += get_setting(self.view, 'prepend_cmd')
            except TypeError:
                pass

            # Strategy
            if get_setting(self.view, 'strategy') == 'kitty':
                cmd += ['kitty', '--hold']
            elif get_setting(self.view, 'strategy') == 'iterm':
                cmd.append(get_osx_term_script_path())
            elif get_setting(self.view, 'strategy') == 'powershell':
                cmd += ['powershell', '-Command']
            elif get_setting(self.view, 'strategy') == 'xterm':
                cmd += ['xterm', '-hold', '-e']
            elif get_setting(self.view, 'strategy') == 'cmd':
                cmd += ['cmd.exe', '/c']

            if get_setting(self.view, 'ssh'):
                cmd += ['ssh']
                for ssh_option, ssh_option_value in get_setting(self.view, 'ssh_options').items():
                    cmd += [ssh_option]
                    if isinstance(ssh_option_value, str):
                        cmd += [ssh_option_value]

                cmd += ['{}@{}'.format(
                    get_setting(self.view, 'ssh_user'),
                    get_setting(self.view, 'ssh_host'))
                ]

                cmd += ['cd {working_dir};']

            if get_setting(self.view, 'docker'):
                cmd += get_setting(self.view, 'docker_command')

            cmd += phpunit_executable

            build_cmd_options(options, cmd)

            if file:
                cmd.append(os.path.relpath(file, working_dir))

            if get_setting(self.view, 'ssh'):
                cmd = resolve_path_mapping(self.view, 'ssh_paths', cmd)

            if get_setting(self.view, 'docker'):
                cmd = resolve_path_mapping(self.view, 'docker_paths', cmd)

        except Exception as e:
            status_message('PHPUnit: {}'.format(e))
            print('PHPUnit: \'{}\''.format(e))
            if is_debug(self.view):
                raise e
            return

        debug_message(
            'working dir: %s\n  php executable: %s\n  phpunit executable: %s\n  options: %s\n  env: %s\n  cmd: %s',
            working_dir,
            php_executable,
            phpunit_executable,
            options,
            env,
            cmd
        )

        if get_setting(self.view, 'save_all_on_run'):
            save_views(self.window)

        set_last_run({
            'working_dir': working_dir,
            'file': file,
            'options': options
        })

        if get_setting(self.view, 'strategy') == 'tmux':
            cmd = strategy.build_tmux_cmd(self.view, working_dir, cmd)

        strategy.execute(self.window, self.view, env, cmd, working_dir)

    def run_last(self) -> None:
        last_test_args = get_last_run()
        if not last_test_args:
            status_message('PHPUnit: no tests were run so far')
            return

        self.run(**last_test_args)

    def run_file(self, file=None, options=None) -> None:
        if file is None:
            file = self.view.file_name()

        if options is None:
            options = {}

        if not file:
            status_message('PHPUnit: not a test file')
            return

        if has_test(self.view):
            self.run(file=file, options=options)
        else:
            find_switchable(
                self.view,
                on_select=lambda switchable: self.run(
                    file=switchable.file,
                    options=options))

    def run_nearest(self, options) -> None:
        file = self.view.file_name()
        if not file:
            status_message('PHPUnit: not a test file')
            return

        if has_test(self.view):
            if 'filter' not in options:
                nearest_tests = find_nearest_tests(self.view)
                if nearest_tests:
                    options['filter'] = build_filter_option(self.view, nearest_tests)

            self.run(file=file, options=options)
        else:
            find_switchable(
                self.view,
                on_select=lambda switchable: self.run(
                    file=switchable.file,
                    options=options))

    def show(self) -> None:
        self.window.run_command('show_panel', {'panel': 'output.exec'})

    def cancel(self) -> None:
        kill_any_running_tests(self.window)

    def coverage(self) -> None:
        working_dir = find_phpunit_working_directory(self.view.file_name(), self.window.folders())
        if not working_dir:
            status_message('PHPUnit: could not find a PHPUnit working directory')
            return

        coverage_html_index_html_file = os.path.join(working_dir, 'build/coverage/index.html')
        if not os.path.exists(coverage_html_index_html_file):
            status_message('PHPUnit: could not find PHPUnit HTML code coverage %s' % coverage_html_index_html_file)  # noqa: E501
            return

        webbrowser.open_new_tab('file://' + coverage_html_index_html_file)

    def switch(self) -> None:
        def _on_switchable(switchable):
            self.window.open_file(switchable.file_encoded_position(self.view), ENCODED_POSITION)
            put_views_side_by_side(self.view, self.window.active_view())

        find_switchable(self.view, on_select=_on_switchable)

    def visit(self) -> None:
        test_last = get_last_run()
        if test_last:
            if 'file' in test_last and 'working_dir' in test_last:
                if test_last['file']:
                    file = os.path.join(test_last['working_dir'], test_last['file'])
                    if os.path.isfile(file):
                        return self.window.open_file(file)

        status_message('PHPUnit: no tests were run so far')

    def toggle(self, option: str, value=None) -> None:
        options = get_phpunit_options(self.view)
        new_options = options.copy()

        if value is None:
            # Option is a boolean, toggle it.
            # Default to true if no current value,
            # Otherwise negate it.
            cur_value = options.get(option)
            new_value = True if cur_value is None else not cur_value
            new_options[option] = new_value
        else:
            if option in options and options[option] == value:
                value = None
            new_options[option] = value

        # Diff out session values that are the same user settings. This is
        # better because it means if the user changes the setting in their
        # settings file it will take imediate effect.
        view_options = get_setting(self.view, 'options')
        for name, value in view_options.items():
            if name in new_options:
                if new_options[name] == value:
                    del new_options[name]

        set_session('options', new_options)
