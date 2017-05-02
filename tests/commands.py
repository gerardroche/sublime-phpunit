# Note: on why inline imports of the sublime module are used in the commands?
# We need to use inline import statements because tests fail on subsequent runs
# without them. The fail error is: "attribute 'Region' not found error". I'm
# not sure why this happens, however we are reloading these commands before the
# tests are run which is probably a cause of the issue. We need to reload these
# commands because they are required by the tests. See tests/__init__.py

import sublime # noqa
import sublime_plugin


class PhpunitTestReplace(sublime_plugin.TextCommand):

    def run(self, edit, text):
        import sublime # noqa see note above on why we are import sublime here

        self.view.replace(edit, sublime.Region(0, self.view.size()), text)


class PhpunitTestFilterSelection(sublime_plugin.TextCommand):

    def run(self, edit):
        import sublime # noqa see note above on why we are import sublime here

        cursor_placeholders = self.view.find_all('\|')
        if cursor_placeholders:
            self.view.sel().clear()
            for i, cursor_placeholder in enumerate(cursor_placeholders):
                self.view.sel().add(cursor_placeholder.begin() - i)
                self.view.replace(
                    edit,
                    sublime.Region(cursor_placeholder.begin() - i, cursor_placeholder.end() - i),
                    ''
                )
