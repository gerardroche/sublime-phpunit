from PHPUnitKit.tests import unittest
from PHPUnitKit.plugin import find_php_classes


class TestFindPHPClasses(unittest.ViewTestCase):

    def test_empty(self):
        self.fixture('')
        self.assertEquals([], find_php_classes(self.view))

    def test_none(self):
        self.fixture('foobar')
        self.assertEquals([], find_php_classes(self.view))

    def test_one(self):
        self.fixture('<?php\nclass x {}')
        self.assertEquals(['x'], find_php_classes(self.view))
        self.assertEquals([{'class': 'x', 'namespace': None}], find_php_classes(self.view, True))

    def test_many(self):
        self.fixture('<?php\nclass x {}\nclass y {}\nclass z {}')
        self.assertEquals(['x', 'y', 'z'], find_php_classes(self.view))
        self.assertEquals([
            {
                'class': 'x',
                'namespace': None
            },
            {
                'class': 'y',
                'namespace': None
            },
            {
                'class': 'z',
                'namespace': None
            }], find_php_classes(self.view, True))

    def test_with_namespace(self):
        self.fixture("""<?php

            namespace User\\Repository;

            class ClassNameTest extends \\PHPUnit_Framework_TestCase
            {
            }

        """)

        self.assertEquals(['ClassNameTest'], find_php_classes(self.view))
        self.assertEquals(
            [{'class': 'ClassNameTest', 'namespace': 'User\\Repository'}],
            find_php_classes(self.view, True)
        )

    def test_with_namespace_alias(self):
        self.fixture("""<?php

            use A\\Name\\SpaceInterface as AliasName;

            class ClassNameTest
            {
            }

        """)

        self.assertEquals(['ClassNameTest'], find_php_classes(self.view))
        self.assertEquals(
            [{'class': 'ClassNameTest', 'namespace': None}],
            find_php_classes(self.view, True)
        )

    def test_with_implements(self):
        self.fixture("""<?php

            class ClassNameTest imports Countable
            {
            }

        """)

        self.assertEquals(['ClassNameTest'], find_php_classes(self.view))
