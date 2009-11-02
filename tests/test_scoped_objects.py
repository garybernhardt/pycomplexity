from tests.utils import complexity


class describe_modules:
    def test_that_they_are_scored(self):
        assert complexity(
            """
            a if a else a
            """).stats.named('<module>').score == 2
        assert complexity(
            """
                0 if x else 1 if y else 2
            """).stats.named('<module>').score == 3

    def test_that_they_know_their_names(self):
        assert complexity("").stats.named('<module>').name == '<module>'

    def test_that_they_know_their_line_range(self):
        stats = complexity("").stats.named('<module>')
        assert stats.start_line == 1
        assert stats.end_line == 1

        stats = complexity(
            """
            a
            """).stats.named('<module>')
        print '-%s-' % (
            """
            a
            """)
        assert stats.start_line == 1
        assert stats.end_line == 3

    def test_module_with_function_in_it(self):
        assert complexity(
            """
            a if a else a
            def foo():
                a if a else a
            a if a else a
            """).stats.named('<module>').score == 3


class describe_functions:
    def test_that_they_are_scored(self):
        assert complexity(
            """
            def foo():
                0 if x else 1
            """).stats.named('foo').score == 2
        assert complexity(
            """
            def foo():
                0 if x else 1 if y else 2
            """).stats.named('foo').score == 3

    def test_that_they_know_their_names(self):
        assert complexity(
            """
            def foo(): pass
            """).stats.named('foo').name == 'foo'

    def test_that_they_know_their_line_range(self):
        stats = complexity("def foo(): pass").stats.named('foo')
        assert stats.start_line == 1
        assert stats.end_line == 1

        stats = complexity(
            """
            def foo(): pass
            """).stats.named('foo')
        assert stats.start_line == 2
        assert stats.end_line == 2


class describe_classes:
    def test_that_they_are_scored(self):
        assert complexity(
            """
            class Foo:
                0 if x else 1
            """).stats.named('Foo').score == 2
        assert complexity(
            """
            class Foo:
                0 if x else 1 if y else 2
            """).stats.named('Foo').score == 3

    def test_that_they_know_their_names(self):
        assert complexity(
            """
            class Foo: pass
            """).stats.named('Foo').name == 'Foo'

    def test_that_they_know_their_line_range(self):
        stats = complexity("class Foo: pass").stats.named('Foo')
        assert stats.start_line == 1
        assert stats.end_line == 1

        stats = complexity(
            """
            class Foo:
                pass
            """).stats.named('Foo')
        assert stats.start_line == 2
        assert stats.end_line == 3

    def test_that_they_include_code_interspersed_with_methods(self):
        stats = complexity(
            """
            class Foo:
                0 if x else 1
                def foo(self): pass
                0 if x else 1
            """).stats.named('Foo')
        assert stats.score == 3
        assert stats.end_line == 5



class describe_methods:
    def test_that_they_are_scored(self):
        assert complexity(
            """
            class Foo:
                def foo():
                    0 if x else 1
            """).stats.named('Foo.foo').score == 2
        assert complexity(
            """
            class Foo:
                def foo():
                    0 if x else 1 if y else 2
            """).stats.named('Foo.foo').score == 3

    def test_that_they_know_their_names(self):
        assert complexity(
            """
            class Foo:
                def foo(): pass
            """).stats.named('Foo.foo').name == 'Foo.foo'

    def test_that_they_know_their_line_range(self):
        stats = complexity(
            """
            class Foo():
                def foo():
                    pass
            """).stats.named('Foo.foo')
        assert stats.start_line == 3
        assert stats.end_line == 4

        stats = complexity(
            """
            pass
            class Foo:
                def foo():
                    pass
                    pass
            """).stats.named('Foo.foo')
        assert stats.start_line == 4
        assert stats.end_line == 6

