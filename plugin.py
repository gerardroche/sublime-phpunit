import re
import os
import shutil


import sublime
import sublime_plugin


DEBUG = bool(os.getenv('SUBLIME_PHPUNIT_DEBUG'))

if DEBUG:
    def debug_message(msg):
        print('PHPUnit: %s' % str(msg))
else:
    def debug_message(msg):
        pass


def is_debug(view=None):
    if view is not None:
        return view.settings().get('phpunit.debug') or (view.settings().get('debug') and view.settings().get('phpunit.debug') is not False)
    else:
        return DEBUG


def get_window_setting(key, default=None, window=None):
    if not window:
        window = sublime.active_window()

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
    Find the first PHPUnit configuration file, either phpunit.xml or
    phpunit.xml.dist, in {file_name} directory or the nearest common ancestor
    directory in {folders}.
    """
    debug_message('Find PHPUnit configuration file for %s in %s (%d)' % (file_name, folders, len(folders) if folders else 0))

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

    debug_message('  Found %d common ancestor folder%s %s' % (len(ancestor_folders), '' if len(ancestor_folders) == 1 else 's', ancestor_folders))

    for folder in ancestor_folders:
        debug_message('    Searching folder: %s' % folder)
        for file_name in ['phpunit.xml', 'phpunit.xml.dist']:
            phpunit_configuration_file = os.path.join(folder, file_name)
            debug_message('     Checking: %s' % phpunit_configuration_file)
            if os.path.isfile(phpunit_configuration_file):
                debug_message('  Found PHPUnit configuration file: %s' % phpunit_configuration_file)
                return phpunit_configuration_file

    debug_message('  PHPUnit Configuration file not found')

    return None


def find_phpunit_working_directory(file_name, folders):
    configuration_file = find_phpunit_configuration_file(file_name, folders)
    if configuration_file:
        return os.path.dirname(configuration_file)
    return None


def is_valid_php_identifier(string):
    return re.match('^[a-zA-Z_][a-zA-Z0-9_]*$', string)


def has_test_case(view):
    """True if the view contains a valid PHPUnit test case."""
    for php_class in find_php_classes(view):
        if php_class[-4:] == 'Test':
            return True
    return False


def find_php_classes(view):
    """Returns an array of classes (class names) defined in the view."""
    classes = []

    for class_as_region in view.find_by_selector('source.php entity.name.type.class - meta.use'):
        class_as_string = view.substr(class_as_region)
        if is_valid_php_identifier(class_as_string):
            classes.append(class_as_string)

    # Quick fix for ST build >= 3114 because the default PHP package changed the
    # scope on class entities.
    if not classes:
        for class_as_region in view.find_by_selector('source.php entity.name.class - meta.use'):
            class_as_string = view.substr(class_as_region)
            if is_valid_php_identifier(class_as_string):
                classes.append(class_as_string)

    return classes


def find_first_switchable(view):
    """Returns the first switchable; otherwise None."""
    debug_message('find_first_switchable(view = %s:%s)' % (view, view.file_name()))

    window = view.window()
    if not window:
        return None

    classes = find_php_classes(view)
    debug_message('Found %d PHP class%s %s in %s' % (len(classes), '' if len(classes) == 1 else 'es', classes, view.file_name()))

    for class_name in classes:
        if class_name[-4:] == "Test":
            lookup_symbol = class_name[:-4]
        else:
            lookup_symbol = class_name + "Test"

        debug_message('    Switchable symbol: %s' % lookup_symbol)

        switchables_in_open_files = window.lookup_symbol_in_open_files(lookup_symbol)
        switchables_in_index = window.lookup_symbol_in_index(lookup_symbol)

        debug_message('      Found %d switchable symbol(s) in open files %s' % (len(switchables_in_open_files), str(switchables_in_open_files)))
        debug_message('      Found %d switchable symbol(s) in index      %s' % (len(switchables_in_index), str(switchables_in_index)))

        for open_file in switchables_in_open_files:
            debug_message('  Found switchable symbol in open file %s' % str(open_file))
            return open_file

        for index in switchables_in_index:
            debug_message('  Found switchable symbol in index %s' % str(index))
            return index


def find_first_switchable_file(view):
    """Returns the first switchable file; otherwise None."""
    first_switchable = find_first_switchable(view)
    if not first_switchable:
        return None

    file = first_switchable[0]

    if int(sublime.version()) < 3118:
        if sublime.platform() == "windows":
            file = re.sub(r"/([A-Za-z])/(.+)", r"\1:/\2", file)
            file = re.sub(r"/", r"\\", file)

    return file


def exec_file_regex():
    if sublime.platform() == 'windows':
        return '((?:[a-zA-Z]\:)?\\\\[a-zA-Z0-9 \\.\\/\\\\_-]+)(?: on line |\:)([0-9]+)'
    else:
        return '(\\/[a-zA-Z0-9 \\.\\/_-]+)(?: on line |\:)([0-9]+)'


def is_file_executable(file):
    return os.path.isfile(file) and os.access(file, os.X_OK)


def is_valid_php_version_file_version(version):
    return bool(re.match('^(?:master|[1-9]\.[0-9]+(?:snapshot|\.[0-9]+(?:snapshot)?)|[1-9]\.x|[1-9]\.[0-9]+\.x)$', version))


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

    def run(self, working_dir=None, file=None, options=None):
        debug_message('running with (working_dir={}, file={}, options={})'.format(working_dir, file, options))

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

            debug_message('working dir = %s' % working_dir)

            php_executable = self.get_php_executable(working_dir)
            if php_executable:
                env['PATH'] = os.path.dirname(php_executable) + os.pathsep + os.environ['PATH']
                debug_message('php executable = %s' % php_executable)

            phpunit_executable = self.get_phpunit_executable(working_dir)
            cmd.append(phpunit_executable)
            debug_message('phpunit executable = %s' % phpunit_executable)

            options = self.filter_options(options)
            debug_message('options = %s' % options)

            cmd = build_cmd_options(options, cmd)

            if file:
                if os.path.isfile(file):
                    file = os.path.relpath(file, working_dir)
                    cmd.append(file)
                    debug_message('file = %s' % file)
                else:
                    raise ValueError("test file '%s' not found" % file)

        except Exception as e:
            print('PHPUnit: {}'.format(e))
            return sublime.status_message(str(e))

        debug_message('env = %s' % env)
        debug_message('cmd = %s' % cmd)

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
            'syntax': 'Packages/phpunitkit/test-results.hidden-tmLanguage',
            'word_wrap': False,
            'working_dir': working_dir
        })

        set_window_setting('phpunit._test_last', {
            'working_dir': working_dir,
            'file': file,
            'options': options
        }, window=self.window)

        if self.view.settings().get('phpunit.color_scheme'):
            color_scheme = self.view.settings().get('phpunit.color_scheme')
        else:
            color_scheme = self.view.settings().get('color_scheme')

        self.window.create_output_panel('exec').settings().set('color_scheme', color_scheme)

    def run_last(self):
        kwargs = get_window_setting('phpunit._test_last', window=self.window)
        if kwargs:
            self.run(**kwargs)

    def run_file(self):
        file = self.view.file_name()
        if not file:
            return

        self.run(file=file)

    def filter_options(self, options):
        if options is None:
            options = {}

        for k, v in get_window_setting('phpunit.options', default={}, window=self.window).items():
            if k not in options:
                options[k] = v

        for k, v in self.view.settings().get('phpunit.options').items():
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
                raise ValueError("'phpunit.php_versions_path' '%s' does not exist or is not a valid directory" % php_versions_path)

            if sublime.platform() == 'windows':
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

        return None

    def get_phpunit_executable(self, working_dir):
        if sublime.platform() == 'windows':
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
        view = self.window.active_view()
        if not view:
            return

        if has_test_case(view):
            debug_message('Found test case in %s' % view.file_name())

            unit_test = view.file_name()
            options = {}

            unit_test_method_names = self.selected_unit_test_method_names(view)
            debug_message('Test method selections: %s' % unit_test_method_names)
            if unit_test_method_names:
                options = {
                    # @todo optimise filter regex; possibly limit the size of the regex too
                    'filter': '::(' + '|'.join(unit_test_method_names) + ')( with data set .+)?$'
                }
        else:
            debug_message('No test case found in %s' % view.file_name())

            unit_test = find_first_switchable_file(view)
            options = {}
            # @todo how to check that the switchable contains a testcase?

        if not unit_test:
            debug_message('Could not find a PHPUnit test case or a switchable test case')
            return

        PHPUnit(self.window).run(file=unit_test, options=options)

    def selected_unit_test_method_names(self, view):
        """
        Returns an array of selected test method names.
        Selection can be anywhere inside one or more test methods.
        If no selection is found inside any test method, then all test method names are returned.
        """

        method_names = []
        function_areas = view.find_by_selector('meta.function')
        function_regions = view.find_by_selector('entity.name.function')

        for region in view.sel():
            for i, area in enumerate(function_areas):
                if not area.a <= region.a <= area.b:
                    continue
                if not i in function_regions and not area.intersects(function_regions[i]):
                    continue
                word = view.substr(function_regions[i])
                if is_valid_php_identifier(word):
                    method_names.append(word)
                break

        # fallback
        if not method_names:
            for region in view.sel():
                word = view.substr(view.word(region))
                if not is_valid_php_identifier(word) or word[:4] != 'test':
                    return None
                method_names.append(word)

        return method_names


class PhpunitSwitchFile(sublime_plugin.WindowCommand):

    def run(self):
        current_view = self.window.active_view()
        if not current_view:
            return

        first_switchable = find_first_switchable(current_view)
        if not first_switchable:
            sublime.status_message('No PHPUnit switchable found for "%s"' % current_view.file_name())
            return

        debug_message('Switching from %s to %s' % (current_view.file_name(), first_switchable))

        self.window.open_file(first_switchable[0])
        switched_view = self.window.active_view()

        if current_view == switched_view: # looks like the class and test-case are in the same view
            return

        # split in two with test case and class under test side-by-side

        if self.window.num_groups() == 1:
            self.window.run_command('set_layout', {
                "cols": [0.0, 0.5, 1.0],
                "rows": [0.0, 1.0],
                "cells": [[0, 0, 1, 1], [1, 0, 2, 1]]
            })

        current_view_index = self.window.get_view_index(current_view)
        switched_view_index = self.window.get_view_index(switched_view)

        if self.window.num_groups() <= 2 and current_view_index[0] == switched_view_index[0]:

            if current_view_index[0] == 0:
                self.window.set_view_index(switched_view, 1, 0)
            else:
                self.window.set_view_index(switched_view, 0, 0)

            # ensure focus is not lost from either view
            self.window.focus_view(current_view)
            self.window.focus_view(switched_view)


class PhpunitToggleOptionCommand(sublime_plugin.WindowCommand):

    def run(self, option):
        options = get_window_setting('phpunit.options', default={}, window=self.window)
        options[option] = not bool(options[option]) if option in options else True
        set_window_setting('phpunit.options', options, window=self.window)


class PhpunitOpenCodeCoverageCommand(sublime_plugin.WindowCommand):

    def run(self):
        view = self.window.active_view()
        if not view:
            return

        working_dir = find_phpunit_working_directory(view.file_name(), self.window.folders())
        if not working_dir:
            return sublime.status_message('Could not find a PHPUnit working directory')

        coverage_html_index_html_file = os.path.join(working_dir, 'build/coverage/index.html')
        if not os.path.exists(coverage_html_index_html_file):
            return sublime.status_message('Could not find PHPUnit HTML code coverage %s' % coverage_html_index_html_file)

        import webbrowser
        webbrowser.open_new_tab('file://' + coverage_html_index_html_file)
