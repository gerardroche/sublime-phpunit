from PHPUnitKit.plugin import _resolve_working_dir
from PHPUnitKit.tests import unittest


class ViewStub():
    def __init__(self, file_name: str, folders: list):
        self._file_name = file_name
        self._folders = folders

    def file_name(self):
        return self._file_name

    def window(self):
        class ViewWindowStub():
            def __init__(self, folders: list):
                self._folders = folders

            def folders(self):
                return self._folders

        return ViewWindowStub(self._folders)


class TestResolveWorkingDir(unittest.ViewTestCase):

    def test_resolve_existing_working_dir(self):
        working_dir = unittest.fixtures_path('working_dir_empty')
        self.assertEqual(working_dir, _resolve_working_dir(self.view, working_dir))

    def test_resolve_non_existing_working_dir_raises_exception(self):
        working_dir = unittest.fixtures_path('working_dir_does_not_exist')
        with self.assertRaisesRegex(ValueError, 'working directory does not exist or is not a valid directory'):
            _resolve_working_dir(self.view, working_dir)

    def test_resolve_working_dir(self):
        file_name = unittest.fixtures_path('working_dir', 'phpunit.dist.xml')
        working_dir = unittest.fixtures_path('working_dir')
        folders = [working_dir]

        self.assertEqual(working_dir, _resolve_working_dir(ViewStub(file_name, folders), None))

    def test_resolve_working_dir_does_not_exist_for_file(self):
        file_name = unittest.fixtures_path('working_dir', 'phpunit.dist.xml')
        working_dir_2 = unittest.fixtures_path('working_dir_2')
        folders = [working_dir_2]

        with self.assertRaisesRegex(ValueError, 'working directory not found'):
            _resolve_working_dir(ViewStub(file_name, folders), None)

    def test_resolve_working_dir_does_exist_for_file(self):
        file_name = unittest.fixtures_path('working_dir', 'phpunit.dist.xml')
        working_dir = unittest.fixtures_path('working_dir')
        working_dir_2 = unittest.fixtures_path('working_dir_2')

        folders = [working_dir, working_dir_2]
        self.assertEqual(working_dir, _resolve_working_dir(ViewStub(file_name, folders), None))

        folders = [working_dir_2, working_dir]
        self.assertEqual(working_dir, _resolve_working_dir(ViewStub(file_name, folders), None))
