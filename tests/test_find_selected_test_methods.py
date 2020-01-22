from sublime import find_resources

from PHPUnitKit.tests import unittest
from PHPUnitKit.plugin import find_selected_test_methods


def _is_php_syntax_using_php_grammar():
    return 'php-grammar' in find_resources('PHP.sublime-syntax')[0]


class TestFindSelectedTestMethods(unittest.ViewTestCase):

    def test_empty(self):
        self.fixture('')
        self.assertEqual([], find_selected_test_methods(self.view))

    def test_none_when_plain_text(self):
        self.fixture('foo|bar')
        self.assertEqual([], find_selected_test_methods(self.view))

    def test_none_when_bof(self):
        self.fixture("""|<?php

            namespace User\\Repository;

            class ClassNameTest extends \\PHPUnit_Framework_TestCase
            {
                public function testOne()
                {
                    $this->assertTrue(true);
                }
            }

        """)

        self.assertEqual([], find_selected_test_methods(self.view))

    def test_one(self):
        self.fixture("""<?php

            namespace User\\Repository;

            class ClassNameTest extends \\PHPUnit_Framework_TestCase
            {
                public function testFoobar1()
                {
                    $this->assertTrue(true);
                }

                public function test|One()
                {
                    $this->assertTrue(true);
                }

                public function testFoobar2()
                {
                    $this->assertTrue(true);
                }
            }

        """)

        self.assertEqual(['testOne'], find_selected_test_methods(self.view))

    def test_underscore_test_methods(self):
        self.fixture("""<?php

            namespace User\\Repository;

            class ClassNameTest extends \\PHPUnit_Framework_TestCase
            {
                public function test_one_un|derscore()
                {
                    $this->assertTrue(true);
                }

                public function testFoobar()
                {
                    $this->assertTrue(true);
                }

                public function test_two|_under_scored()
                {
                    $this->assertTrue(true);
                }

            }

        """)

        self.assertEqual(['test_one_underscore', 'test_two_under_scored'],
                         find_selected_test_methods(self.view))

    def test_annotated_test_methods(self):
        self.fixture("""<?php

            namespace User\\Repository;

            class ClassNameTest extends \\PHPUnit_Framework_TestCase
            {
                /**
                 * @test
                 */
                public function o|ne()
                {
                    $this->assertTrue(true);
                }

                /** @test */
                public function tw|o()
                {
                    $this->assertTrue(true);
                }
            }

        """)

        self.assertEqual(['one', 'two'],
                         find_selected_test_methods(self.view))

    def test_many(self):
        self.fixture("""<?php

            namespace User\\Repository;

            class ClassNameTest extends \\PHPUnit_Framework_TestCase
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

        self.assertEqual(['testOne', 'testTwo', 'testThree'],
                         find_selected_test_methods(self.view))

    def test_many_when_cursor_is_anywhere_on_method_declarations(self):
        if _is_php_syntax_using_php_grammar():
            # Skip because php-grammar does not support this feature
            return

        self.fixture("""<?php
            class ClassNameTest extends \\PHPUnit_Framework_TestCase
            {
                public function foobar()
                {
                    $this->assertTrue(true);
                }

                public fun|ction testOne()
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

        self.assertEqual(['testOne', 'testTwo', 'testThree'],
                         find_selected_test_methods(self.view))

    def test_many_when_cursor_is_anywhere_inside_method_declarations(self):
        if _is_php_syntax_using_php_grammar():
            # Skip because php-grammar does not support this feature
            return

        self.fixture("""<?php
            class ClassNameTest extends \\PHPUnit_Framework_TestCase
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

        self.assertEqual(['testOne', 'testTwo', 'testThree'],
                         find_selected_test_methods(self.view))

    def test_setup_and_teardown_methods_should_be_ignored(self):
        self.fixture("""<?php

            class ClassNameTest extends \\PHPUnit_Framework_TestCase
            {
                public function se|tUp() {}
                public function se|tup() {}
                public function tea|rDown() {}
                public function tea|rdown() {}
                public function tes|t_x() {}
                public function te|stY() {}
            }

        """)

        self.assertEqual(['test_x', 'testY'],
                         find_selected_test_methods(self.view))

    def test_issue_76_setup_method_is_not_a_test_method(self):
        self.fixture("""<?php
            namespace Tests\\Feature;

            use Tests\\TestCase;

            class CreateThreadsTest extends TestCase
            {
                use DatabaseMigrations, MockeryPHPUnitIntegration;

                public function se|tUp()
                {
                    parent::setUp();

                    app()->singleton(Recaptcha::class, function () {
                        return \\Mockery::mock(Recaptcha::class, function ($m) {
                            $m->shouldReceive('passes')->andReturn(true);
                        });
                    });
                }

                /** @test */
                function |guests_may_not_create_threads()
                {
                    $this->withExceptionHandling();

                    $this->get('/threads/create')
                        ->assertRedirect(route('login'));

                    $this->post(route('threads'))
                        ->assertRedirect(route('login'));
                }
            }
        """)

        self.assertEqual(['guests_may_not_create_threads'],
                         find_selected_test_methods(self.view))

    def test_issue_76_list_index_out_of_range(self):
        self.fixture("""<?php
            class ClassNameTest extends \\PHPUnit_Framework_TestCase {
                public function setUp() {
                    $func = function () {};
                }

                /** @test */
                function x_|y_z() {}
            }
        """)

        self.assertEqual(['x_y_z'], find_selected_test_methods(self.view))
