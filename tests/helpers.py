import unittest


import sublime
import sublime_plugin


class phpunit_test_view_replace(sublime_plugin.TextCommand):

    def run(self, edit, text):
        # Don't know it fails without import sublime
        # here. Without the import running tests
        # multiple times fails with an
        # attribute "Region" not
        # found error.
        import sublime

        self.view.replace(edit, sublime.Region(0, self.view.size()), text)


class ViewTestCase(unittest.TestCase):

    def setUp(self):
        self.view = sublime.active_window().create_output_panel('phpunit_test_view', unlisted=True)
        self.view.set_scratch(True)
        self.view.settings().set('auto_indent', False)
        self.view.settings().set('indent_to_bracket', False)
        self.view.settings().set('tab_size', 4)
        self.view.settings().set('trim_automatic_white_space', False)
        self.view.settings().set('smart_indent', True)
        self.view.settings().set('tab_size', 4)
        self.view.settings().set('translate_tabs_to_spaces', True)
        self.view.set_syntax_file(sublime.find_resources('PHP.sublime-syntax')[0])

        self.maxDiff = None

    def tearDown(self):
        if self.view:
            self.view.close()

    def set_view_content(self, text):
        self.view.run_command('phpunit_test_view_replace', {'text': text})

    def get_view_content(self):
        return self.view.substr(sublime.Region(0, self.view.size()))
