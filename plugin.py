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
        self.last_run_phpunit_command_args = None

    def load(self):

        debug_message('[Config] Load plugin settings...')
        self.plugin_settings = sublime.load_settings('phpunit.sublime-settings')

        if DEBUG_MODE:
            debug_message('[Config] Found plugin settings: %s' % self.plugin_settings_as_dict())

        self.loaded = True

    def get(self, key):

        debug_message('[Config] get: %s' % key)

        # @todo should raise not loaded exception if not loaded
        if self.loaded:

            if sublime.active_window() is not None:

                debug_message('[Config] Window is active, load project settings...')
                project_settings = sublime.active_window().active_view().settings()

                if project_settings.has('phpunit'):
                    project_phpunit_settings = project_settings.get('phpunit')
                    debug_message('[Config] Found project settings: %s' % project_phpunit_settings)

                    if key in project_phpunit_settings:
                        value = project_phpunit_settings.get(key)
                        debug_message('[Config] Found project setting: %s' % ({key: value}))
                        return value
                else:
                    debug_message('[Config] No project settings')

            if DEBUG_MODE:
                debug_message('[Config] Found plugin settings: %s' % self.plugin_settings_as_dict())

            if self.plugin_settings.has(key):
                value = self.plugin_settings.get(key)
                debug_message('[Config] Found plugin setting: %s' % ({key: value}))
                return value

        # @todo should use special ConfigError class exception
        raise AttributeError('Unknown config key "%s"' % key)

    # @todo how to simplify dumping the settings?
    # @todo if not loaded raise not loaded exception
    def plugin_settings_as_dict(self):
        return {
            "save_all_on_run": self.plugin_settings.get('save_all_on_run')
        }

    def get_last_run_phpunit_command_args(self):
        return self.last_run_phpunit_command_args

    def set_last_run_phpunit_command_args(self, working_dir, unit_test_or_directory=None, options = {}):
        self.last_run_phpunit_command_args = {
            'working_dir': working_dir,
            'unit_test_or_directory': unit_test_or_directory,
            'options': options
        }

config = Config()

def plugin_loaded():
    debug_message('[plugin_loaded] Loading...')
    config.load()

    # last-run file is no longer used
    old_phpunit_last_run_file = os.path.join(sublime.packages_path(), 'User', 'phpunit.last-run')
    if os.path.isfile(old_phpunit_last_run_file):
        os.remove(old_phpunit_last_run_file)

class PHPUnitXmlFinder():

    """
    Find the first PHPUnit configuration file, either
    phpunit.xml or phpunit.xml.dist, in the file_name
    directory or the nearest common ancestor directory
    in folders.
    """

    def find(self, file_name, folders):
        """
        Finds the PHPUnit configuration file.
        """

        debug_message('[PHPUnitXmlFinder] Find the configuration for "%s" in folders: %s' % (file_name, folders))

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

def find_php_classes(view):
    class_definitions = view.find_by_selector('source.php entity.name.type.class')
    classes = []
    for class_definition in class_definitions:
        class_name = view.substr(class_definition)
        if is_valid_php_identifier(class_name):
            classes.append(class_name)

    debug_message('[find_php_classes] Found %d class definition(s) %s in view: id=%s, file_name=%s' % (len(classes), classes, view.id(), view.file_name()))

    return classes

def is_valid_php_identifier(string):
    return re.match('^[a-zA-Z][a-zA-Z0-9_]*$', string)

def find_first_switchable_file(view):
    for class_name in find_php_classes(view):

        debug_message('[find_first_switchable_file] Trying to find switchable for class "%s"' % (class_name))

        if class_name[-4:] == "Test":
            lookup_symbol = class_name[:-4]
        else:
            lookup_symbol = class_name + "Test"

        debug_message('[find_first_switchable_file] Trying to find switchable class "%s"' % (lookup_symbol))

        switchables_in_open_files = view.window().lookup_symbol_in_open_files(lookup_symbol)
        debug_message('[find_first_switchable_file] Found (%d) possible switchables for %s in open files: %s' % (len(switchables_in_open_files), class_name, str(switchables_in_open_files)))

        for open_file in switchables_in_open_files:
            debug_message('[find_first_switchable_file] Found switchable %s for %s in open files (%s): %s' % (open_file, class_name, len(switchables_in_open_files), switchables_in_open_files))
            return open_file[0]

        switchables_in_index = view.window().lookup_symbol_in_index(lookup_symbol)
        debug_message('[find_first_switchable_file] Found (%d) possible switchables for %s in index: %s' % (len(switchables_in_index), class_name, switchables_in_index))

        for index in switchables_in_index:
            debug_message('[find_first_switchable_file] Found switchable %s for %s in indexes (%d): %s' % (index, class_name, len(switchables_in_index), switchables_in_index))
            return index[0]

        debug_message('[find_first_switchable_file] No switchable found for class: %s' % class_name)

class PhpunitCommand(sublime_plugin.WindowCommand):

    def run(self, working_dir, unit_test_or_directory=None, options = {}):
        debug_message('command: phpunit_command {"working_dir": "%s", "unit_test_or_directory": "%s", "options": "%s"}' % (working_dir, unit_test_or_directory, options))

        if not working_dir or not os.path.isdir(working_dir):
            debug_message('[phpunit_command] Working directory does not exist or is not a directory: %s' % (working_dir))
            return

        if unit_test_or_directory and not os.path.isfile(unit_test_or_directory) and not os.path.isdir(unit_test_or_directory):
            debug_message('[phpunit_command] Unit test or directory is invalid: %s' % (unit_test_or_directory))
            return

        if config.get('save_all_on_run'):
            debug_message('[phpunit_command] "save_all_on_run" is enabled, saving...')
            self.window.run_command('save_all')

        cmd = 'phpunit'

        for k, v in options.items():
            if not v == False:
                cmd += " --" + k
                if not v == True:
                    cmd += " \"" + v + "\""

        if unit_test_or_directory:
            cmd += " " + unit_test_or_directory

        debug_message('[phpunit_command] cmd: %s' % cmd)
        debug_message('[phpunit_command] working_dir: %s' % working_dir)

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
        self.window.run_command("show_panel", {"panel": "output.exec"})

class PhpunitRunAllTests(sublime_plugin.TextCommand):

    def run(self, edit):
        debug_message('command: phpunit_run_all_tests')

        working_dir = findup_phpunit_xml_directory(self.view.file_name(), self.view.window().folders())
        if not working_dir:
            debug_message('[phpunit_run_all_tests_command] Could not find a PHPUnit working directory')
            return

        sublime.active_window().run_command('phpunit', { "working_dir": working_dir })

class PhpunitRunSingleTestCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        debug_message('command: phpunit_run_single_test')

        options = {}

        if self.contains_test_case():
            unit_test = self.view.file_name()
            test_method = self.get_selection_test_name()
            if test_method:
                options['filter'] = test_method
        else:
            unit_test = find_first_switchable_file(self.view)
            if not unit_test: # @todo check that the switchable contains a testcase
                debug_message('[phpunit_run_single_test_command] Could not find a test-case or a switchable test-case')
                return

        working_dir = findup_phpunit_xml_directory(self.view.file_name(), self.view.window().folders())
        if not working_dir:
            debug_message('[phpunit_run_single_test_command] Could not find a PHPUnit working directory')
            return

        sublime.active_window().run_command("phpunit", {
            "working_dir": working_dir ,
            "unit_test_or_directory": unit_test,
            "options": options
        })

    def contains_test_case(self):
        for class_name in find_php_classes(self.view):
            if class_name[-4:] == 'Test':
                return True
        return False

    def get_selection_test_name(self):
        # todo should be a scoped selection i.e. is the selection an entity.name.function
        for region in self.view.sel():
            word = self.view.substr(self.view.word(region))
            if is_valid_php_identifier(word):
                if word[:4] == 'test':
                    return word

class PhpunitRunLastTestCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        debug_message('command: phpunit_run_last_test')

        phpunit_args = config.get_last_run_phpunit_command_args()
        if phpunit_args:
            self.view.window().run_command('phpunit', phpunit_args)

class PhpunitSwitchFile(sublime_plugin.TextCommand):

    def run(self, edit, split_below=False, split_right=False):
        debug_message('command: phpunit_switch_file { "split_below": %s, "split_right": %s }')

        switchable_file_name = find_first_switchable_file(self.view)
        if not switchable_file_name:
            return

        debug_message('[phpunit_switch_file_command] Switching to %s from %s' % (switchable_file_name, self.view.file_name()))

        self.view.window().open_file(switchable_file_name)
