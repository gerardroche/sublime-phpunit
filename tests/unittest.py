import os
from unittest import TestCase
from unittest import mock  # noqa: F401
from unittest import skipIf  # noqa: F401

from sublime import find_resources
from sublime import active_window


def fixtures_path(*path) -> str:
    if path is None:
        return os.path.join(os.path.dirname(__file__), 'fixtures')

    return os.path.join(os.path.dirname(__file__), 'fixtures', *path)


class ViewTestCase(TestCase):

    def setUp(self) -> None:
        self.view = active_window().new_file()
        self.view.set_syntax_file(find_resources('PHP.sublime-syntax')[0])

    def tearDown(self) -> None:
        if self.view:
            self.view.set_scratch(True)
            self.view.close()

    def fixture(self, text):
        self.view.run_command('phpunit_test_setup_fixture', {'text': text})
