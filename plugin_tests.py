import os
from threading import Thread
import unittest

import sublime
import sublime_plugin

from phpunitkit.plugin import find_phpunit_configuration_file
from phpunitkit.plugin import find_phpunit_working_directory
from phpunitkit.plugin import find_php_classes
from phpunitkit.plugin import has_test_case

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

class FindersTest(unittest.TestCase):

    def fixtures_path(self):
        return os.path.join(os.path.dirname(__file__), 'tests', 'fixtures')

    def test_find_none(self):
        self.assertIsNone(find_phpunit_configuration_file(None, None))
        self.assertIsNone(find_phpunit_configuration_file('', ['']))
        self.assertIsNone(find_phpunit_configuration_file(' ', [' ']))

    def test_find_nonw_with_file(self):
        file = os.path.join(self.fixtures_path(), 'common_prefix_parent', 'valid', 'file.php')

        self.assertIsNone(find_phpunit_configuration_file(file, None))
        self.assertIsNone(find_phpunit_configuration_file(file, []))
        self.assertIsNone(find_phpunit_configuration_file(file, [' ']))
        self.assertIsNone(find_phpunit_configuration_file(file, ['foobarfoobar']))

    def test_find_nonw_with_folders(self):
        folders = [
            os.path.join(self.fixtures_path(), 'common_prefix_parent'),
            os.path.join(self.fixtures_path(), 'common_prefix_parent', 'has_phpunit_xml'),
            os.path.join(self.fixtures_path(), 'common_prefix_parent', 'has_phpunit_xml_dist')
        ]

        self.assertIsNone(find_phpunit_configuration_file(None, folders))
        self.assertIsNone(find_phpunit_configuration_file('', folders))
        self.assertIsNone(find_phpunit_configuration_file(' ', folders))
        self.assertIsNone(find_phpunit_configuration_file('foobarfoobar', folders))

    def test_find_phpunit_xml_dist(self):
        project_path = os.path.join(self.fixtures_path(), 'common_prefix_parent', 'has_phpunit_xml_dist')

        self.assertEqual(
            os.path.join(project_path, 'phpunit.xml.dist'),
            find_phpunit_configuration_file(
                os.path.join(project_path, 'src', 'Has', 'PHPUnitXmlDist.php'),
                [
                    os.path.join(self.fixtures_path(), 'common_prefix_parent'),
                    os.path.join(self.fixtures_path(), 'common_prefix_parent', 'has_phpunit_xml'),
                    os.path.join(self.fixtures_path(), 'common_prefix_parent', 'has_phpunit_xml_dist')
                ]
                )
        )

    def test_find_phpunit_xml_before_phpunit_xml_dist(self):
        project_path = os.path.join(self.fixtures_path(), 'common_prefix_parent', 'has_phpunit_xml')

        self.assertEqual(
            os.path.join(project_path, 'phpunit.xml'),
            find_phpunit_configuration_file(
                os.path.join(project_path, 'src', 'Has', 'PHPUnitXml.php'),
                [
                    os.path.join(self.fixtures_path(), 'common_prefix_parent'),
                    os.path.join(self.fixtures_path(), 'common_prefix_parent', 'has_phpunit_xml'),
                    os.path.join(self.fixtures_path(), 'common_prefix_parent', 'has_phpunit_xml_dist')
                ]
            )
        )

    def test_find_only_checks_as_far_as_the_nearest_common_prefix_of_folders(self):

        common_prefix_parent = os.path.join(self.fixtures_path(), 'common_prefix_parent')
        common_prefix = os.path.join(common_prefix_parent, 'common_prefix')
        folder_a = os.path.join(common_prefix, 'folder_a')
        folder_b = os.path.join(common_prefix, 'folder_b')

        php_file = os.path.join(folder_a, 'FileA.php')
        folders =  [folder_a, folder_b]

        self.assertIsNone(find_phpunit_configuration_file(php_file, folders))

        # adding the common prefix parent directory should yield success
        folders.append(common_prefix_parent)
        phpunit_xml_file = os.path.join(common_prefix_parent, 'phpunit.xml.dist')

        self.assertEqual(phpunit_xml_file, find_phpunit_configuration_file(php_file, folders))

class ViewHelpersTest(ViewTestCase):

    def test_find_php_classes_returns_array_of_classes_in_view(self):
        self.set_view_content('<?php\nclass x {}\nclass y {}')
        self.assertEquals(['x', 'y'], find_php_classes(self.view))

    def test_find_php_classes_returns_empty_array_when_view_is_empty(self):
        self.set_view_content('')
        self.assertEquals([], find_php_classes(self.view))

    def test_contains_phpunit_test_case_returns_true_when_view_has_test_case(self):
        self.set_view_content("<?php\nclass ExampleTest {}")
        self.assertTrue(has_test_case(self.view))

    def test_contains_phpunit_test_case_returns_false_when_view_has_no_test_case_classes(self):
        self.set_view_content('<?php\nclass x {}\nclass y {}')
        self.assertFalse(has_test_case(self.view))

    def test_contains_phpunit_test_case_returns_false_when_view_is_empty(self):
        self.set_view_content('')
        self.assertFalse(has_test_case(self.view))

class PhpunitRunAllPluginTests(sublime_plugin.WindowCommand):

    def run(self):

        display = OutputPanel(self.window, 'phpunit.tests')
        display.show()

        test_loader = unittest.TestLoader()
        test_suite = unittest.TestSuite()

        test_suite.addTest(test_loader.loadTestsFromTestCase(FindersTest))
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
