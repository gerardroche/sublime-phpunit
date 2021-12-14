import re
import os
import shutil

from sublime import ENCODED_POSITION
from sublime import active_window
from sublime import cache_path
from sublime import load_resource
from sublime import platform
from sublime import status_message
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


def message(msg, *args):
    if args:
        msg = msg % args

    msg = 'PHPUnit: ' + msg

    print(msg)
    status_message(msg)


def is_debug(view=None):
    if view:
        phpunit_debug = view.settings().get('phpunit.debug')
        return phpunit_debug or (
            phpunit_debug is not False and view.settings().get('debug')
        )
    else:
        return _DEBUG


def get_active_view(window):
    active_view = window.active_view()

    if not active_view:
        raise ValueError('view not found')

    return active_view


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

    candidate_configuration_file_names = ['phpunit.xml', 'phpunit.xml.dist']
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


def is_valid_php_identifier(string):
    return re.match('^[a-zA-Z_][a-zA-Z0-9_]*$', string)


def has_test_case(view):
    """Return True if the view contains a valid PHPUnit test case."""
    for php_class in find_php_classes(view):
        if php_class[-4:] == 'Test':
            return True
    return False


def find_php_classes(view, with_namespace=False):
    """Return list of class names defined in the view."""
    classes = []

    namespace = None
    for namespace_region in view.find_by_selector('source.php entity.name.namespace'):
        namespace = view.substr(namespace_region)
        break  # TODO handle files with multiple namespaces

    for class_as_region in view.find_by_selector('source.php entity.name.class - meta.use'):
        class_as_string = view.substr(class_as_region)
        if is_valid_php_identifier(class_as_string):
            if with_namespace:
                classes.append({
                    'namespace': namespace,
                    'class': class_as_string
                })
            else:
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

    # BC: < 3114
    if not method_names:  # pragma: no cover
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


def refine_switchable_locations(locations, file):
    debug_message('refine location')
    if not file:
        return locations, False

    debug_message('file=%s', file)
    debug_message('locations=%s', locations)

    files = []
    if file.endswith('Test.php'):
        file_is_test_case = True
        file = file.replace('Test.php', '.php')
        files.append(re.sub('(\\/)?[tT]ests\\/([uU]nit\\/)?', '/', file))
        files.append(re.sub('(\\/)?[tT]ests\\/', '/src/', file))
    else:
        file_is_test_case = False
        file = file.replace('.php', 'Test.php')
        files.append(file)
        files.append(re.sub('(\\/)?src\\/', '/', file))
        files.append(re.sub('(\\/)?src\\/', '/test/', file))

    debug_message('files=%s', files)

    if len(locations) > 1:
        common_prefix = os.path.commonprefix([loc[0] for loc in locations])
        if common_prefix != '/':
            files = [file.replace(common_prefix, '') for file in files]

    for location in locations:
        loc_file = location[0]
        if not file_is_test_case:
            loc_file = re.sub('\\/[tT]ests\\/([uU]nit\\/)?', '/', loc_file)

        for file in files:
            if loc_file.endswith(file):
                return [location], True

    return locations, False


def find_switchable(view, on_select=None):
    # Args:
    #   view (View)
    #   on_select (callable)
    #
    # Returns:
    #   void
    window = view.window()

    if on_select is None:
        raise ValueError('a callable is required')

    file = view.file_name()
    debug_message('file=%s', file)

    classes = find_php_classes(view, with_namespace=True)
    if len(classes) == 0:
        return message('could not find a test case or class under test for %s', file)

    debug_message('file contains %s class %s', len(classes), classes)

    locations = []  # type: list
    for _class in classes:
        class_name = _class['class']

        if class_name[-4:] == 'Test':
            symbol = class_name[:-4]
        else:
            symbol = class_name + 'Test'

        symbol_locations = window.lookup_symbol_in_index(symbol)
        locations += symbol_locations

    debug_message('class has %s location %s', len(locations), locations)

    def unique_locations(locations):
        locs = []
        seen = set()  # type: set
        for location in locations:
            if location[0] not in seen:
                seen.add(location[0])
                locs.append(location)

        return locs

    locations = unique_locations(locations)

    if len(locations) == 0:
        if has_test_case(view):
            return message('could not find class under test for %s', file)
        else:
            return message('could not find test case for %s', file)

    def _on_select(index):
        if index == -1:
            return

        switchable = Switchable(locations[index])

        if on_select is not None:
            on_select(switchable)

    locations, is_exact = refine_switchable_locations(locations=locations, file=file)

    debug_message('is_exact=%s', is_exact)
    debug_message('locations(%s)=%s', len(locations), locations)

    if is_exact and len(locations) == 1:
        return _on_select(0)

    window.show_quick_panel(['{}:{}'.format(loc[1], loc[2][0]) for loc in locations], _on_select)


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

        # Ensure focus is not lost from either view.
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
        '^(?:master|[1-9](?:\\.[0-9]+)?(?:snapshot|\\.[0-9]+(?:snapshot)?)|[1-9]\\.x|[1-9]\\.[0-9]+\\.x)$',
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
                if k[-1] == '=':
                    cmd.append('--' + k + v)
                else:
                    cmd.append('--' + k)
                    if v is not True:
                        cmd.append(v)

    return cmd


def build_filter_option_pattern(methods):
    test_methods = [m[4:] for m in methods if m.startswith('test')]

    if len(test_methods) == len(methods):
        methods = test_methods
        f = '::test'
    else:
        f = '::'

    f += '(' + '|'.join(sorted(methods)) + ')( with data set .+)?$'

    return f


def filter_path(path):
    return os.path.expandvars(os.path.expanduser(path))


def _get_phpunit_executable(working_dir, include_composer_vendor_dir=True):
    debug_message('find phpunit executable composer=%s', include_composer_vendor_dir)
    if include_composer_vendor_dir:
        if platform() == 'windows':
            composer_phpunit_executable = os.path.join(working_dir, os.path.join('vendor', 'bin', 'phpunit.bat'))
            debug_message('  found \'%s\' (windows)', composer_phpunit_executable)
        else:
            composer_phpunit_executable = os.path.join(working_dir, os.path.join('vendor', 'bin', 'phpunit'))
            debug_message('  found \'%s\' (unix)', composer_phpunit_executable)

        if is_file_executable(composer_phpunit_executable):
            return composer_phpunit_executable

        debug_message('  Warning: \'%s\' is not executable!', composer_phpunit_executable)

    executable = shutil.which('phpunit')
    debug_message('  found \'%s\' (global)', executable)
    if executable:
        return executable
    else:
        raise ValueError('phpunit not found')


def _get_php_executable(working_dir, php_versions_path, php_executable=None):
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

        if not is_file_executable(php_executable):
            raise ValueError("php executable '%s' is not an executable file" % php_executable)

        return php_executable

    if php_executable:
        php_executable = filter_path(php_executable)
        if not is_file_executable(php_executable):
            raise ValueError("'phpunit.php_executable' '%s' is not an executable file" % php_executable)

        return php_executable


def kill_any_running_tests(window) -> None:
    window.run_command('exec', {'kill': True})


class PHPUnit():

    def __init__(self, window):
        self.window = window
        self.view = get_active_view(window)
        debug_message('init %s', None)

    def run(self, working_dir=None, file=None, options=None):
        debug_message('run working_dir=%s, file=%s, options=%s', working_dir, file, options)

        kill_any_running_tests(self.window)

        env = {}

        try:
            working_dir = self.get_working_dir(working_dir)
            php_executable = self.get_php_executable(working_dir)

            if php_executable:
                env['PATH'] = os.path.dirname(php_executable) + os.pathsep + os.environ['PATH']

            phpunit_executable = self.get_phpunit_executable(working_dir)

            options = self.filter_options(options)

            cmd = []
            cmd.append(phpunit_executable)
            cmd = build_cmd_options(options, cmd)

            if file:
                if os.path.isfile(file):
                    file = os.path.relpath(file, working_dir)
                    cmd.append(file)
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

        debug_message(
            '*** Configuration ***\n  working dir: %s\n  php: %s\n  phpunit: %s\n  options: %s\n  env: %s\n  cmd: %s',
            working_dir,
            php_executable,
            phpunit_executable,
            options,
            env,
            cmd
        )

        if self.view.settings().get('phpunit.save_all_on_run'):
            # Write out every buffer in active
            # window that has changes and is
            # a real file on disk.
            for view in self.window.views():
                if view.is_dirty() and view.file_name():
                    view.run_command('save')

        set_window_setting('phpunit._test_last', {
            'working_dir': working_dir,
            'file': file,
            'options': options
        }, window=self.window)

        if self.view.settings().get('phpunit.strategy') == 'iterm':
            osx_iterm_script = os.path.join(
                os.path.dirname(os.path.realpath(__file__)), 'bin', 'osx_iterm')

            cmd = [osx_iterm_script] + cmd

            self.window.run_command('exec', {
                'env': env,
                'cmd': cmd,
                'quiet': not is_debug(self.view),
                'shell': False,
                'working_dir': working_dir
            })
        else:
            self.window.run_command('exec', {
                'env': env,
                'cmd': cmd,
                'file_regex': exec_file_regex(),
                'quiet': not is_debug(self.view),
                'shell': False,
                'syntax': 'Packages/{}/res/text-ui-result.sublime-syntax'.format(__name__.split('.')[0]),
                'word_wrap': False,
                'working_dir': working_dir
            })

            panel = self.window.create_output_panel('exec')

            header_text = []
            if env:
                header_text.append("env: {}\n".format(env))

            header_text.append("{}\n\n".format(' '.join(cmd)))

            panel.run_command('insert', {'characters': ''.join(header_text)})

            panel_settings = panel.settings()
            panel_settings.set('rulers', [])
            panel_settings.set('highlight_line', False)

            if self.view.settings().has('phpunit.text_ui_result_font_size'):
                panel_settings.set(
                    'font_size',
                    self.view.settings().get('phpunit.text_ui_result_font_size')
                )

            color_scheme = self.get_auto_generated_color_scheme()
            panel_settings.set('color_scheme', color_scheme)

    def get_working_dir(self, working_dir) -> str:
        if not working_dir:
            working_dir = find_phpunit_working_directory(self.view.file_name(), self.window.folders())
            if not working_dir:
                raise ValueError('working directory not found')

        if not os.path.isdir(working_dir):
            raise ValueError('working directory does not exist or is not a valid directory')

        return working_dir

    def run_last(self):
        last_test_args = get_window_setting('phpunit._test_last', window=self.window)
        if not last_test_args:
            return status_message('PHPUnit: no tests were run so far')

        self.run(**last_test_args)

    def run_file(self, options=None):
        if options is None:
            options = {}

        file = self.view.file_name()
        if not file:
            return status_message('PHPUnit: not a test file')

        if has_test_case(self.view):
            self.run(file=file, options=options)
        else:
            find_switchable(
                self.view,
                on_select=lambda switchable: self.run(
                    file=switchable.file,
                    options=options
                )
            )

    def run_nearest(self, options):
        file = self.view.file_name()
        if not file:
            return status_message('PHPUnit: not a test file')

        if has_test_case(self.view):
            if 'filter' not in options:
                selected_test_methods = find_selected_test_methods(self.view)
                if selected_test_methods:
                    options['filter'] = build_filter_option_pattern(selected_test_methods)

            self.run(file=file, options=options)
        else:
            find_switchable(
                self.view,
                on_select=lambda switchable: self.run(
                    file=switchable.file,
                    options=options
                )
            )

    def show_results(self):
        self.window.run_command('show_panel', {'panel': 'output.exec'})

    def cancel(self):
        self.window.run_command('exec', {'kill': True})

    def open_coverage_report(self):
        working_dir = find_phpunit_working_directory(self.view.file_name(), self.window.folders())
        if not working_dir:
            return status_message('PHPUnit: could not find a PHPUnit working directory')

        coverage_html_index_html_file = os.path.join(working_dir, 'build/coverage/index.html')
        if not os.path.exists(coverage_html_index_html_file):
            return status_message('PHPUnit: could not find PHPUnit HTML code coverage %s' % coverage_html_index_html_file)  # noqa: E501

        import webbrowser
        webbrowser.open_new_tab('file://' + coverage_html_index_html_file)

    def switch(self):
        def _on_switchable(switchable):
            self.window.open_file(switchable.file_encoded_position(self.view), ENCODED_POSITION)
            put_views_side_by_side(self.view, self.window.active_view())

        find_switchable(self.view, on_select=_on_switchable)

    def visit(self):
        test_last = get_window_setting('phpunit._test_last', window=self.window)
        if test_last:
            if 'file' in test_last and 'working_dir' in test_last:
                if test_last['file']:
                    file = os.path.join(test_last['working_dir'], test_last['file'])
                    if os.path.isfile(file):
                        return self.window.open_file(file)

        return status_message('PHPUnit: no tests were run so far')

    def toggle_option(self, option, value=None):
        options = get_window_setting('phpunit.options', default={}, window=self.window)

        if value is None:
            options[option] = not bool(options[option]) if option in options else True
        else:
            if option in options and options[option] == value:
                del options[option]
            else:
                options[option] = value

        set_window_setting('phpunit.options', options, window=self.window)

    def filter_options(self, options):
        if options is None:
            options = {}

        window_options = get_window_setting('phpunit.options', default={}, window=self.window)
        debug_message('window options %s', window_options)
        if window_options:
            for k, v in window_options.items():
                if k not in options:
                    options[k] = v

        view_options = self.view.settings().get('phpunit.options')
        debug_message('view options %s', view_options)
        if view_options:
            for k, v in view_options.items():
                if k not in options:
                    options[k] = v

        return options

    def get_php_executable(self, working_dir):
        versions_path = self.view.settings().get('phpunit.php_versions_path')
        executable = self.view.settings().get('phpunit.php_executable')

        return _get_php_executable(working_dir, versions_path, executable)

    def get_phpunit_executable(self, working_dir):
        composer = self.view.settings().get('phpunit.composer')
        debug_message('phpunit.composer: %s', composer)

        executable = self.view.settings().get('phpunit.executable')
        if executable:
            executable = filter_path(executable)
            debug_message('phpunit.executable: %s', executable)
            return executable

        return _get_phpunit_executable(working_dir, composer)

    def get_auto_generated_color_scheme(self):
        """Try to patch color scheme with default test result colors."""
        color_scheme = self.view.settings().get('color_scheme')
        if color_scheme.endswith('.sublime-color-scheme'):
            return color_scheme

        try:
            color_scheme_resource = load_resource(color_scheme)
            if 'phpunitkit' in color_scheme_resource or 'PHPUnitKit' in color_scheme_resource:
                return color_scheme

            if 'region.greenish' in color_scheme_resource:
                return color_scheme

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


class PhpunitTestSuiteCommand(sublime_plugin.WindowCommand):

    def run(self, **kwargs):
        PHPUnit(self.window).run(options=kwargs)


class PhpunitTestFileCommand(sublime_plugin.WindowCommand):

    def run(self, **kwargs):
        PHPUnit(self.window).run_file(options=kwargs)


class PhpunitTestLastCommand(sublime_plugin.WindowCommand):

    def run(self):
        PHPUnit(self.window).run_last()


class PhpunitTestNearestCommand(sublime_plugin.WindowCommand):

    def run(self, **kwargs):
        PHPUnit(self.window).run_nearest(options=kwargs)


class PhpunitTestResultsCommand(sublime_plugin.WindowCommand):

    def run(self):
        PHPUnit(self.window).show_results()


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
        PHPUnit(self.window).toggle_option(option, value)


class PhpunitTestCoverageCommand(sublime_plugin.WindowCommand):

    def run(self):
        PHPUnit(self.window).open_coverage_report()


class PhpunitEvents(sublime_plugin.EventListener):

    def on_post_save(self, view):
        file_name = view.file_name()
        if not file_name:
            return

        if not file_name.endswith('.php'):
            return

        on_post_save_events = view.settings().get('phpunit.on_post_save')

        if 'run_test_file' in on_post_save_events:
            PHPUnit(view.window()).run_file()
