import re
import os
import shutil

from sublime import active_window
from sublime import cache_path
from sublime import ENCODED_POSITION
from sublime import load_resource
from sublime import platform
from sublime import status_message
from sublime import version
import sublime_plugin


_DEBUG = bool(os.getenv('SUBLIME_PHPUNIT_DEBUG'))


if _DEBUG:
    def debug_message(msg, *args):
        if args:
            msg = msg % args
        print('PHPUnit: ' + msg)
else:  # pragma: no cover
    def debug_message(msg, *args):
        pass


def is_debug(view=None):
    if view:
        phpunit_debug = view.settings().get('phpunit.debug')
        return phpunit_debug or (
            phpunit_debug is not False and
            view.settings().get('debug')
        )
    else:
        return _DEBUG


def get_window_setting(key, default=None, window=None):
    if not window:
        window = active_window()

    if window.settings().has(key):
        return window.settings().get(key)

    view = window.active_view()

    if view and view.settings().has(key):
        return view.settings().get(key)

    return default


def set_window_setting(key, value, window):
    window.settings().set(key, value)


def find_phpunit_configuration_file(file_name, folders):
    """
    Find the first PHPUnit configuration file.

    Finds either phpunit.xml or phpunit.xml.dist, in {file_name} directory or
    the nearest common ancestor directory in {folders}.
    """
    debug_message('@find_phpunit_configuration_file file=\'%s\', folder(s)(%d)=%s', file_name, len(folders) if folders else 0, folders)  # noqa: E501

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

    ancestor_folders = []
    common_prefix = os.path.commonprefix(folders)
    parent = os.path.dirname(file_name)
    while parent not in ancestor_folders and parent.startswith(common_prefix):
        ancestor_folders.append(parent)
        parent = os.path.dirname(parent)

    ancestor_folders.sort(reverse=True)

    debug_message('@find_phpunit_configuration_file found %d common ancestor(s) %s', len(ancestor_folders), ancestor_folders)  # noqa: E501

    candidate_configuration_file_names = ['phpunit.xml', 'phpunit.xml.dist']
    debug_message('@find_phpunit_configuration_file search for configuration files %s', candidate_configuration_file_names)  # noqa: E501
    for folder in ancestor_folders:
        debug_message('@find_phpunit_configuration_file search in \'%s\'', folder)
        for file_name in candidate_configuration_file_names:
            phpunit_configuration_file = os.path.join(folder, file_name)
            if os.path.isfile(phpunit_configuration_file):
                debug_message('@find_phpunit_configuration_file found configuration file \'%s\'', phpunit_configuration_file)  # noqa: E501
                return phpunit_configuration_file

    debug_message('@find_phpunit_configuration_file not found')

    return None


def find_phpunit_working_directory(file_name, folders):
    configuration_file = find_phpunit_configuration_file(file_name, folders)
    if configuration_file:
        return os.path.dirname(configuration_file)


def is_valid_php_identifier(string):
    return re.match('^[a-zA-Z_][a-zA-Z0-9_]*$', string)


def has_test_case(view):
    """Return True if the view contains a valid PHPUnit test case."""
    for php_class in find_php_classes(view):
        if php_class[-4:] == 'Test':
            return True
    return False


def find_php_classes(view):
    """Return list of class names defined in the view."""
    classes = []

    for class_as_region in view.find_by_selector('source.php entity.name.class - meta.use'):
        class_as_string = view.substr(class_as_region)
        if is_valid_php_identifier(class_as_string):
            classes.append(class_as_string)

    # BC: < 3114
    if not classes:  # pragma: no cover
        for class_as_region in view.find_by_selector('source.php entity.name.type.class - meta.use'):
            class_as_string = view.substr(class_as_region)
            if is_valid_php_identifier(class_as_string):
                classes.append(class_as_string)

    return classes


def find_selected_test_methods(view):
    """
    Return a list of selected test method names.

    Return an empty list if no selections found.

    Selection can be anywhere inside one or more test methods.
    """
    method_names = []
    function_areas = view.find_by_selector('meta.function')
    function_regions = view.find_by_selector('entity.name.function')

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

    # BC: < 3114
    if not method_names:  # pragma: no cover
        for region in view.sel():
            word = view.substr(view.word(region))
            if not is_valid_php_identifier(word) or word[:4] != 'test':
                return []

            method_names.append(word)

    return method_names


def find_first_switchable(view):
    """Return first switchable in view; otherwise None."""
    debug_message('@find_first_switchable view=[id=%d,file=%s]', view.id(), view.file_name())

    window = view.window()
    if not window:
        return None

    classes = find_php_classes(view)
    debug_message('@find_first_switchable found %d PHP class(es) %s', len(classes), classes)

    for class_name in classes:
        if class_name[-4:] == "Test":
            lookup_symbol = class_name[:-4]
        else:
            lookup_symbol = class_name + "Test"

        debug_message('@find_first_switchable lookup symbol: \'%s\'', lookup_symbol)

        switchables_in_open_files = window.lookup_symbol_in_open_files(lookup_symbol)
        debug_message('@find_first_switchable found %d symbol(s) in open files %s', len(switchables_in_open_files), switchables_in_open_files)  # noqa: E501
        for open_file in switchables_in_open_files:
            debug_message('@find_first_switchable found symbol in open file %s', open_file)
            return open_file

        switchables_in_index = window.lookup_symbol_in_index(lookup_symbol)
        debug_message('@find_first_switchable found %d symbol(s) in index %s', len(switchables_in_index), switchables_in_index)  # noqa: E501
        for index in switchables_in_index:
            debug_message('@find_first_switchable found symbol in index %s', index)
            return index


def find_first_switchable_file(view):
    """Return first switchable file in view; otherwise None."""
    first_switchable = find_first_switchable(view)
    if not first_switchable:
        return None

    file = first_switchable[0]

    if int(version()) < 3118:
        if platform() == "windows":
            file = re.sub(r"/([A-Za-z])/(.+)", r"\1:/\2", file)
            file = re.sub(r"/", r"\\", file)

    return file


def put_views_side_by_side(view_a, view_b):
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

        # Ensure focus is not
        # lost from either
        # view.
        window.focus_view(view_a)
        window.focus_view(view_b)


def exec_file_regex():
    if platform() == 'windows':
        return '((?:[a-zA-Z]\\:)?\\\\[a-zA-Z0-9 \\.\\/\\\\_-]+)(?: on line |\\:)([0-9]+)'
    else:
        return '(\\/[a-zA-Z0-9 \\.\\/_-]+)(?: on line |\\:)([0-9]+)'


def is_file_executable(file):
    return os.path.isfile(file) and os.access(file, os.X_OK)


def is_valid_php_version_file_version(version):
    return bool(re.match(
        '^(?:master|[1-9]\\.[0-9]+(?:snapshot|\\.[0-9]+(?:snapshot)?)|[1-9]\\.x|[1-9]\\.[0-9]+\\.x)$',
        version
    ))


def build_cmd_options(options, cmd):
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
                cmd.append('--' + k)
                if v is not True:
                    cmd.append(v)

    return cmd


# TODO do we need to optimise the filter pattern?
# TODO should the filter pattern have max size?
def build_filter_option_pattern(list):
    return '::(' + '|'.join(sorted(list)) + ')( with data set .+)?$'


def filter_path(path):
    path = os.path.expanduser(path)
    path = os.path.expandvars(path)
    return path


class PHPUnit():

    def __init__(self, window):
        self.window = window
        self.view = self.window.active_view()
        if not self.view:
            raise ValueError('view not found')

        debug_message('@init view=[id=%d,file=%s]', self.view.id(), self.view.file_name())

    def run(self, working_dir=None, file=None, options=None):
        debug_message('@run working_dir=%s, file=%s, options=%s', working_dir, file, options)

        # Kill any currently running tests
        self.window.run_command('exec', {'kill': True})

        env = {}
        cmd = []

        try:
            if not working_dir:
                working_dir = find_phpunit_working_directory(self.view.file_name(), self.window.folders())
                if not working_dir:
                    raise ValueError('working directory not found')

            if not os.path.isdir(working_dir):
                raise ValueError('working directory does not exist or is not a valid directory')

            debug_message('workingdir = %s', working_dir)

            php_executable = self.get_php_executable(working_dir)
            if php_executable:
                env['PATH'] = os.path.dirname(php_executable) + os.pathsep + os.environ['PATH']
                debug_message('php executable = %s', php_executable)

            phpunit_executable = self.get_phpunit_executable(working_dir)
            cmd.append(phpunit_executable)
            debug_message('executable = %s', phpunit_executable)

            options = self.filter_options(options)
            debug_message('options = %s', options)

            cmd = build_cmd_options(options, cmd)

            if file:
                if os.path.isfile(file):
                    file = os.path.relpath(file, working_dir)
                    cmd.append(file)
                    debug_message('file = %s', file)
                else:
                    raise ValueError('test file \'%s\' not found' % file)

        except ValueError as e:
            status_message('PHPUnit: {}'.format(e))
            print('PHPUnit: {}'.format(e))
            return
        except Exception as e:
            status_message('PHPUnit: {}'.format(e))
            print('PHPUnit: \'{}\''.format(e))
            raise e

        debug_message('env = %s', env)
        debug_message('cmd = %s', cmd)

        if self.view.settings().get('phpunit.save_all_on_run'):
            # Write out every buffer in active
            # window that has changes and is
            # a real file on disk.
            for view in self.window.views():
                if view.is_dirty() and view.file_name():
                    view.run_command('save')

        self.window.run_command('exec', {
            'env': env,
            'cmd': cmd,
            'file_regex': exec_file_regex(),
            'quiet': not is_debug(self.view),
            'shell': False,
            'syntax': 'Packages/phpunitkit/res/text-ui-result.sublime-syntax',
            'word_wrap': False,
            'working_dir': working_dir
        })

        set_window_setting('phpunit._test_last', {
            'working_dir': working_dir,
            'file': file,
            'options': options
        }, window=self.window)

        if self.view.settings().has('phpunit.text_ui_result_font_size'):
            self.window.create_output_panel('exec').settings().set(
                'font_size',
                self.view.settings().get('phpunit.text_ui_result_font_size')
            )

        # BC: to be removed in v3.0.0
        # Custom color schemes are deprecated and will
        # be removed in v3.0.0. Instead, a definitive
        # syntax for test results panels will be
        # written and popular color schemes will
        # be asked to support it. See the issue
        # tracker for more details.
        if self.view.settings().has('phpunit.color_scheme'):
            color_scheme = self.view.settings().get('phpunit.color_scheme')
            if color_scheme:
                color_scheme = color_scheme.replace('Packages/phpunitkit/color-schemes/', 'Packages/phpunitkit/res/')
            else:
                color_scheme = self.view.settings().get('color_scheme')
        else:
            color_scheme = self.get_auto_generated_color_scheme()
        self.window.create_output_panel('exec').settings().set('color_scheme', color_scheme)

    def run_last(self):
        kwargs = get_window_setting('phpunit._test_last', window=self.window)
        if kwargs:
            self.run(**kwargs)
        else:
            return status_message('PHPUnit: no tests were run so far')

    def run_file(self):
        file = self.view.file_name()
        if file:
            if has_test_case(self.view):
                self.run(file=file)
            else:
                self.run(file=find_first_switchable_file(self.view))
        else:
            return status_message('PHPUnit: not a test file')

    def run_nearest(self):
        options = {}

        if has_test_case(self.view):
            unit_test = self.view.file_name()
            selected_test_methods = find_selected_test_methods(self.view)
            if selected_test_methods:
                debug_message('found test selections: %s', selected_test_methods)
                options = {'filter': build_filter_option_pattern(selected_test_methods)}
        else:
            debug_message('current file is not a test file')
            unit_test = find_first_switchable_file(self.view)

        if unit_test:
            self.run(file=unit_test, options=options)
        else:
            return status_message('PHPUnit: not a test file')

    def results(self):
        self.window.run_command('show_panel', {'panel': 'output.exec'})

    def cancel(self):
        self.window.run_command('exec', {'kill': True})

    def toggle(self, option):
        options = get_window_setting('phpunit.options', default={}, window=self.window)
        options[option] = not bool(options[option]) if option in options else True
        set_window_setting('phpunit.options', options, window=self.window)

    def filter_options(self, options):
        if options is None:
            options = {}

        window_options = get_window_setting('phpunit.options', default={}, window=self.window)
        if window_options:
            for k, v in window_options.items():
                if k not in options:
                    options[k] = v

        view_options = self.view.settings().get('phpunit.options')
        if view_options:
            for k, v in view_options.items():
                if k not in options:
                    options[k] = v

        return options

    def get_php_executable(self, working_dir):
        php_version_file = os.path.join(working_dir, '.php-version')
        if os.path.isfile(php_version_file):
            with open(php_version_file, 'r') as f:
                php_version_number = f.read().strip()

            if not is_valid_php_version_file_version(php_version_number):
                raise ValueError("'%s' file contents is not a valid version number" % php_version_file)

            php_versions_path = self.view.settings().get('phpunit.php_versions_path')
            if not php_versions_path:
                raise ValueError("'phpunit.php_versions_path' is not set")

            php_versions_path = filter_path(php_versions_path)
            if not os.path.isdir(php_versions_path):
                raise ValueError("'phpunit.php_versions_path' '%s' does not exist or is not a valid directory" % php_versions_path)  # noqa: E501

            if platform() == 'windows':
                php_executable = os.path.join(php_versions_path, php_version_number, 'php.exe')
            else:
                php_executable = os.path.join(php_versions_path, php_version_number, 'bin', 'php')

            if not is_file_executable(php_executable):
                raise ValueError("php executable '%s' is not an executable file" % php_executable)

            return php_executable

        php_executable = self.view.settings().get('phpunit.php_executable')
        if php_executable:
            php_executable = filter_path(php_executable)
            if not is_file_executable(php_executable):
                raise ValueError("'phpunit.php_executable' '%s' is not an executable file" % php_executable)

            return php_executable

    def get_phpunit_executable(self, working_dir):
        if platform() == 'windows':
            composer_phpunit_executable = os.path.join(working_dir, os.path.join('vendor', 'bin', 'phpunit.bat'))
        else:
            composer_phpunit_executable = os.path.join(working_dir, os.path.join('vendor', 'bin', 'phpunit'))

        if self.view.settings().get('phpunit.composer') and is_file_executable(composer_phpunit_executable):
            return composer_phpunit_executable
        else:
            executable = shutil.which('phpunit')
            if executable:
                return executable
            else:
                raise ValueError('phpunit not found')

    def get_auto_generated_color_scheme(self):
        color_scheme = self.view.settings().get('color_scheme')
        debug_message('color scheme \'{}\''.format(color_scheme))

        if color_scheme.endswith('.sublime-color-scheme'):
            return color_scheme

        try:
            # Try to patch color scheme with default test result colors

            color_scheme_resource = load_resource(color_scheme)
            if 'phpunitkit' in color_scheme_resource or 'region.greenish' in color_scheme_resource:
                debug_message('color looks like it has color support')
                return color_scheme

            cs_head, cs_tail = os.path.split(color_scheme)
            cs_package = os.path.split(cs_head)[1]
            cs_name = os.path.splitext(cs_tail)[0]

            file_name = cs_package + '__' + cs_name + '.hidden-tmTheme'
            abs_file = os.path.join(cache_path(), 'phpunitkit', 'color-schemes', file_name)
            rel_file = 'Cache/phpunitkit/color-schemes/' + file_name

            debug_message('auto generated color scheme = %s', rel_file)

            if not os.path.exists(os.path.dirname(abs_file)):
                os.makedirs(os.path.dirname(abs_file))

            color_scheme_resource_partial = load_resource('Packages/phpunitkit/res/text-ui-result-theme-partial.txt')
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


class PhpunitTestSuiteCommand(sublime_plugin.WindowCommand):

    def run(self):
        PHPUnit(self.window).run()


class PhpunitTestFileCommand(sublime_plugin.WindowCommand):

    def run(self):
        PHPUnit(self.window).run_file()


class PhpunitTestLastCommand(sublime_plugin.WindowCommand):

    def run(self):
        PHPUnit(self.window).run_last()


class PhpunitTestNearestCommand(sublime_plugin.WindowCommand):

    def run(self):
        PHPUnit(self.window).run_nearest()


class PhpunitTestResultsCommand(sublime_plugin.WindowCommand):

    def run(self):
        PHPUnit(self.window).results()


class PhpunitTestCancelCommand(sublime_plugin.WindowCommand):

    def run(self):
        PHPUnit(self.window).cancel()


class PhpunitTestVisitCommand(sublime_plugin.WindowCommand):

    def run(self):
        test_last = get_window_setting('phpunit._test_last', window=self.window)
        if test_last:
            if 'file' in test_last and 'working_dir' in test_last:
                if test_last['file']:
                    file = os.path.join(test_last['working_dir'], test_last['file'])
                    if os.path.isfile(file):
                        return self.window.open_file(file)

        return status_message('PHPUnit: no tests were run so far')


class PhpunitTestSwitchCommand(sublime_plugin.WindowCommand):

    def run(self):
        view = self.window.active_view()
        if not view:
            return status_message('PHPUnit: view not found')

        first_switchable = find_first_switchable(view)
        if not first_switchable:
            return status_message('PHPUnit: no switchable found')

        self.window.open_file(first_switchable[0] + ':' + str(first_switchable[2][0]), ENCODED_POSITION)
        debug_message('@run switch from \'%s\' to \'%s\'', view.file_name(), first_switchable)
        put_views_side_by_side(view, self.window.active_view())


class PhpunitToggleOptionCommand(sublime_plugin.WindowCommand):

    def run(self, option):
        PHPUnit(self.window).toggle(option)


class PhpunitTestCoverageCommand(sublime_plugin.WindowCommand):

    def run(self):
        view = self.window.active_view()
        if not view:
            return

        working_dir = find_phpunit_working_directory(view.file_name(), self.window.folders())
        if not working_dir:
            return status_message('PHPUnit: could not find a PHPUnit working directory')

        coverage_html_index_html_file = os.path.join(working_dir, 'build/coverage/index.html')
        if not os.path.exists(coverage_html_index_html_file):
            return status_message('PHPUnit: could not find PHPUnit HTML code coverage %s' % coverage_html_index_html_file)  # noqa: E501

        import webbrowser
        webbrowser.open_new_tab('file://' + coverage_html_index_html_file)


# DEPRECATED: to be removed in v3.0.0; use :TestSwitchCommand instead
class PhpunitSwitchFile(sublime_plugin.WindowCommand):

    def run(self):
        print('PHPUnit: DEPRECATED :SwitchFile; please use :TestSwitch instead')
        self.window.run_command('phpunit_test_switch')


# DEPRECATED: to be removed in v3.0.0; use :TestCoverageCommand instead
class PhpunitOpenCodeCoverageCommand(sublime_plugin.WindowCommand):

    def run(self):
        print('PHPUnit: DEPRECATED :OpenCodeCoverage; please use :TestCoverage instead')
        self.window.run_command('phpunit_test_coverage')
