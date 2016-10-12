from threading import Thread
import unittest

import sublime
import sublime_plugin

class OutputPanel(object):

    def __init__(self, window, name):
        self.name = name
        self.window = window
        self.view = self.window.create_output_panel(self.name)
        self.view.settings().set('word_wrap', True)
        self.view.settings().set('line_numbers', False)
        self.view.settings().set('gutter', False)
        self.view.settings().set('scroll_past_end', False)

    def write(self, s):
        f = lambda: self.view.run_command('append', {'characters': s})
        sublime.set_timeout(f, 0)

    def flush(self):
        pass

    def show(self):
        self.window.run_command('show_panel', {'panel': 'output.' + self.name})

    def close(self):
        pass

class PhpunitRunAllPluginTests(sublime_plugin.WindowCommand):

    def run(self):

        display = OutputPanel(self.window, 'phpunit.tests')
        display.show()

        test_loader = unittest.TestLoader()
        test_suite = unittest.TestSuite()

        # @todo autoload all tests from tests/ directory rather than hardcoded imports

        from phpunitkit.tests.test_finder import PHPUnitConfigurationFileFinderTest
        test_suite.addTest(test_loader.loadTestsFromTestCase(PHPUnitConfigurationFileFinderTest))

        from phpunitkit.tests.test_view_helpers import ViewHelpersTest
        test_suite.addTest(test_loader.loadTestsFromTestCase(ViewHelpersTest))

        runner = unittest.TextTestRunner(stream=display, verbosity=2)

        def run_and_display():
            runner.run(test_suite)

        Thread(target=run_and_display).start()

    def is_enabled(self):
        return bool(self.window.active_view().settings().get('phpunit.development'))

# @todo is there is an ST command that replaces view content?
class phpunit_test_view_replace(sublime_plugin.TextCommand):

    def run(self, edit, text):
        self.view.replace(edit, sublime.Region(0, self.view.size()), text)
