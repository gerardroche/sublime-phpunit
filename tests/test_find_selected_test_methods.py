from sublime import find_resources

from phpunitkit.tests.utils import ViewTestCase
from phpunitkit.plugin import find_selected_test_methods


def _is_php_syntax_using_php_grammar():
    return 'php-grammar' in find_resources('PHP.sublime-syntax')[0]


class TestFindSelectedTestMethods(ViewTestCase):

    def test_empty(self):
        self.fixture('')
        self.assertEqual([], find_selected_test_methods(self.view))

    def test_none_in_plain_text(self):
        self.fixture('foo|bar')
        self.assertEqual([], find_selected_test_methods(self.view))

    def test_no_selection(self):
        self.fixture("""<?php
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
        """)

        self.assertEqual([], find_selected_test_methods(self.view))

    def test_selection_on_method_declaration(self):
        self.fixture("""<?php
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
        """)

        self.assertEqual(['testOne'], find_selected_test_methods(self.view))

    def test_selection_on_many_method_declarations(self):
        self.fixture("""<?php
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
        """)

        self.assertEqual(['testOne', 'testTwo', 'testThree'], find_selected_test_methods(self.view))

    def test_selection_anywhere_on_method_declarations(self):
        self.fixture("""<?php
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
        """)

        self.assertEqual(['testOne', 'testTwo', 'testThree'], find_selected_test_methods(self.view))

    def test_selection_anywhere_inside_method_declarations(self):
        if _is_php_syntax_using_php_grammar():
            # Skip because php-grammar does not support this feature
            return

        self.fixture("""<?php
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
        """)

        self.assertEqual(['testOne', 'testTwo', 'testThree'], find_selected_test_methods(self.view))
