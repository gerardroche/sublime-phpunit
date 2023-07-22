import sublime

from PHPUnitKit.plugin import _create_exec_output_panel
from PHPUnitKit.tests import unittest


class TestCreateExecOutputPanel(unittest.ViewTestCase):

    def setUp(self):
        super().setUp()
        self.view.window().destroy_output_panel('exec')  # type: ignore[union-attr]

    def getExecOutputPanel(self):
        return self.view.window().find_output_panel('exec')  # type: ignore[union-attr]

    def getExecOutputPanelContent(self) -> str:
        view = self.view.window().find_output_panel('exec')  # type: ignore[union-attr]

        return view.substr(sublime.Region(0, view.size()))  # type: ignore[union-attr]

    def test_basic_exec_output_panel(self):
        font_size = self.view.settings().get('font_size')
        color_scheme = self.view.settings().get('color_scheme')
        self.assertIsNone(_create_exec_output_panel(self.view, {
            'envx': 'envy'}, 'thecmd'))  # type: ignore[func-returns-value]
        view = self.getExecOutputPanel()
        self.assertEqual('', self.getExecOutputPanelContent())
        self.assertFalse(view.settings().get('highlight_line'))
        self.assertEqual([], view.settings().get('rulers'))
        self.assertEqual(font_size, view.settings().get('font_size'))
        self.assertEqual(color_scheme, view.settings().get('color_scheme'))

    def test_can_set_exec_output_panel_font_size(self):
        font_size = self.view.settings().get('font_size')
        font_size_config = font_size + 1  # type: ignore[operator]
        self.view.settings().set('phpunit.font_size', font_size_config)
        _create_exec_output_panel(self.view, {'envx': 'envy'}, 'thecmd')
        self.assertEqual(font_size_config, self.getExecOutputPanel().settings().get('font_size'))

    def test_can_debug_exec_output(self):
        self.view.settings().set('phpunit.debug', True)
        _create_exec_output_panel(self.view, {'x': 'y'}, 'thecmd')
        self.assertEqual('env: {\'x\': \'y\'}\nt h e c m d\n\n', self.getExecOutputPanelContent())
