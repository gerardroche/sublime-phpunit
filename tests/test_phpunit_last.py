from PHPUnitKit.tests import unittest


class TestPHPUnitLast(unittest.DeferrableExecViewTestCase):

    def test_last_runs_last_test_run(self):
        if not self.endToEndTestsEnabled():
            print('SKIPPED')
            return

        self.openProjectFile('tests', 'LastTest.php')

        yield self.getLoadTimeout()

        self.view.window().run_command('phpunit_test_file')

        yield self.getWaitTimeout()

        self.clearExecOutput()
        self.assertExecContentEmpty()

        self.view.window().run_command('phpunit_test_last')

        yield self.getWaitTimeout()

        self.assertExecContentRegex('PHPUnit \\d+\\.\\d+\\.\\d+')
        self.assertExecContentRegex('\\.\\s+2 \\/ 2 \\(100%\\)')
        self.assertExecContentRegex('OK \\(2 tests, 6 assertions\\)')
