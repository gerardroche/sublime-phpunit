import re
import os

import sublime
import sublime_plugin

if bool(os.getenv('SUBLIME_PHPUNIT_DEBUG')):
    def debug_message(message):
        """Prints a debug level message."""
        print('DEBUG phpunitkit: %s' % str(message))
else:
    def debug_message(message):
        pass

def get_setting(key):
    view = sublime.active_window().active_view()
    if view:
        settings = view.settings()
    else:
        settings = sublime.load_settings('Preferences.sublime-settings')

    if settings.has('phpunit.' + key):
        return settings.get('phpunit.' + key)
    else:
        raise RuntimeError('Could not get setting: phpunit.%s' % key)

def get_window_setting(key, default = None):
    settings = sublime.active_window().settings()
    if settings.has('phpunit.' + str(key)):
        return settings.get('phpunit.' + str(key))
    else:
        try:
            return get_setting(key)
        except:
            return default

def set_window_setting(key, value):
    sublime.active_window().settings().set('phpunit.' + str(key), value)

def find_phpunit_configuration_file(file_name, folders):
    """
    Find the first PHPUnit configuration file, either phpunit.xml or
    phpunit.xml.dist, in {file_name} directory or the nearest common ancestor
    directory in {folders}.
    """
    debug_message('Find PHPUnit configuration file for %s in %s (%d)' % (file_name, folders, len(folders) if folders else 0))

    if file_name == None:
        return None

    if not isinstance(file_name, str):
        return None

    if not len(file_name) > 0:
        return None

    if folders == None:
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

        debug_message('      Found %d switchable symbol%s in open files %s' % (len(switchables_in_open_files), '' if len(switchables_in_open_files) == 1 else 's', str(switchables_in_open_files)))
        debug_message('      Found %d switchable symbol%s in index      %s' % (len(switchables_in_index), '' if len(switchables_in_index) == 1 else 's', str(switchables_in_index)))

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

class PHPUnitTextUITestRunner():

    def __init__(self, window):
        self.window = window

    def run(self, args=None):
        if args:
            debug_message('PHPUnitTextUITestRunner::run %s' % (args))
            self._run(**args)
        else:
            debug_message('PHPUnitTextUITestRunner::run {}')
            self._run()

    def _run(self, working_dir=None, unit_test_or_directory=None, options = None):
        view = self.window.active_view()
        if not view:
            return

        # Working directory
        if not working_dir:
            working_dir = find_phpunit_working_directory(view.file_name(), self.window.folders())
            if not working_dir:
                debug_message('Could not find a PHPUnit working directory')
                return
            debug_message('Found PHPUnit working directory: %s' % working_dir)
        if not os.path.isdir(working_dir):
            debug_message('PHPUnit working directory does not exist or is not a valid directory: %s' % working_dir)
            return
        debug_message('PHPUnit working directory: %s' % working_dir)

        # Unit test or directory
        if unit_test_or_directory:
            if not os.path.isfile(unit_test_or_directory) and not os.path.isdir(unit_test_or_directory):
                debug_message('PHPUnit test or directory is invalid: %s' % unit_test_or_directory)
                return
            unit_test_or_directory = os.path.relpath(unit_test_or_directory, working_dir)
        debug_message('PHPUnit test or directory: %s' % unit_test_or_directory)

        # PHPUnit options
        # Order of Precedence
        # * User specific "phpunit.options" setting
        # * Project specific "phpunit.options" setting
        # * toggled "transient/session" settings
        # * this command's argument
        if options is None:
            options = {}
        for k, v in get_window_setting('options', {}).items():
            if k not in options:
                options[k] = v
        for k, v in get_setting('options').items():
            if k not in options:
                options[k] = v
        debug_message('PHPUnit options %s' % str(options))

        # PHPUnit bin
        phpunit_bin = 'phpunit'
        if get_setting('composer'):
            relative_composer_phpunit_bin = os.path.join('vendor', 'bin', 'phpunit')
            composer_phpunit_bin = os.path.join(working_dir, relative_composer_phpunit_bin)
            if os.path.isfile(composer_phpunit_bin):
                debug_message('Found Composer PHPUnit bin: %s' % composer_phpunit_bin)
                phpunit_bin = relative_composer_phpunit_bin
        debug_message('PHPUnit bin: %s' % phpunit_bin)

        # Execute Command
        cmd = phpunit_bin
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
        if unit_test_or_directory:
            cmd += " " + unit_test_or_directory
        debug_message('exec cmd: %s' % cmd)

        # Write out every buffer (active window) with changes and a file name.
        if get_setting('save_all_on_run'):
            for view in self.window.views():
                if view.is_dirty() and view.file_name():
                    view.run_command('save')

        self.window.run_command('exec', {
            'cmd': cmd,
            'file_regex': '([a-zA-Z0-9\\.\\/_-]+)(?: on line |\:)([0-9]+)$',
            'quiet': not bool(os.getenv('SUBLIME_PHPUNIT_DEBUG')),
            'shell': True,
            'syntax': 'Packages/phpunitkit/test-results.hidden-tmLanguage',
            'word_wrap': False,
            'working_dir': working_dir
        })

        set_window_setting('last_test_run_args', {
            'working_dir': working_dir,
            'unit_test_or_directory': unit_test_or_directory,
            'options': options
        })

        # Configure color scheme
        panel_settings = self.window.create_output_panel('exec').settings()
        panel_settings.set('color_scheme',
            get_setting('color_scheme')
                if get_setting('color_scheme')
                    else view.settings().get('color_scheme'))

    def run_last_test(self):
        args = get_window_setting('last_test_run_args')
        if args:
            self.run(args)

class PhpunitRunAllTests(sublime_plugin.WindowCommand):

    def run(self):
        PHPUnitTextUITestRunner(self.window).run()

class PhpunitRunLastTestCommand(sublime_plugin.WindowCommand):

    def run(self):
        PHPUnitTextUITestRunner(self.window).run_last_test()

class PhpunitRunSingleTestCommand(sublime_plugin.WindowCommand):

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

        PHPUnitTextUITestRunner(self.window).run({
            "unit_test_or_directory": unit_test,
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
                word = view.substr(function_regions[i])
                if is_valid_php_identifier(word):
                    method_names.append(word)
                break

        if not method_names:
            for region in function_regions:
                word = view.substr(region)
                if is_valid_php_identifier(word):
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

class PhpunitToggleLongOption(sublime_plugin.WindowCommand):

    def run(self, option):
        options = get_window_setting('options', {})
        options[option] = not bool(options[option]) if option in options else True
        set_window_setting('options', options)

class PhpunitOpenHtmlCodeCoverageInBrowser(sublime_plugin.WindowCommand):

    def run(self):
        view = self.window.active_view()
        if not view:
            return

        working_dir = find_phpunit_working_directory(view.file_name(), self.window.folders())
        if not working_dir:
            sublime.status_message('Could not find a PHPUnit working directory')
            return

        coverage_html_index_html_file = os.path.join(working_dir, 'build/coverage/index.html')
        if not os.path.exists(coverage_html_index_html_file):
            sublime.status_message('Could not find PHPUnit HTML code coverage %s' % coverage_html_index_html_file)
            return

        import webbrowser
        webbrowser.open_new_tab('file://' + coverage_html_index_html_file)
