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

def debug_get_view_info(view):
    return 'view=[ id=%d, buffer_id=%d, file=%s window=[ id=%d, active_view_id=%d, active_group=%s ]]'\
    % (view.id(), view.buffer_id(), view.file_name(), view.window().id(), view.window().active_view().id(), view.window().active_group())

def findup_phpunit_working_directory(file_name, folders):
    """
    Find the first PHPUnit configuration file directory,
    either phpunit.xml or phpunit.xml.dist, in the
    file_name directory or the nearest common ancestor
    directory in folders.
    """

    if file_name == None or not len(file_name) > 0:
        # @todo should probably throw a logic error
        return None

    if not len(folders) > 0:
        # @todo should probably throw a logic error
        return None

    debug_message("findup_phpunit_working_directory() file_name=%s folders=%s" % (file_name, folders))

    possible_folders = []
    folders_common_prefix = os.path.commonprefix(folders)
    file_name_dir = os.path.dirname(file_name)
    while file_name_dir not in possible_folders and file_name_dir.startswith(folders_common_prefix):
        possible_folders.append(file_name_dir)
        file_name_dir = os.path.dirname(file_name_dir)

    possible_folders.sort(reverse=True)

    debug_message("There are %d possible PHPUnit working directory locations: %s" % (len(possible_folders), possible_folders))

    for possible_folder in possible_folders:
        for file_name in ["phpunit.xml", "phpunit.xml.dist"]:
            phpunit_config_file = os.path.join(possible_folder, file_name)
            debug_message("  Looking for a PHPUnit working directory at %s..." % phpunit_config_file)
            if os.path.isfile(phpunit_config_file):
                working_dir = os.path.dirname(phpunit_config_file)
                debug_message("Found PHPUnit working directory at %s" % working_dir)
                return working_dir

    debug_message("Could not find a PHPUnit working directory.")

def find_php_classes(view):
    class_definitions = view.find_by_selector('source.php entity.name.type.class')
    classes = []
    for class_definition in class_definitions:
        class_name = view.substr(class_definition)
        if is_valid_php_identifier(class_name):
            classes.append(class_name)

    debug_message('[PHPUnit] Found %d class definition(s) %s in view: %s' % (len(classes), classes, debug_get_view_info(view)))

    return classes

def is_valid_php_identifier(string):
    return re.match('^[a-zA-Z][a-zA-Z0-9_]*$', string)

def find_first_switchable_file(view):
    for class_name in find_php_classes(view):

        debug_message("Trying to find switchable for class '%s'" % (class_name))

        if class_name[-4:] == "Test":
            lookup_symbol = class_name[:-4]
        else:
            lookup_symbol = class_name + "Test"

        debug_message("Trying to find switchable class '%s'" % (lookup_symbol))

        switchables_in_open_files = view.window().lookup_symbol_in_open_files(lookup_symbol)
        debug_message("Found (%d) possible switchables for %s in open files: %s" % (len(switchables_in_open_files), class_name, str(switchables_in_open_files)))

        for open_file in switchables_in_open_files:
            debug_message("Found switchable %s for %s in open files (%s): %s" % (open_file, class_name, len(switchables_in_open_files), switchables_in_open_files))
            return open_file[0]

        switchables_in_index = view.window().lookup_symbol_in_index(lookup_symbol)
        debug_message("Found (%d) possible switchables for %s in index: %s" % (len(switchables_in_index), class_name, switchables_in_index))

        for index in switchables_in_index:
            debug_message("Found switchable %s for %s in indexes (%d): %s" % (index, class_name, len(switchables_in_index), switchables_in_index))
            return index[0]

        debug_message("No switchable found for class: %s" % class_name)

def contains_phpunit_test_case(view):
    for class_name in find_php_classes(view):
        if class_name[-4:] == 'Test':
            return True
    return False

def get_selection_phpunit_test_method(view):
    for region in view.sel():
        word = view.substr(view.word(region))
        if is_valid_php_identifier(word):
            if word[:4] == "test":
                return word

def file_exists(view):
    return (view.file_name() is not None and len(view.file_name()) > 0)

def is_multiple_selection(view):
    return (len(view.sel()) != 1)

def is_selection_php_scope(view):
    for region in view.sel():
        if view.score_selector(region.begin(), 'source.php') > 0:
            return True
    return False

def load_settings():
    return sublime.load_settings("phpunit.last-run")

def load_last_run():
    settings = load_settings()
    return (
        settings.get("phpunit_last_test_run_working_dir"),
        settings.get("phpunit_last_test_run_unit_test_or_directory"),
        settings.get("phpunit_last_test_run_options")
    )

def save_last_run(working_dir, unit_test_or_directory=None, options = {}):
    settings = load_settings()
    settings.set("phpunit_last_test_run_working_dir", working_dir)
    settings.set("phpunit_last_test_run_unit_test_or_directory", unit_test_or_directory)
    settings.set("phpunit_last_test_run_options", options)
    sublime.save_settings("phpunit.last-run")

class PhpunitCommand(sublime_plugin.WindowCommand):

    def run(self, working_dir, unit_test_or_directory=None, options = {}):
        debug_message("[PhpunitCommand] working_dir=%s, unit_test_or_directory=%s, options=%s" % (working_dir, unit_test_or_directory, options))

        if not working_dir or not os.path.isdir(working_dir):
            debug_message("Working directory does not exist or is not a directory: %s" % (working_dir))
            return

        if unit_test_or_directory and not os.path.isfile(unit_test_or_directory) and not os.path.isdir(unit_test_or_directory):
            debug_message("Unit test or directory is invalid: %s" % (unit_test_or_directory))
            return

        self.window.run_command("save_all")

        active_view = self.window.active_view()
        if active_view:
            view_settings = active_view.settings()
            if view_settings.get("phpunit_option_testdox") != None:
                options['testdox'] = view_settings.get("phpunit_option_testdox")

        cmd = 'phpunit'

        for k, v in options.items():
            if not v == False:
                cmd += " --" + k
                if not v == True:
                    cmd += " \"" + v + "\""

        if unit_test_or_directory:
            cmd += " " + unit_test_or_directory

        debug_message("[Command]: %s" % cmd)

        self.window.run_command('exec', {
            'cmd': cmd,
            'working_dir': working_dir,
            'file_regex': '([a-zA-Z0-9\\/_-]+\.php)(?:\:| on line )([0-9]+)$',
            'shell': True,
            'quiet': not DEBUG_MODE
        })

        save_last_run(working_dir, unit_test_or_directory, options)

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
        debug_message("[TextCommand] phpunit_run_all_tests *** run")

        working_dir = findup_phpunit_working_directory(self.view.file_name(), self.view.window().folders())
        if not working_dir:
            debug_message("Could not find a PHPUnit working directory")
            return

        sublime.active_window().run_command('phpunit', { "working_dir": working_dir })

class PhpunitRunSingleTestCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        debug_message("[TextCommand] phpunit_run_single_test *** run")

        working_dir = findup_phpunit_working_directory(self.view.file_name(), self.view.window().folders())
        if not working_dir:
            debug_message("Could not find a PHPUnit working directory")
            return

        options = {}

        if not contains_phpunit_test_case(self.view):
            switchable_file = find_first_switchable_file(self.view)
            if not switchable_file:
                debug_message("Could not find a PHPUnit test case or a switchable file")
                return
            # @todo should verify that the file switched-to contains a testcase
            unit_test = switchable_file
        else:

            test_method = get_selection_phpunit_test_method(self.view)
            if test_method:
                options['filter'] = test_method

            unit_test = self.view.file_name()

        sublime.active_window().run_command("phpunit", {
            "working_dir": working_dir ,
            "unit_test_or_directory": unit_test,
            "options": options
        })

class PhpunitRunLastTestCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        debug_message("[TextCommand] phpunit_run_last_test *** run")

        working_dir, unit_test_or_directory, options = load_last_run()

        sublime.active_window().run_command("phpunit", {
            "working_dir": working_dir ,
            "unit_test_or_directory": unit_test_or_directory,
            "options": options
        })

class PhpunitSwitchFile(sublime_plugin.TextCommand):

    def run(self, edit, split_below=False, split_right=False):
        debug_message("[TextCommand] phpunit_switch_file *** run")

        file_name = find_first_switchable_file(self.view)
        if not file_name:
            return

        debug_message("Switching to %s from %s" % (file_name, self.view.file_name()))

        self.view.window().open_file(file_name)
