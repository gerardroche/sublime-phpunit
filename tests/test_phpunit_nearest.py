from PHPUnitKit.tests import unittest


class TestPHPUnitNearest(unittest.DeferrableExecViewTestCase):

    def test_basic_run_nearest(self):
        if not self.endToEndTestsEnabled():
            print('SKIPPED')
            return

        self.openProjectFile('tests', 'NearestTest.php')

        yield self.getLoadTimeout()

        self.view.window().run_command('phpunit_test_nearest')

        yield self.getWaitTimeout()

        self.assertExecContentRegex('PHPUnit \\d+\\.\\d+\\.\\d+')
        self.assertExecContentRegex('\\.\\s+3 \\/ 3 \\(100%\\)')
        self.assertExecContentRegex('OK \\(3 tests, 15 assertions\\)')

    def test_can_run_nearest_test_method(self):
        if not self.endToEndTestsEnabled():
            print('SKIPPED')
            return

        self.openProjectFile('tests', 'NearestTest.php')

        yield self.getLoadTimeout()

        self.setSelection(152)

        self.view.window().run_command('phpunit_test_nearest')

        yield self.getWaitTimeout()

        self.assertExecContentRegex('\\.\\s+1 \\/ 1 \\(100%\\)')
        self.assertExecContentRegex('OK \\(1 test, 4 assertions\\)')

    def test_can_run_nearest_test_method_from_within_body_of_method(self):
        if not self.endToEndTestsEnabled():
            print('SKIPPED')
            return

        self.openProjectFile('tests', 'NearestTest.php')

        yield self.getLoadTimeout()

        self.setSelection(420)

        self.view.window().run_command('phpunit_test_nearest')

        yield self.getWaitTimeout()

        self.assertExecContentRegex('\\.\\s+1 \\/ 1 \\(100%\\)')
        self.assertExecContentRegex('OK \\(1 test, 5 assertions\\)')

    def test_can_run_nearest_multiple_test_methods(self):
        if not self.endToEndTestsEnabled():
            print('SKIPPED')
            return

        self.openProjectFile('tests', 'NearestTest.php')

        yield self.getLoadTimeout()

        self.setSelection([420, 650])

        self.view.window().run_command('phpunit_test_nearest')

        yield self.getWaitTimeout()

        self.assertExecContentRegex('\\.\\s+2 \\/ 2 \\(100%\\)')
        self.assertExecContentRegex('OK \\(2 tests, 11 assertions\\)')
