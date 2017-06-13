import sublime

from phpunitkit.tests.utils import ViewTestCase

from phpunitkit.plugin import _DEBUG
from phpunitkit.plugin import is_debug
from phpunitkit.plugin import find_php_classes
from phpunitkit.plugin import has_test_case
from phpunitkit.plugin import find_selected_test_methods


class FindPHPClassesTest(ViewTestCase):

    def test_find_php_classes_returns_array_of_classes_in_view(self):
        self.set_view_content('<?php\nclass x {}\nclass y {}')
        self.assertEquals(['x', 'y'], find_php_classes(self.view))

    def test_find_php_classes_returns_empty_array_when_view_is_empty(self):
        self.set_view_content('foobar')
        self.assertEquals([], find_php_classes(self.view))

    def test_find_php_classes_has_namespace(self):
        self.set_view_content('''<?php
            namespace Vendor\Package;
            class BooleanTest extends \PHPUnit_Framework_TestCase
            {
                public function testTrue()
                {
                    $this->assertTrue(true);
                }

                public function testFalse()
                {
                    $this->assertFalse(false);
                }
            }
        ''')

        self.assertEquals(['BooleanTest'], find_php_classes(self.view))

    def test_find_php_classes_with_namespace_alias(self):
        self.set_view_content('''<?php
            use some\\namespace\\BaseCommandInterface as Command;
            class CommandBus
            {
            }
        ''')

        self.assertEquals(['CommandBus'], find_php_classes(self.view))


class HasTestCaseTest(ViewTestCase):

    def test_contains_phpunit_test_case_returns_true_when_view_has_test_case(self):
        self.set_view_content("<?php\nclass ExampleTest {}")
        self.assertTrue(has_test_case(self.view))

    def test_contains_phpunit_test_case_returns_false_when_view_has_no_test_case_classes(self):
        self.set_view_content('<?php\nclass x {}\nclass y {}')
        self.assertFalse(has_test_case(self.view))

    def test_contains_phpunit_test_case_returns_false_when_view_is_empty(self):
        self.set_view_content('')
        self.assertFalse(has_test_case(self.view))


class IsDebugTest(ViewTestCase):

    def test_is_debug(self):
        self.view.settings().erase('debug')
        self.view.settings().erase('phpunit.debug')

        self.assertEqual(_DEBUG, is_debug())

        self.view.settings().set('phpunit.debug', True)
        self.assertTrue(is_debug(self.view))

        self.view.settings().set('phpunit.debug', False)
        self.assertFalse(is_debug(self.view))

        self.view.settings().erase('phpunit.debug')
        self.assertFalse(is_debug(self.view))

        self.view.settings().set('debug', True)
        self.view.settings().set('phpunit.debug', True)
        self.assertTrue(is_debug(self.view))

        self.view.settings().set('debug', False)
        self.view.settings().set('phpunit.debug', True)
        self.assertTrue(is_debug(self.view))

        self.view.settings().set('debug', False)
        self.view.settings().set('phpunit.debug', False)
        self.assertFalse(is_debug(self.view))

        self.view.settings().set('debug', True)
        self.view.settings().set('phpunit.debug', False)
        self.assertFalse(is_debug(self.view))


class SelectedUnitTestMethodsNamesTest(ViewTestCase):

    def test_none_in_empty(self):
        self.set_view_content('')
        self.assertEqual([], find_selected_test_methods(self.view))

    def test_none_in_plain_text(self):
        self.set_view_selection('foo|bar')
        self.assertEqual([], find_selected_test_methods(self.view))

    def test_no_selection(self):
        self.set_view_selection('''<?php
            namespace Vendor\Package;
            class BooleanTest extends \PHPUnit_Framework_TestCase
            {
                public function testOne()
                {
                    $this->assertTrue(true);
                }

                public function testTwo()
                {
                    $this->assertTrue(true);
                }
            }
        ''')

        self.assertEqual([], find_selected_test_methods(self.view))

    def test_selection_on_method_declaration(self):
        self.set_view_selection('''<?php
            namespace Vendor\Package;
            class BooleanTest extends \PHPUnit_Framework_TestCase
            {
                public function testFoobar()
                {
                    $this->assertTrue(true);
                }

                public function test|One()
                {
                    $this->assertTrue(true);
                }

                public function testFoobar()
                {
                    $this->assertTrue(true);
                }
            }
        ''')

        self.assertEqual(['testOne'], find_selected_test_methods(self.view))

    def test_selection_on_many_method_declarations(self):
        self.set_view_selection('''<?php
            namespace Vendor\Package;
            class BooleanTest extends \PHPUnit_Framework_TestCase
            {
                public function testFoobar()
                {
                    $this->assertTrue(true);
                }

                public function test|One()
                {
                    $this->assertTrue(true);
                }

                public function testFoobar()
                {
                    $this->assertTrue(true);
                }

                public function test|Two()
                {
                    $this->assertTrue(true);
                }

                public function testFoobar()
                {
                    $this->assertTrue(true);
                }

                public function test|Three()
                {
                    $this->assertTrue(true);
                }

                public function testFoobar()
                {
                    $this->assertTrue(true);
                }
            }
        ''')

        self.assertEqual(['testOne', 'testTwo', 'testThree'], find_selected_test_methods(self.view))

    def test_selection_anywhere_on_method_declarations(self):
        self.set_view_selection('''<?php
            class BooleanTest extends \PHPUnit_Framework_TestCase
            {
                public function foobar()
                {
                    $this->assertTrue(true);
                }

                pu|blic function testOne()
                {
                    $this->assertTrue(true);
                }

                public function foobar()
                {
                    $this->assertTrue(true);
                }

                public func|tion testTwo()
                {
                    $this->assertTrue(true);
                }

                public function foobar()
                {
                    $this->assertTrue(true);
                }

                public function testThree(|)
                {
                    $this->assertTrue(true);
                }

                public function foobar()
                {
                    $this->assertTrue(true);
                }
            }
        ''')

        self.assertEqual(['testOne', 'testTwo', 'testThree'], find_selected_test_methods(self.view))

    def test_selection_anywhere_inside_method_declarations(self):
        if 'php-grammar' in sublime.find_resources('PHP.sublime-syntax')[0]:
            # Skip because php-grammar does not support this feature
            return

        self.set_view_selection('''<?php
            class BooleanTest extends \PHPUnit_Framework_TestCase
            {
                public function foobar()
                {
                    $this->assertTrue(true);
                }

                public function testOne()
                {|
                    $this->assertTrue(true);
                }

                public function foobar()
                {
                    $this->assertTrue(true);
                }

                public function testTwo()
                {
                    $this->assert|True(true);
                }

                public function foobar()
                {
                    $this->assertTrue(true);
                }

                public function testThree()
                {
                    $this->assertTrue(true);
                    $this->assertTrue(true);
                    $this->assertTrue(true);
                    |
                }

                public function foobar()
                {
                    $this->assertTrue(true);
                }
            }
        ''')

        self.assertEqual(['testOne', 'testTwo', 'testThree'], find_selected_test_methods(self.view))
