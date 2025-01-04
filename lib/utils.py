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
import shutil

from sublime import active_window
from sublime import platform
from sublime import status_message
from sublime import version


_PEST_TEST_PATTERN = '^\\s*(it|test)\\(("|\')(.*)("|\')'


_session = {}  # type: dict


def debug_message(msg, *args) -> None:
    window = active_window()
    if not window:
        return

    view = window.active_view()
    if not view:
        return

    if not is_debug(view):
        return

    if args:
        msg = msg % args
    print('PHPUnit: ' + msg)


def is_debug(view) -> bool:
    if view:
        return get_setting(view, 'debug')

    return False


def get_setting(view, name: str):
    return view.settings().get('phpunit.%s' % name)


def debug_settings(view) -> None:
    if int(version()) >= 4078 and is_debug(view):
        for key, val in view.settings().to_dict().items():
            if key.startswith('phpunit.'):
                debug_message('setting %s = %s', key, val)


def message(msg, *args) -> None:
    if args:
        msg = msg % args

    msg = 'PHPUnit: ' + msg

    print(msg)
    status_message(msg)


def get_active_view(window):
    active_view = window.active_view()

    if not active_view:
        raise ValueError('view not found')

    return active_view


def get_session(key: str):
    return _session.get(key)


def set_session(key: str, value) -> None:
    _session[key] = value


def get_last_run():
    return get_session('last_run')


def set_last_run(args: dict):
    return set_session('last_run', args)


def find_phpunit_configuration_file(file_name, folders):
    """
    Find the first PHPUnit configuration file.

    Finds either phpunit.xml or phpunit.xml.dist, in {file_name} directory or
    the nearest common ancestor directory in {folders}.
    """
    debug_message('find configuration for \'%s\' ...', file_name)
    debug_message('  found %d folders %s', len(folders) if folders else 0, folders)

    if file_name is None:
        return None

    if not isinstance(file_name, str):
        return None

    if not len(file_name) > 0:
        return None

    if folders is None:
        return None

    if not isinstance(folders, list):
        return None

    if not len(folders) > 0:
        return None

    ancestor_folders = []  # type: list
    common_prefix = os.path.commonprefix(folders)
    parent = os.path.dirname(file_name)
    while parent not in ancestor_folders and parent.startswith(common_prefix):
        ancestor_folders.append(parent)
        parent = os.path.dirname(parent)

    ancestor_folders.sort(reverse=True)

    debug_message('  found %d possible locations %s', len(ancestor_folders), ancestor_folders)

    candidate_configuration_file_names = ['phpunit.xml', 'phpunit.xml.dist', 'phpunit.dist.xml']
    debug_message('  looking for %s ...', candidate_configuration_file_names)
    for folder in ancestor_folders:
        for file_name in candidate_configuration_file_names:
            phpunit_configuration_file = os.path.join(folder, file_name)
            if os.path.isfile(phpunit_configuration_file):
                debug_message('  found configuration \'%s\'', phpunit_configuration_file)
                return phpunit_configuration_file

    debug_message('  no configuration found')

    return None


def find_phpunit_working_directory(file_name, folders):
    configuration_file = find_phpunit_configuration_file(file_name, folders)
    if configuration_file:
        return os.path.dirname(configuration_file)


def is_valid_php_identifier(string: str) -> bool:
    return bool(re.match('^[a-zA-Z_][a-zA-Z0-9_]*$', string))


def has_test(view) -> bool:
    for php_class in find_php_classes(view):
        if php_class[-4:] == 'Test':
            return True

    if get_setting(view, 'pest'):
        has_test = view.find(_PEST_TEST_PATTERN, 0)
        if has_test:
            return True

    return False


def find_php_classes(view, with_namespace: bool = False) -> list:
    classes = []

    # See https://github.com/sublimehq/sublime_text/issues/5499
    if int(version()) >= 4134:
        namespace_selector = 'embedding.php meta.namespace meta.path'
        class_as_regions_selector = 'embedding.php entity.name.class - meta.use'
    else:
        namespace_selector = 'source.php entity.name.namespace'
        class_as_regions_selector = 'source.php entity.name.class - meta.use'

    namespace = None
    for namespace_region in view.find_by_selector(namespace_selector):
        namespace = view.substr(namespace_region)
        break  # TODO handle files with multiple namespaces

    for class_as_region in view.find_by_selector(class_as_regions_selector):
        class_as_string = view.substr(class_as_region)
        if is_valid_php_identifier(class_as_string):
            if with_namespace:
                classes.append({
                    'namespace': namespace,
                    'class': class_as_string
                })
            else:
                classes.append(class_as_string)

    if int(version()) <= 3114:  # no pragma
        if not classes:
            for class_as_region in view.find_by_selector('source.php entity.name.type.class - meta.use'):
                class_as_string = view.substr(class_as_region)
                if is_valid_php_identifier(class_as_string):
                    classes.append(class_as_string)

    return classes


def find_nearest_tests(view) -> list:
    """
    Return a list of tests nearest to cursor.

    Return an empty list if no selections found.

    Selection can be anywhere inside one or more test methods.
    """
    method_names = []

    if get_setting(view, 'pest'):
        for sel in view.sel():
            test_pattern_start_pt = view.line(sel.b).end()
            test = view_rmatch(view, _PEST_TEST_PATTERN, test_pattern_start_pt)
            if test:
                method_names.append(test.group(3))

        return method_names

    function_regions = view.find_by_selector('entity.name.function')
    function_areas = []
    # Only include areas that contain function declarations.
    for function_area in view.find_by_selector('meta.function'):
        for function_region in function_regions:
            if function_region.intersects(function_area):
                function_areas.append(function_area)

    for region in view.sel():
        for i, area in enumerate(function_areas):
            if not area.a <= region.a <= area.b:
                continue

            if i not in function_regions and not area.intersects(function_regions[i]):
                continue

            word = view.substr(function_regions[i])
            if is_valid_php_identifier(word):
                method_names.append(word)
            break

    if int(version()) <= 3114:  # no pragma
        if not method_names:
            for region in view.sel():
                word_region = view.word(region)
                word = view.substr(word_region)
                if not is_valid_php_identifier(word):
                    return []

                scope_score = view.score_selector(word_region.begin(), 'entity.name.function.php')
                if scope_score > 0:
                    method_names.append(word)
                else:
                    return []

    ignore_methods = ['setup', 'teardown']

    return [m for m in method_names if m.lower() not in ignore_methods]


# Polyfill: There is no API to find a pattern in reverse direction.
# @see https://github.com/SublimeTextIssues/Core/issues/245
def view_rfind_all(view, pattern: str, start_pt: int, flags: int = 0):
    matches = view.find_all(pattern, flags)
    for region in matches:
        if region.b > start_pt:
            return reversed(matches[:matches.index(region)])

    return reversed(matches)


# Polyfill: There is no API to find a pattern in reverse direction.
# @see https://github.com/SublimeTextIssues/Core/issues/245
def view_rfind(view, pattern: str, start_pt: int, flags: int = 0):
    matches = view_rfind_all(view, pattern, start_pt, flags)
    if matches:
        try:
            return next(matches)
        except StopIteration:
            pass


def view_rmatch(view, pattern: str, start_pt: int, flags: int = 0):
    match = view_rfind(view, pattern, start_pt, flags)
    if match:
        return re.match(pattern, view.substr(match))


class Switchable:

    def __init__(self, location):
        self.location = location
        self.file = location[0]

    def file_encoded_position(self, view):
        window = view.window()

        file = self.location[0]
        row = self.location[2][0]
        col = self.location[2][1]

        # If the file we're switching to is already open,
        # then by default don't goto encoded position.
        for v in window.views():
            if v.file_name() == self.location[0]:
                row = None
                col = None

        # If cursor is on a symbol like a class method,
        # then try find the relating test method or vice-versa,
        # and use that as the encoded position to jump to.
        symbol = view.substr(view.word(view.sel()[0].b))
        if symbol:
            if symbol[:4] == 'test':
                symbol = symbol[4:]
                symbol = symbol[0].lower() + symbol[1:]
            else:
                symbol = 'test' + symbol[0].upper() + symbol[1:]

            locations = window.lookup_symbol_in_open_files(symbol)
            if locations:
                for location in locations:
                    if location[0] == self.location[0]:
                        row = location[2][0]
                        col = location[2][1]
                        break

        encoded_postion = ''
        if row:
            encoded_postion += ':' + str(row)
        if col:
            encoded_postion += ':' + str(col)

        return file + encoded_postion


def _get_switchable_lookup_symbols(window, classes: list) -> list:
    locations = []  # type: list
    for _class in classes:
        if _class['class'][-4:] == 'Test':
            symbol = _class['class'][:-4]
        else:
            symbol = _class['class'] + 'Test'

        locations += window.lookup_symbol_in_index(symbol)

    locations = _unique_lookup_symbols(locations)

    return locations


def find_switchable(view, on_select) -> None:
    window = view.window()

    classes = find_php_classes(view, with_namespace=True)
    debug_message('found %s class(s): %s in %s', len(classes), classes, view.file_name() if view.file_name() else view)

    if not len(classes):
        message('Could not find a class in %s', view.file_name() if view.file_name() else view)
        return

    lookup_symbols = _get_switchable_lookup_symbols(window, classes)
    debug_message('found %s lookup symbol(s): %s', len(lookup_symbols), lookup_symbols)

    if not len(lookup_symbols):
        message('Could not find a switchable for %s', view.file_name() if view.file_name() else view)
        return

    def _on_select(index: int) -> None:
        if index >= 0:
            on_select(Switchable(lookup_symbols[index]))

    if len(lookup_symbols) == 1:
        _on_select(0)
        return

    lookup_symbols, is_exact = _find_switchable_in_lookup_symbols(view.file_name(), lookup_symbols)

    debug_message('found %d lookup symbol(s): %s', len(lookup_symbols), lookup_symbols)

    if is_exact and len(lookup_symbols) == 1:
        return _on_select(0)

    window.show_quick_panel(['{}:{}'.format(loc[1], loc[2][0]) for loc in lookup_symbols], _on_select)


def _unique_lookup_symbols(locations: list) -> list:
    locs = []
    seen = set()  # type: set
    for location in locations:
        if location[0] not in seen:
            seen.add(location[0])
            locs.append(location)

    return locs


def _find_switchable_in_lookup_symbols(file, lookup_symbols: list) -> tuple:
    if not file:
        return lookup_symbols, False

    switchable_targets, switchable_targets_are_tests = _get_switchable_targets(file)

    debug_message('switchable_targets=%s', switchable_targets)

    # print('->', file)
    # print('  switchables:')
    # for f in switchable_targets:
    #     print('  ', f)
    # print('  lookup symbols:')
    # for lookup_symbol in lookup_symbols:
    #     print('  ', lookup_symbol[0], lookup_symbol[1])

    matched_switchables = []
    for switchable_file in switchable_targets:
        for lookup_symbol in lookup_symbols:
            if lookup_symbol[0] == switchable_file:
                matched_switchables.append(lookup_symbol)

    if matched_switchables:
        return (matched_switchables, True if len(matched_switchables) == 1 else False)

    if len(lookup_symbols) > 1:
        common_prefix = os.path.commonprefix([loc[0] for loc in lookup_symbols])
        if common_prefix != '/':
            switchable_targets = [file.replace(common_prefix, '') for file in switchable_targets]

    for location in lookup_symbols:
        loc_file = location[0]
        if not switchable_targets_are_tests:
            loc_file = re.sub('\\/[tT]ests\\/([uU]nit\\/)?', '/', loc_file)

        for file in switchable_targets:
            if loc_file.endswith(file):
                return [location], True

    return lookup_symbols, False


def _get_switchable_targets(file: str) -> tuple:
    switchable_files = []

    if file.endswith('Test.php'):
        is_test = True
        file = file.replace('Test.php', '.php')

        switchable_file = re.sub('(\\/)?[tT]ests\\/([uU]nit\\/)?', '/', file, count=1)
        if switchable_file not in switchable_files:
            switchable_files.append(switchable_file)
        switchable_file = re.sub('(\\/)?[tT]ests\\/Unit/', '/app/', file, count=1)
        if switchable_file not in switchable_files:
            switchable_files.append(switchable_file)
        switchable_file = re.sub('(\\/)?[tT]ests\\/Integration/', '/app/', file, count=1)
        if switchable_file not in switchable_files:
            switchable_files.append(switchable_file)
        switchable_file = re.sub('(\\/)?[tT]ests\\/', '/src/', file, count=1)
        if switchable_file not in switchable_files:
            switchable_files.append(switchable_file)

    else:
        is_test = False
        file = file.replace('.php', 'Test.php')

        # app/
        switchable_file = re.sub('app\\/(?!.*app\\/)', 'tests/', file, count=1)
        if switchable_file not in switchable_files:
            switchable_files.append(switchable_file)
        switchable_file = re.sub('app\\/(?!.*app\\/)', 'tests/Unit/', file, count=1)
        if switchable_file not in switchable_files:
            switchable_files.append(switchable_file)
        switchable_file = re.sub('app\\/(?!.*app\\/)', 'tests/Integration/', file, count=1)
        if switchable_file not in switchable_files:
            switchable_files.append(switchable_file)
        switchable_file = re.sub('app\\/(?!.*app\\/)', '', file, count=1)
        if switchable_file not in switchable_files:
            switchable_files.append(switchable_file)
        switchable_file = re.sub('app\\/(?!.*app\\/)', 'test/', file, count=1)
        if switchable_file not in switchable_files:
            switchable_files.append(switchable_file)

        # src/
        switchable_file = re.sub('(\\/)?src\\/', '/', file, count=1)
        if switchable_file not in switchable_files:
            switchable_files.append(switchable_file)
        switchable_file = re.sub('(\\/)?src\\/', '/test/', file, count=1)
        if switchable_file not in switchable_files:
            switchable_files.append(switchable_file)

    # 1:1
    if file not in switchable_files:
        switchable_files.append(file)

    return switchable_files, is_test


def put_views_side_by_side(view_a, view_b) -> None:
    if view_a == view_b:
        return

    window = view_a.window()

    if window.num_groups() == 1:
        window.run_command('set_layout', {
            "cols": [0.0, 0.5, 1.0],
            "rows": [0.0, 1.0],
            "cells": [[0, 0, 1, 1], [1, 0, 2, 1]]
        })

    view_a_index = window.get_view_index(view_a)
    view_b_index = window.get_view_index(view_b)

    if window.num_groups() <= 2 and view_a_index[0] == view_b_index[0]:

        if view_a_index[0] == 0:
            window.set_view_index(view_b, 1, 0)
        else:
            window.set_view_index(view_b, 0, 0)

        # Ensure focus is not lost from either view.
        window.focus_view(view_a)
        window.focus_view(view_b)


def file_exists_and_is_executable(file: str) -> bool:
    return os.path.isfile(file) and os.access(file, os.X_OK)


def is_valid_php_version_file_version(version: str) -> bool:
    return bool(re.match(
        '^(?:master|[1-9](?:\\.[0-9]+)?(?:snapshot|\\.[0-9]+(?:snapshot)?)|[1-9]\\.x|[1-9]\\.[0-9]+\\.x)$',
        version
    ))


def build_cmd_options(options: dict, cmd: list) -> list:
    for k, v in options.items():
        if v:
            if len(k) == 1:
                if isinstance(v, list):
                    for _v in v:
                        cmd.append('-' + k)
                        cmd.append(_v)
                else:
                    cmd.append('-' + k)
                    if v is not True:
                        cmd.append(v)
            else:
                if k[-1] == '=':
                    cmd.append('--' + k + v)
                else:
                    cmd.append('--' + k)
                    if v is not True:
                        cmd.append(v)

    return cmd


def build_filter_option(view, tests: list) -> str:
    if get_setting(view, 'pest'):
        return '(' + '|'.join(tests) + ')'

    tests_without_test_prefix = [m[4:] for m in tests if m.startswith('test')]

    if len(tests_without_test_prefix) == len(tests):
        tests = tests_without_test_prefix
        f = '::test'
    else:
        f = '::'

    f += '(' + '|'.join(sorted(tests)) + ')( with data set .+)?$'

    return f


def filter_path(path):
    if isinstance(path, list):
        return [filter_path(p) for p in path]

    return os.path.expandvars(os.path.expanduser(path))


def _get_executable(working_dir: str, path: str):
    if platform() == 'windows':
        path += '.bat'

    executable = os.path.join(working_dir, path)

    if file_exists_and_is_executable(executable):
        return executable


def _get_vendor_executable(working_dir: str, name: str) -> str:
    return _get_executable(working_dir, os.path.join('vendor', 'bin', name))


def get_phpunit_executable(view, working_dir: str) -> list:
    executable = get_setting(view, 'executable')
    if executable:
        executable = filter_path(executable)
        return executable if isinstance(executable, list) else [executable]

    if get_setting(view, 'paratest'):
        paratest_executable = _get_vendor_executable(working_dir, 'paratest')
        if paratest_executable:
            return [paratest_executable]

    if get_setting(view, 'artisan'):
        artisan_executable = _get_executable(working_dir, 'artisan')
        if artisan_executable:
            return [artisan_executable, 'test']

    if get_setting(view, 'pest') and get_setting(view, 'composer'):
        pest_executable = _get_vendor_executable(working_dir, 'pest')
        if pest_executable:
            return [pest_executable]

    if get_setting(view, 'composer'):
        executable = _get_vendor_executable(working_dir, 'phpunit')
        if executable:
            return [executable]

    executable = shutil.which('phpunit')
    if executable:
        return [executable]

    raise ValueError('phpunit not found')


def get_php_executable(view, working_dir: str):
    php_versions_path = get_setting(view, 'php_versions_path')
    php_executable = get_setting(view, 'php_executable')
    php_version_file = os.path.join(working_dir, '.php-version')
    if os.path.isfile(php_version_file):
        with open(php_version_file, 'r') as f:
            php_version_number = f.read().strip()

        if not is_valid_php_version_file_version(php_version_number):
            raise ValueError("'%s' file contents is not a valid version number" % php_version_file)

        if not php_versions_path:
            raise ValueError("'phpunit.php_versions_path' is not set")

        php_versions_path = filter_path(php_versions_path)
        if not os.path.isdir(php_versions_path):
            raise ValueError("'phpunit.php_versions_path' '%s' does not exist or is not a valid directory" % php_versions_path)  # noqa: E501

        if platform() == 'windows':
            php_executable = os.path.join(php_versions_path, php_version_number, 'php.exe')
        else:
            php_executable = os.path.join(php_versions_path, php_version_number, 'bin', 'php')

        if not file_exists_and_is_executable(php_executable):
            raise ValueError("php executable '%s' is not an executable file" % php_executable)

        debug_message('using php executable version found in %s', php_version_file)

        return php_executable

    if php_executable:
        php_executable = filter_path(php_executable)
        if not file_exists_and_is_executable(php_executable):
            raise ValueError("'phpunit.php_executable' '%s' is not an executable file" % php_executable)

        return php_executable


def kill_any_running_tests(window) -> None:
    window.run_command('exec', {'kill': True})


def get_osx_term_script_path() -> str:
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
        'bin',
        'osx_iterm')


def save_views(window) -> None:
    for view in window.views():
        if view.is_dirty() and view.file_name():
            view.run_command('save')


def get_phpunit_options(view, options=None) -> dict:
    if options is None:
        options = {}

    session_options = get_session('options')
    debug_message('session options %s', session_options)
    if session_options:
        for k, v in session_options.items():
            if k not in options:
                options[k] = v

    view_options = get_setting(view, 'options')
    debug_message('view options %s', view_options)
    if view_options:
        for k, v in view_options.items():
            if k not in options:
                options[k] = v

    # Workaround some of the color output issues in Pest and Artisan.
    # See https://github.com/pestphp/pest/issues/778
    # See https://github.com/gerardroche/sublime-phpunit/issues/103
    # See https://github.com/gerardroche/sublime-phpunit/issues/102
    # See https://github.com/laravel/framework/issues/46759
    if get_setting(view, 'strategy') in ('sublime', 'basic'):
        if get_setting(view, 'pest') or get_setting(view, 'artisan'):
            options['colors=never'] = True

    debug_message('options %s', options)

    return options


def resolve_working_dir(view, working_dir) -> str:
    if not working_dir:
        working_dir = find_phpunit_working_directory(view.file_name(), view.window().folders())
        if not working_dir:
            raise ValueError('working directory not found')

    if not os.path.isdir(working_dir):
        raise ValueError('working directory does not exist or is not a valid directory')

    return working_dir


def resolve_path_mapping(view, paths: str, command_params: list) -> list:
    path_mappings = get_setting(view, paths)
    if not path_mappings:
        return command_params

    match = _find_matching_path(path_mappings, command_params)
    if match:
        command_params = _apply_path_mapping(match, command_params)

    return command_params


def _find_matching_path(path_mappings: dict, command_params: list):
    for local_path, remote_path in path_mappings.items():
        filtered_local_path = filter_path(local_path)
        for param in command_params:
            if isinstance(param, str) and param.startswith(filtered_local_path):
                return filtered_local_path, remote_path

    return None


def _apply_path_mapping(match: tuple, command_params: list) -> list:
    filtered_local_path, remote_path = match

    def replace_param(param):
        if not isinstance(param, str):
            return param

        if filtered_local_path in param:
            param = param.replace(filtered_local_path, remote_path)

        if '{working_dir}' in param:
            param = param.replace('{working_dir}', remote_path)

        return param

    return [replace_param(param) for param in command_params]


def toggle_on_post_save(view, item: str) -> None:
    on_post_save = view.settings().get('phpunit.on_post_save')
    if not isinstance(on_post_save, list):
        on_post_save = []

    try:
        on_post_save.remove(item)
    except ValueError:
        on_post_save.append(item)

    # If the new value is the same as the user's default then erase the
    # value from the current and let it fallback to the default. This
    # helps prevent confusion when the user modifies their default.
    view.settings().erase('phpunit.on_post_save')
    if on_post_save != view.settings().get('phpunit.on_post_save'):
        view.settings().set('phpunit.on_post_save', on_post_save)
