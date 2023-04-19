from PHPUnitKit.tests import unittest


class TestPHPUnitFile(unittest.DeferrableExecViewTestCase):

    def test_can_run_test_file_from_test(self):
        if not self.endToEndTestsEnabled():
            print('SKIPPED')
            return

        self.openProjectFile('tests', 'FizzTest.php')

        yield self.getLoadTimeout()

        self.view.window().run_command('phpunit_test_file')

        yield self.getWaitTimeout()

        self.assertExecContentRegex('PHPUnit \\d+\\.\\d+\\.\\d+')
        self.assertExecContentRegex('\\.\\s+1 \\/ 1 \\(100%\\)')
        self.assertExecContentRegex('OK \\(1 test, 1 assertion\\)')

    def test_can_run_test_file_from_file_under_test(self):
        if not self.endToEndTestsEnabled():
            print('SKIPPED')
            return

        self.openProjectFile('src', 'Buzz.php')

        yield self.getLoadTimeout()

        self.view.window().run_command('phpunit_test_file')

        yield self.getWaitTimeout()

        self.assertExecContentRegex('PHPUnit \\d+\\.\\d+\\.\\d+')
        self.assertExecContentRegex('\\.\\s+1 \\/ 1 \\(100%\\)')
        self.assertExecContentRegex('OK \\(1 test, 2 assertions\\)')
