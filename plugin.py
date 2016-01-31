import sublime
import sublime_plugin
import re
import os

DEBUG_MODE=bool(os.getenv('SUBLIME_PHPUNIT_DEBUG'))

if DEBUG_MODE:
    def debug_message(message):
        """
        Prints a debug level message.
        """
        print('[phpunit] %s' % str(message))
else:
    def debug_message(message):
        pass

class PluginSettings():

    def __init__(self, name):
        self.name = name
        self.loaded = False
        self.transient_data = {}

    def on_load(self):
        if self.loaded:
            return

        self.loaded = True

    def get(self, key):
        if not self.loaded:
            raise RuntimeError('Plugin settings not loaded')

        window = sublime.active_window()
        if window is not None:

            view = window.active_view()
            if view is not None:

                settings = view.settings()
                if settings.has(self.name + '.' + key):
                    return settings.get(self.name + '.' + key)

        raise RuntimeError('Unknown plugin setting "%s"' % key)

    def get_transient(self, key, default = None):
        if key in self.transient_data:
            return self.transient_data[key]

        try:
            return self.get(key)
        except:
            return default

    def set_transient(self, key, value):
        self.transient_data[key] = value

plugin_settings = PluginSettings('phpunit')

def plugin_loaded():
    plugin_settings.on_load()

class PHPUnitConfigurationFileFinder():

    """
    Find the first PHPUnit configuration file, either
    phpunit.xml or phpunit.xml.dist, in {file_name}
    directory or the nearest common ancestor directory
    in {folders}.
    """

    def find(self, file_name, folders):
        """
        Finds the PHPUnit configuration file.
        """

        debug_message('[PHPUnitConfigurationFileFinder] Find PHPUnit configuration file for "%s" in folders %s' % (file_name, folders))

        if file_name == None:
            debug_message('[PHPUnitConfigurationFileFinder] Invalid argument: file is None')
            return None

        if not isinstance(file_name, str):
            debug_message('[PHPUnitConfigurationFileFinder] Invalid argument: file not instance')
            return None

        if not len(file_name) > 0:
            debug_message('[PHPUnitConfigurationFileFinder] Invalid argument: file len not > 0')
            return None

        if folders == None:
            debug_message('[PHPUnitConfigurationFileFinder] Invalid argument: folders is None')
            return None

        if not isinstance(folders, list):
            debug_message('[PHPUnitConfigurationFileFinder] Invalid argument: folders not instance')
            return None

        if not len(folders) > 0:
            debug_message('[PHPUnitConfigurationFileFinder] Invalid argument: folder len not > 0')
            return None

        ancestor_folders = []
        common_prefix = os.path.commonprefix(folders)
        parent = os.path.dirname(file_name)
        while parent not in ancestor_folders and parent.startswith(common_prefix):
            ancestor_folders.append(parent)
            parent = os.path.dirname(parent)
        ancestor_folders.sort(reverse=True)

        debug_message('[PHPUnitConfigurationFileFinder] Look for PHPUnit configuration file in common ancestor folder(s) (%s) %s' % (len(ancestor_folders), ancestor_folders))

        for ancestor in ancestor_folders:
            for file_name in ['phpunit.xml', 'phpunit.xml.dist']:
                phpunit_configuration_file = os.path.join(ancestor, file_name)
                if os.path.isfile(phpunit_configuration_file):
                    debug_message('[PHPUnitConfigurationFileFinder] PHPUnit configuration file found at %s' % phpunit_configuration_file)
                    return phpunit_configuration_file

        debug_message('[PHPUnitConfigurationFileFinder] Configuration file not found')

        return None

    def find_dirname(self, file_name, folders):
        phpunit_configuration_file = self.find(file_name, folders)
        if phpunit_configuration_file:
            return os.path.dirname(phpunit_configuration_file)

        return None

def is_valid_php_identifier(string):
    return re.match('^[a-zA-Z_][a-zA-Z0-9_]*$', string)

class ViewHelpers():

    def __init__(self, view):
        self.view = view

    def contains_phpunit_test_case(self):
        """
        Returns true if view contains a PHPUnit test-case; otherwise false
        """

        for php_class in self.find_php_classes():
            if php_class[-4:] == 'Test':
                return True

        return False

    def find_php_classes(self):
        """
        Returns an array of classes (class names) defined in the view
        """

        classes = []
        for class_as_region in self.view.find_by_selector('source.php entity.name.type.class'):
            class_as_string = self.view.substr(class_as_region)
            if is_valid_php_identifier(class_as_string):
                classes.append(class_as_string)

        return classes

    def find_first_switchable(self):
        """
        Returns the first switchable; otherwise None
        """

        debug_message('[ViewHelpers::find_first_switchable_file] Find in view: %s' % ({"id": self.view.id(), "file_name": self.view.file_name()}))

        for class_name in self.find_php_classes():

            debug_message('[ViewHelpers::find_first_switchable_file] Trying to find switchable for class "%s"' % (class_name))

            if class_name[-4:] == "Test":
                lookup_symbol = class_name[:-4]
            else:
                lookup_symbol = class_name + "Test"

            debug_message('[ViewHelpers::find_first_switchable_file] Trying to find switchable class "%s"' % (lookup_symbol))

            switchables_in_open_files = self.view.window().lookup_symbol_in_open_files(lookup_symbol)
            debug_message('[ViewHelpers::find_first_switchable_file] Found (%d) possible switchables for %s in open files: %s' % (len(switchables_in_open_files), class_name, str(switchables_in_open_files)))

            for open_file in switchables_in_open_files:
                debug_message('[ViewHelpers::find_first_switchable_file] Found switchable %s for %s in open files (%s): %s' % (open_file, class_name, len(switchables_in_open_files), switchables_in_open_files))
                return open_file

            switchables_in_index = self.view.window().lookup_symbol_in_index(lookup_symbol)
            debug_message('[ViewHelpers::find_first_switchable_file] Found (%d) possible switchables for %s in index: %s' % (len(switchables_in_index), class_name, switchables_in_index))

            for index in switchables_in_index:
                debug_message('[ViewHelpers::find_first_switchable_file] Found switchable %s for "%s" in indexes (%d): %s' % (index, class_name, len(switchables_in_index), switchables_in_index))
                return index

            debug_message('[ViewHelpers::find_first_switchable_file] No switchable found for class: %s' % class_name)

    def find_first_switchable_file(self):
        """
        Returns the first switchable file; otherwise None
        """

        first_switchable = self.find_first_switchable()
        if not first_switchable:
            return None

        return first_switchable[0]

class PHPUnitTextUITestRunner():

    """
    PHPUnit test runner
    """

    def __init__(self, window):
        self.window = window

    def run(self, args=None):
        if args:
            debug_message('PHPUnitTextUITestRunner %s' % (args))
            self._run(**args)
        else:
            debug_message('PHPUnitTextUITestRunner')
            self._run()

    def _run(self, working_dir=None, unit_test_or_directory=None, options = None):

        view = self.window.active_view()
        if not view:
            return

        if working_dir is None:
            working_dir = PHPUnitConfigurationFileFinder().find_dirname(view.file_name(), self.window.folders())

        if not working_dir:
            return debug_message('[PHPUnitTextUITestRunner] Could not find a PHPUnit working directory')

        if not os.path.isdir(working_dir):
            return debug_message('[PHPUnitTextUITestRunner] Working directory does not exist or is not a directory: %s' % (working_dir))

        if unit_test_or_directory and not os.path.isfile(unit_test_or_directory) and not os.path.isdir(unit_test_or_directory):
            return debug_message('[PHPUnitTextUITestRunner] Unit test or directory is invalid: %s' % (unit_test_or_directory))

        if plugin_settings.get('save_all_on_run'):
            for view in self.window.views():
                if view.is_dirty() and view.file_name():
                    view.run_command('save')

        if plugin_settings.get('composer') and os.path.isfile(os.path.join(working_dir, 'vendor', 'bin', 'phpunit')):
            debug_message('[PHPUnitTextUITestRunner] Found Composer installed PHPUnit: "vendor/bin/phpunit"')
            cmd = 'vendor/bin/phpunit'
        else:
            debug_message('[PHPUnitTextUITestRunner] Composer installed PHPUnit not found, using default command: "phpunit"')
            cmd = 'phpunit'

        # Options
        #
        # Order of Precedence
        #
        # * User specific "phpunit.options" setting
        # * Project specific "phpunit.options" setting
        # * toggled "transient/session" settings
        # * this command's argument

        if options is None:
            options = {}

        for k, v in plugin_settings.get_transient('options', {}).items():
            if k not in options:
                options[k] = v

        for k, v in plugin_settings.get('options').items():
            if k not in options:
                options[k] = v

        for k, v in options.items():
            if not v == False:
                cmd += " --" + k
                if not v == True:
                    cmd += " \"" + v + "\""

        if unit_test_or_directory:
            cmd += " " + unit_test_or_directory

        debug_message('[PHPUnitTextUITestRunner] cmd: %s' % cmd)
        debug_message('[PHPUnitTextUITestRunner] options: %s' % options)
        debug_message('[PHPUnitTextUITestRunner] working_dir: %s' % working_dir)

        self.window.run_command('exec', {
            'cmd': cmd,
            'working_dir': working_dir,
            'file_regex': '([a-zA-Z0-9\\.\\/_-]+)(?: on line |\:)([0-9]+)$',
            'shell': True,
            'quiet': not DEBUG_MODE
        })

        # save last run arguments (for current window)
        plugin_settings.set_transient('__window__' + str(self.window.id()) + '__run_last_test_args', {
            'working_dir': working_dir,
            'unit_test_or_directory': unit_test_or_directory,
            'options': options
        })

        panel_settings = self.window.create_output_panel('exec').settings()
        panel_settings.set('syntax','Packages/phpunit/test-results.hidden-tmLanguage')
        panel_settings.set('rulers', [])
        panel_settings.set('gutter', False)
        panel_settings.set('scroll_past_end', False)
        panel_settings.set('draw_centered', False)
        panel_settings.set('line_numbers', False)
        panel_settings.set('spell_check', False)
        panel_settings.set('word_wrap', False) # @todo results output should wrap to size of window

        panel_settings.set('color_scheme',
            plugin_settings.get('color_scheme')
                if plugin_settings.get('color_scheme')
                    else view.settings().get('color_scheme'))

    def run_last_test(self):
        # get last run arguments (for current window)
        args = plugin_settings.get_transient('__window__' + str(self.window.id()) + '__run_last_test_args')
        if args:
            self.run(args)

class PhpunitRunAllTests(sublime_plugin.WindowCommand):

    """
    Runs all tests
    """

    def run(self):
        PHPUnitTextUITestRunner(self.window).run()

class PhpunitRunLastTestCommand(sublime_plugin.WindowCommand):

    """
    Run last test
    """

    def run(self):
        PHPUnitTextUITestRunner(self.window).run_last_test()

class PhpunitRunSingleTestCommand(sublime_plugin.WindowCommand):

    """
    Run single test
    """

    def run(self):
        view = self.window.active_view()
        if not view:
            return

        options = {}
        view_helpers = ViewHelpers(view)

        if view_helpers.contains_phpunit_test_case():
            unit_test_file = view.file_name()
            unit_test_method_names = self.selected_unit_test_method_names(view)
            if unit_test_method_names:
                # @todo optimise filter regex; possibly limit the size of the regex too
                options['filter'] = '::(' + '|'.join(unit_test_method_names) + ')( with data set .+)?$'
        else:
            unit_test_file = view_helpers.find_first_switchable_file()
            # @todo how to check that the switchable contains a testcase?

        if not unit_test_file:
            debug_message('[phpunit_run_single_test_command] Could not find a test-case or a switchable test-case')
            return

        PHPUnitTextUITestRunner(self.window).run({
            "unit_test_or_directory": unit_test_file,
            "options": options
        })

    def selected_unit_test_method_names(self, view):
        """
        If all selections are test methods returns an array of all selected
        test method names; otherwise None
        """

        # @todo should be a scoped selection i.e. is the selection a source.php entity.name.function
        method_names = []
        for region in view.sel():
            word = view.substr(view.word(region))
            if not is_valid_php_identifier(word) or word[:4] != 'test':
                return None

            method_names.append(word)

        return method_names

class PhpunitSwitchFile(sublime_plugin.WindowCommand):

    """
    Switch file
    """

    def run(self):

        current_view = self.window.active_view()
        if not current_view:
            return

        first_switchable = ViewHelpers(current_view).find_first_switchable()
        if not first_switchable:
            return sublime.status_message('No PHPUnit switchable found for "%s"' % current_view.file_name())

        debug_message('[phpunit_switch_file_command] Switching from "%s" to %s' % (current_view.file_name(), first_switchable))

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

class PHPUnitOption():

    def __init__(self, name):
        self.name = name

    def toggle(self):
        """
        Toggle a PHPUnit option
        """

        options = plugin_settings.get_transient('options', {})
        options[self.name] = not bool(options[self.name]) if self.name in options else True
        plugin_settings.set_transient('options', options)

class PhpunitToggleTapOption(sublime_plugin.WindowCommand):

    """
    Toggle PHPUnit --tap option
    """

    def run(self):
        PHPUnitOption('tap').toggle()

class PhpunitToggleTestdoxOption(sublime_plugin.WindowCommand):

    """
    Toggle PHPUnit --testdox option
    """

    def run(self):
        PHPUnitOption('testdox').toggle()

class PhpunitToggleNoCoverageOption(sublime_plugin.WindowCommand):

    """
    Toggle PHPUnit --no-coverage option
    """

    def run(self):
        PHPUnitOption('no-coverage').toggle()

class PhpunitOpenHtmlCodeCoverageInBrowser(sublime_plugin.WindowCommand):

    """
    Open HTML code coverage in browser
    """

    def run(self):

        working_dir = PHPUnitConfigurationFileFinder().find_dirname(self.window.active_view().file_name(), self.window.folders())
        if not working_dir:
            return sublime.status_message('PHPUnit: Could not find a working directory')

        coverage_html_index_file = os.path.join(working_dir, 'build/coverage/index.html')
        if not os.path.exists(coverage_html_index_file):
            return sublime.status_message('PHPUnit: Could not find HTML code coverage at "%s"' % coverage_html_index_file)

        import webbrowser
        webbrowser.open_new_tab('file://' + coverage_html_index_file)
