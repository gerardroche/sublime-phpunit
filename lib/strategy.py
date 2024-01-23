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
import re
import shlex

from sublime import cache_path
from sublime import load_resource
from sublime import platform

from PHPUnitKit.lib.utils import debug_message
from PHPUnitKit.lib.utils import get_setting
from PHPUnitKit.lib.utils import is_debug


def execute(window, view, env: dict, cmd: list, working_dir: str) -> None:
    if get_setting(view, 'strategy') in ('cmd', 'external', 'iterm', 'kitty', 'powershell', 'tmux', 'xterm'):
        window.run_command('exec', {
            'env': env,
            'cmd': cmd,
            'quiet': not is_debug(view),
            'shell': False,
            'working_dir': working_dir
        })

        # Don't display exec output panel.
        window.run_command('hide_panel', {'panel': 'output.exec'})
    else:
        window.run_command('exec', {
            'env': env,
            'cmd': cmd,
            'file_regex': _exec_file_regex(),
            'quiet': not is_debug(view),
            'shell': False,
            'syntax': 'Packages/{}/res/text-ui-result.sublime-syntax'.format(__name__.split('.')[0]),
            'word_wrap': False,
            'working_dir': working_dir
        })

        _create_exec_output_panel(view, env, cmd)


def _create_exec_output_panel(view, env, cmd) -> None:
    panel = view.window().create_output_panel('exec')

    if is_debug(view):
        header_text = []
        if env:
            header_text.append("env: {}\n".format(env))
        header_text.append("{}\n\n".format(' '.join(cmd)))
        panel.run_command('insert', {'characters': ''.join(header_text)})

    panel_settings = panel.settings()
    panel_settings.set('rulers', [])
    panel_settings.set('highlight_line', False)
    panel_settings.set('draw_indent_guides', False)
    panel_settings.set('draw_white_space', [])

    font_size = get_setting(view, 'font_size')
    if font_size:
        panel_settings.set('font_size', int(font_size))

    panel_settings.set('color_scheme', _get_color_scheme(view))


def _exec_file_regex() -> str:
    if platform() == 'windows':
        return '((?:[a-zA-Z]\\:)?\\\\[a-zA-Z0-9 \\.\\/\\\\_-]+)(?: on line |\\:)([0-9]+)'
    else:
        return '(\\/[a-zA-Z0-9 \\.\\/_-]+)(?: on line |\\:)([0-9]+)'


def _get_color_scheme(view):
    color_scheme = view.settings().get('color_scheme')

    # If the color scheme is using the new system then it is good.
    if color_scheme.endswith('.sublime-color-scheme'):
        return color_scheme

    try:
        color_scheme_resource = load_resource(color_scheme)

        # If the color scheme has PHPUnitKit specific rules then it is good.
        if 'phpunitkit' in color_scheme_resource or 'PHPUnitKit' in color_scheme_resource:
            return color_scheme

        # If the color scheme has region.*ish rules then it is good.
        if 'region.greenish' in color_scheme_resource:
            return color_scheme

        # Try to generate a patched color scheme from the current one with
        # additional rules for PHPUnit exec output panel color output.

        cs_head, cs_tail = os.path.split(color_scheme)
        cs_package = os.path.split(cs_head)[1]
        cs_name = os.path.splitext(cs_tail)[0]

        file_name = cs_package + '__' + cs_name + '.hidden-tmTheme'
        abs_file = os.path.join(cache_path(), __name__.split('.')[0], 'color-schemes', file_name)
        rel_file = 'Cache/{}/color-schemes/{}'.format(__name__.split('.')[0], file_name)

        debug_message('auto generating color scheme = %s', rel_file)

        if not os.path.exists(os.path.dirname(abs_file)):
            os.makedirs(os.path.dirname(abs_file))

        color_scheme_resource_partial = load_resource(
            'Packages/{}/res/text-ui-result-theme-partial.txt'.format(__name__.split('.')[0]))

        with open(abs_file, 'w', encoding='utf8') as f:
            f.write(re.sub(
                '</array>\\s*'
                '((<!--\\s*)?<key>.*</key>\\s*<string>[^<]*</string>\\s*(-->\\s*)?)*'
                '</dict>\\s*</plist>\\s*'
                '$',

                color_scheme_resource_partial + '\\n</array></dict></plist>',
                color_scheme_resource
            ))

        return rel_file
    except Exception as e:
        print('PHPUnit: an error occurred trying to patch color'
              ' scheme with PHPUnit test results colors: {}'.format(str(e)))

        return color_scheme


def build_tmux_cmd(view, working_dir: str, cmd: list) -> list:
    tmux_target = get_setting(view, 'tmux_target')

    # Try make initial cmd relative to working directory to reduce length.
    if cmd[0].startswith(working_dir):
        cmd = [os.path.relpath(cmd[0], working_dir)] + cmd[1:]

    key_cmds = []

    # Clear the terminal screen.
    if get_setting(view, 'tmux_clear'):
        clear_cmd = ['clear']
        if not get_setting(view, 'tmux_clear_scrollback'):
            clear_cmd.append('-x')
        key_cmds.append(shlex.join(clear_cmd))

    # Switch to the working directory.
    key_cmds.append(shlex.join(['cd', working_dir]))

    # The test command.
    key_cmds.append(shlex.join(cmd))

    # Run inside a subshell to avoid changing the current working directory.
    keys = '({})\n'.format(' && '.join(key_cmds))

    return ['tmux', 'send-keys', '-t', tmux_target, keys]
