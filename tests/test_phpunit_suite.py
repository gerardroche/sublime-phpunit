from PHPUnitKit.tests import unittest


class TestPHPUnitSuite(unittest.DeferrableExecViewTestCase):

    def test_suite(self):
        if not self.endToEndTestsEnabled():
            print('SKIPPED')
            return

        self.openProjectFile('phpunit.xml')

        yield self.getLoadTimeout()

        self.view.window().run_command('phpunit_test_suite')

        yield self.getWaitTimeout()

        self.assertExecContentRegex('PHPUnit \\d+\\.\\d+\\.\\d+')
        self.assertExecContentRegex('\\.\\.\\s+\\d+ \\/ \\d+ \\(100%\\)')
        self.assertExecContentRegex('OK \\(\\d+ tests, \\d+ assertions\\)')
