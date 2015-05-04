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

class Config():

    def __init__(self):
        self.loaded = False
        self.last_run_phpunit_command_args = {}
        self.testdox_format = False
        self.tap_format = False

    def load(self):
        if self.loaded:
            return

        self.plugin_settings = sublime.load_settings('phpunit.sublime-settings')
        self.loaded = True

    def get(self, key):
        if not self.loaded:
            raise RuntimeError('Configuration not loaded')

        if sublime.active_window() is not None:
            project_settings = sublime.active_window().active_view().settings()

            if project_settings.has('phpunit'):
                project_phpunit_settings = project_settings.get('phpunit')

                if key in project_phpunit_settings:
                    return project_phpunit_settings.get(key)

        if self.plugin_settings.has(key):
            return self.plugin_settings.get(key)

        raise RuntimeError('Unknown configuration key "%s"' % key)

    def get_last_run_phpunit_command_args(self):
        window_id = sublime.active_window().id()

        if window_id in self.last_run_phpunit_command_args:
            return self.last_run_phpunit_command_args[window_id]

        return None

    def set_last_run_phpunit_command_args(self, working_dir, unit_test_or_directory=None, options = {}):
        self.last_run_phpunit_command_args[sublime.active_window().id()] = {
            'working_dir': working_dir,
            'unit_test_or_directory': unit_test_or_directory,
            'options': options
        }

    def set_tap_format(self, flag):
        self.tap_format = bool(flag)

    def is_tap_format_enabled(self):
        return self.tap_format

    def set_testdox_format(self, flag):
        self.testdox_format = bool(flag)

    def is_testdox_format_enabled(self):
        return self.testdox_format

config = Config()

def plugin_loaded():
    config.load()

    # @deprecated since 0.2.0 BC fix: last-run file is no longer used
    old_phpunit_last_run_file = os.path.join(sublime.packages_path(), 'User', 'phpunit.last-run')
    if os.path.isfile(old_phpunit_last_run_file):
        os.remove(old_phpunit_last_run_file)

class PHPUnitXmlFinder():

    """
    Find the first PHPUnit configuration file, either
    phpunit.xml or phpunit.xml.dist, in file_name
    directory or the nearest common ancestor directory
    in folders.
    """

    def find(self, file_name, folders):
        """
        Finds the PHPUnit configuration file.
        """

        debug_message('[PHPUnitXmlFinder] Find for "%s" in folders: %s' % (file_name, folders))

        if file_name == None:
            debug_message('[PHPUnitXmlFinder] Invalid argument: file is None')
            return None

        if not isinstance(file_name, str):
            debug_message('[PHPUnitXmlFinder] Invalid argument: file not instance')
            return None

        if not len(file_name) > 0:
            debug_message('[PHPUnitXmlFinder] Invalid argument: file len not > 0')
            return None

        if folders == None:
            debug_message('[PHPUnitXmlFinder] Invalid argument: folders is None')
            return None

        if not isinstance(folders, list):
            debug_message('[PHPUnitXmlFinder] Invalid argument: folders not instance')
            return None

        if not len(folders) > 0:
            debug_message('[PHPUnitXmlFinder] Invalid argument: folder len not > 0')
            return None

        ancestor_folders = []
        common_prefix = os.path.commonprefix(folders)
        parent = os.path.dirname(file_name)
        while parent not in ancestor_folders and parent.startswith(common_prefix):
            ancestor_folders.append(parent)
            parent = os.path.dirname(parent)
        ancestor_folders.sort(reverse=True)

        debug_message('[PHPUnitXmlFinder] File has %s common ancestor project folder(s): %s' % (len(ancestor_folders), ancestor_folders))

        for ancestor in ancestor_folders:
            for file_name in ['phpunit.xml', 'phpunit.xml.dist']:
                configuration_file = os.path.join(ancestor, file_name)
                if os.path.isfile(configuration_file):
                    debug_message('[PHPUnitXmlFinder] Found configuration: %s' % configuration_file)
                    return configuration_file

        debug_message('[PHPUnitXmlFinder] Configuration file not found')
        return None

def findup_phpunit_xml_directory(file_name, folders):
    finder = PHPUnitXmlFinder()
    configuration = finder.find(file_name, folders)
    if configuration:
        return os.path.dirname(configuration)
    return None

def is_valid_php_identifier(string):
    return re.match('^[a-zA-Z_][a-zA-Z0-9_]*$', string)

class ViewHelpers():

    def __init__(self, view):
        self.view = view

    def contains_test_case(self):
        for class_name in self.find_php_classes():
            if class_name[-4:] == 'Test':
                debug_message('[ViewHelpers::contains_test_case] Found test-case "%s" in view: %s' % (class_name, {"id": self.view.id(), "file_name": self.view.file_name()}))
                return True
        return False

    def find_php_classes(self):
        class_definitions = self.view.find_by_selector('source.php entity.name.type.class')
        classes = []
        for class_definition in class_definitions:
            class_name = self.view.substr(class_definition)
            if is_valid_php_identifier(class_name):
                classes.append(class_name)

        debug_message('[ViewHelpers::find_php_classes] Found %d class definition(s) %s in view: %s' % (len(classes), classes, {"id": self.view.id(), "file_name": self.view.file_name()}))

        return classes

    def find_first_switchable_file(self):
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
                return open_file[0]

            switchables_in_index = self.view.window().lookup_symbol_in_index(lookup_symbol)
            debug_message('[ViewHelpers::find_first_switchable_file] Found (%d) possible switchables for %s in index: %s' % (len(switchables_in_index), class_name, switchables_in_index))

            for index in switchables_in_index:
                debug_message('[ViewHelpers::find_first_switchable_file] Found switchable %s for "%s" in indexes (%d): %s' % (index, class_name, len(switchables_in_index), switchables_in_index))
                return index[0]

            debug_message('[ViewHelpers::find_first_switchable_file] No switchable found for class: %s' % class_name)

class PHPUnitTextUITestRunner():

    def __init__(self, window):
        self.window = window

    def run(self, args=None):
        if args:
            self._run(**args)
        else:
            self._run()

    def runLast(self):
        args = config.get_last_run_phpunit_command_args()
        if args:
            self.run(args)

    def _run(self, working_dir=None, unit_test_or_directory=None, options = None):
        debug_message('command: PHPUnitTextUITestRunner {"working_dir": "%s", "unit_test_or_directory": "%s", "options": "%s"}' % (working_dir, unit_test_or_directory, options))

        if options is None:
            options = {}

        if working_dir is None:
            working_dir = findup_phpunit_xml_directory(self.window.active_view().file_name(), self.window.folders())

        if not working_dir:
            debug_message('[PHPUnitTextUITestRunner] Could not find a PHPUnit working directory')
            return

        if not os.path.isdir(working_dir):
            debug_message('[PHPUnitTextUITestRunner] Working directory does not exist or is not a directory: %s' % (working_dir))
            return

        if unit_test_or_directory and not os.path.isfile(unit_test_or_directory) and not os.path.isdir(unit_test_or_directory):
            debug_message('[PHPUnitTextUITestRunner] Unit test or directory is invalid: %s' % (unit_test_or_directory))
            return

        if config.get('save_all_on_run'):
            debug_message('[PHPUnitTextUITestRunner] Configuration "save_all_on_run" is enabled, saving active window view files...')
            self.window.run_command('save_all')

        if os.path.isfile(os.path.join(working_dir, 'vendor', 'bin', 'phpunit')):
            debug_message('[PHPUnitTextUITestRunner] Found Composer installed PHPUnit: vendor/bin/phpunit')
            cmd = 'vendor/bin/phpunit'
        else:
            debug_message('[PHPUnitTextUITestRunner] Composer installed PHPUnit not found, using default command: "phpunit"')
            cmd = 'phpunit'

        if 'testdox' not in options and config.is_testdox_format_enabled():
            options['testdox'] = True

        if 'tap' not in options and config.is_tap_format_enabled():
            options['tap'] = True

        for k, v in options.items():
            if not v == False:
                cmd += " --" + k
                if not v == True:
                    cmd += " \"" + v + "\""

        if unit_test_or_directory:
            cmd += " " + unit_test_or_directory

        debug_message('[PHPUnitTextUITestRunner] cmd: %s' % cmd)
        debug_message('[PHPUnitTextUITestRunner] working_dir: %s' % working_dir)

        self.window.run_command('exec', {
            'cmd': cmd,
            'working_dir': working_dir,
            'file_regex': '([a-zA-Z0-9\\/_-]+\.php)(?:\:| on line )([0-9]+)$',
            'shell': True,
            'quiet': not DEBUG_MODE
        })

        config.set_last_run_phpunit_command_args(
            working_dir,
            unit_test_or_directory,
            options
        )

        panel = self.window.get_output_panel("exec")
        panel.settings().set('syntax','Packages/phpunit/result.hidden-tmLanguage')
        panel.settings().set('color_scheme', 'Packages/phpunit/result.hidden-tmTheme')
        panel.settings().set('rulers', [])
        panel.settings().set('gutter', False)
        panel.settings().set('scroll_past_end', False)
        panel.settings().set('draw_centered', False)
        panel.settings().set('line_numbers', False)
        panel.settings().set('spell_check', False)
        panel.settings().set('word_wrap', True)
        self.window.run_command("show_panel", {"panel": "output.exec"})

class PhpunitRunAllTests(sublime_plugin.WindowCommand):

    def run(self):
        testRunner = PHPUnitTextUITestRunner(self.window)
        testRunner.run()

class PhpunitRunLastTestCommand(sublime_plugin.WindowCommand):

    def run(self):
        testRunner = PHPUnitTextUITestRunner(self.window)
        testRunner.runLast()

class PhpunitRunSingleTestCommand(sublime_plugin.WindowCommand):

    def run(self):
        options = {}
        view_helpers = ViewHelpers(self.window.active_view())

        if view_helpers.contains_test_case():
            unit_test = self.window.active_view().file_name()
            test_methods = self.selection_test_method_names()
            if test_methods:
                # @todo optimise filter regex; possibly limit the size of the regex too
                options['filter'] = '::(' + '|'.join(test_methods) + ')( with data set .+)?$'
        else:
            unit_test = view_helpers.find_first_switchable_file()
            if not unit_test:
                debug_message('[phpunit_run_single_test_command] Could not find a test-case or a switchable test-case')
                return
            # else @todo ensure that the switchable contains a testcase

        testRunner = PHPUnitTextUITestRunner(self.window)
        testRunner.run({
            "unit_test_or_directory": unit_test,
            "options": options
        })

    def selection_test_method_names(self):
        # @todo should be a scoped selection i.e. is the selection a source.php entity.name.function
        view = self.window.active_view()
        test_method_names = []
        for region in view.sel():
            word = view.substr(view.word(region))
            if not is_valid_php_identifier(word) or word[:4] != 'test':
                return None
            test_method_names.append(word)
        return test_method_names

class PhpunitSwitchFile(sublime_plugin.TextCommand):

    def run(self, edit):
        view_helpers = ViewHelpers(self.view)
        switchable_file_name = view_helpers.find_first_switchable_file()
        if not switchable_file_name:
            return

        debug_message('[phpunit_switch_file_command] Switching from "%s" to "%s"' % (self.view.file_name(), switchable_file_name))

        split_from_1_group = False
        if self.view.window().num_groups() == 1:
            # The most basic case. If only one group is open then split window for switchable
            self.view.window().run_command('set_layout', {
                "cols": [0.0, 0.5, 1.0],
                "rows": [0.0, 1.0],
                "cells": [[0, 0, 1, 1], [1, 0, 2, 1]]
            })
            self.view.window().focus_group(1)
            split_from_1_group = True

        self.view.window().open_file(switchable_file_name)

        if split_from_1_group == True:
            # if opened switchable is already opened and in group 0 then move it to the group 1 split
            if self.view.window().active_group() == 0:
                self.view.window().set_view_index(self.view, 1, 0)

class PhpunitToggleTapFormat(sublime_plugin.WindowCommand):

    def run(self):
        config.set_tap_format(not config.is_tap_format_enabled())

class PhpunitToggleTestdoxFormat(sublime_plugin.WindowCommand):

    def run(self):
        config.set_testdox_format(not config.is_testdox_format_enabled())
