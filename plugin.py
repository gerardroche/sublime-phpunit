import re
import os
import shutil
import shlex

import sublime
import sublime_plugin


if bool(os.getenv('SUBLIME_PHPUNIT_DEBUG')):
    def debug_message(message):
        """Prints a debug level message."""
        print('DEBUG phpunitkit: %s' % str(message))
else:
    def debug_message(message):
        pass

def fix_windows_path(path):

    if sublime.platform() == 'windows':
        return '"' + path + '"'
    return path

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

    for class_as_region in view.find_by_selector('source.php entity.name.type.class'):
        class_as_string = view.substr(class_as_region)
        if is_valid_php_identifier(class_as_string):
            classes.append(class_as_string)

    # Quick fix for ST build >= 3114 because the default PHP package changed the
    # scope on class entities.
    if not classes:
        for class_as_region in view.find_by_selector('source.php entity.name.class'):
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


class PHPUnit():

    def __init__(self, window):
        self.window = window

    def run(self, args=None):
        if args:
            debug_message('PHPUnit::run %s' % (args))
            self._run(**args)
        else:
            debug_message('PHPUnit::run {}')
            self._run()

    def _run(self, working_dir=None, file=None, options=None):
        view = self.window.active_view()
        if not view:
            return sublime.status_message('PHPUnit: no active view')

        if not working_dir:
            working_dir = find_phpunit_working_directory(view.file_name(), self.window.folders())
            if not working_dir:
                return sublime.status_message('PHPUnit: could not find a working directory')

        if not os.path.isdir(working_dir):
            return sublime.status_message('PHPUnit: working directory does not exist or is not a valid directory')

        debug_message('Working directory: %s' % working_dir)

        if file:
            if not os.path.isfile(file):
                return sublime.status_message('PHPUnit: unit test file does not exist or is not a valid file')

            file = os.path.relpath(file, working_dir)

        debug_message('File: %s' % file)

        if options is None:
            options = {}

        for k, v in get_window_setting('phpunit.options', default={}, window=self.window).items():
            if k not in options:
                options[k] = v

        for k, v in view.settings().get('phpunit.options').items():
            if k not in options:
                options[k] = v

        debug_message('Options: %s' % str(options))

        cmd = ''

        php_executable = view.settings().get('phpunit.php_executable')
        if php_executable:
            php_executable = os.path.expanduser(php_executable)

            if not os.path.isfile(php_executable):
                return sublime.status_message('PHPUnit: PHP executable not found')

            if not os.access(php_executable, os.X_OK):
                return sublime.status_message('PHPUnit: PHP executable is not executable')

            cmd += fix_windows_path(php_executable) + ' '

        else:

            php_version_file = os.path.join(working_dir, '.php-version')
            if os.path.isfile(php_version_file):

                with open(php_version_file, 'r') as f:
                    php_version = f.read().strip()

                php_version = re.match('^master|[1-9]+\.[0-9x](?:\.[0-9x])?(?:snapshot)?$', php_version)
                if not php_version:
                    return sublime.status_message('PHPUnit: .php-version file version is invalid')

                php_versions_path = view.settings().get('phpunit.php_versions_path')
                if not php_versions_path:
                    return sublime.status_message('PHPUnit: PHP versions path is not set')

                php_versions_path = os.path.expanduser(php_versions_path)
                if not os.path.isdir(php_versions_path):
                    return sublime.status_message('PHPUnit: PHP versions path does not exist or is not a valid directory: %s' % php_versions_path)

                php_version = php_version.group(0)

                php_executable = os.path.join(php_versions_path, php_version, 'bin', 'php')

                if not os.path.isfile(php_executable):
                    return sublime.status_message('PHPUnit: PHP executable for .php-version file not found: %s' % php_executable)

                if not os.access(php_executable, os.X_OK):
                    return sublime.status_message('PHPUnit: PHP executable for .php-version file is not executable: %s' % php_executable)

                cmd += fix_windows_path(php_executable) + ' '

        debug_message('PHP executable: %s' % php_executable)

        if view.settings().get('phpunit.composer') and os.path.isfile(os.path.join(working_dir, os.path.join('vendor', 'bin', 'phpunit'))):
            executable = os.path.join(working_dir, os.path.join('vendor', 'bin', 'phpunit'))
        else:
            executable = shutil.which('phpunit')
            if not executable:
                return sublime.status_message('PHPUnit: PHP executable not found')

        cmd += fix_windows_path(executable)

        debug_message('Executable: %s' % executable)

        for k, v in options.items():
            if not v == False:
                if len(k) == 1:
                    if not v == False:
                        if v == True:
                            cmd += " -%s" % (k)
                        else:
                            if isinstance(v, list):
                                for _v in v:
                                    cmd += " -%s \"%s\"" % (k, _v)
                            else:
                                cmd += " -%s \"%s\"" % (k, v)
                else:
                    cmd += " --" + k
                    if not v == True:
                        cmd += " \"%s\"" % (v)
        if file:
            cmd += " " + fix_windows_path(file)

        debug_message('Command: %s' % cmd)

        # Write out every buffer (active window) with changes and a file name.
        if view.settings().get('phpunit.save_all_on_run'):
            for view in self.window.views():
                if view.is_dirty() and view.file_name():
                    view.run_command('save')

        if sublime.platform() == 'windows':
            file_regex = '((?:[a-zA-Z]\:)?[a-zA-Z0-9\\.\\/\\\\_-]+)(?: on line |\:)([0-9]+)$'
        else:
            file_regex = '([a-zA-Z0-9\\.\\/_-]+)(?: on line |\:)([0-9]+)$'

        self.window.run_command('exec', {
            'cmd': cmd,
            'file_regex': file_regex,
            'quiet': not bool(os.getenv('SUBLIME_PHPUNIT_DEBUG')),
            'shell': True,
            'syntax': 'Packages/phpunitkit/test-results.hidden-tmLanguage',
            'word_wrap': False,
            'working_dir': working_dir
        })

        set_window_setting('phpunit._test_last', {
            'working_dir': working_dir,
            'file': file,
            'options': options
        }, window=self.window)

        # Configure color scheme
        if view.settings().get('phpunit.color_scheme'):
            color_scheme = view.settings().get('phpunit.color_scheme')
        else:
            color_scheme = view.settings().get('color_scheme')
        self.window.create_output_panel('exec').settings().set('color_scheme', color_scheme)

    def run_last(self):
        args = get_window_setting('phpunit._test_last', window=self.window)
        if args:
            self.run(args)

    def run_file(self):
        view = self.window.active_view()
        if not view:
            return

        file = view.file_name()
        if not file:
            return

        self.run({"file": file})


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

        PHPUnit(self.window).run({
            "file": unit_test,
            "options": options
        })

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
