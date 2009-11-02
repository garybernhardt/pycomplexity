from tests.utils import complexity


class describe_functions:
    def test_that_they_are_scored(self):
        assert complexity(
            """
            def foo():
                0 if x else 1
            """).stats[0].score == 2
        assert complexity(
            """
            def foo():
                0 if x else 1 if y else 2
            """).stats[0].score == 3

    def test_that_they_know_their_names(self):
        assert complexity(
            """
            def foo(): pass
            """).stats[0].name == 'foo'

    def test_that_they_know_their_line_range(self):
        stats = complexity("def foo(): pass").stats[0]
        assert stats.start_line == 1
        assert stats.end_line == 1

        stats = complexity(
            """
            def foo(): pass
            """).stats[0]
        assert stats.start_line == 2
        assert stats.end_line == 2


class describe_classes:
    def test_that_they_are_scored(self):
        assert complexity(
            """
            class Foo:
                0 if x else 1
            """).stats[0].score == 2
        assert complexity(
            """
            class Foo:
                0 if x else 1 if y else 2
            """).stats[0].score == 3

    def test_that_they_know_their_names(self):
        assert complexity(
            """
            class Foo: pass
            """).stats[0].name == 'Foo'

    def test_that_they_know_their_line_range(self):
        stats = complexity("class Foo: pass").stats[0]
        assert stats.start_line == 1
        assert stats.end_line == 1

        stats = complexity(
            """
            class Foo:
                pass
            """).stats[0]
        assert stats.start_line == 2
        assert stats.end_line == 3

    def test_that_they_include_code_interspersed_with_methods(self):
        stats = complexity(
            """
            class Foo:
                0 if x else 1
                def foo(self): pass
                0 if x else 1
            """).stats[0]
        assert stats.score == 3
        assert stats.end_line == 5



class describe_methods:
    def test_that_they_are_scored(self):
        assert complexity(
            """
            class Foo:
                def foo():
                    0 if x else 1
            """).stats[1].score == 2
        assert complexity(
            """
            class Foo:
                def foo():
                    0 if x else 1 if y else 2
            """).stats[1].score == 3

    def test_that_they_know_their_names(self):
        assert complexity(
            """
            class Foo:
                def foo(): pass
            """).stats[1].name == 'Foo.foo'

    def test_that_they_know_their_line_range(self):
        stats = complexity(
            """
            class Foo():
                def foo():
                    pass
            """).stats[1]
        assert stats.start_line == 3
        assert stats.end_line == 4

        stats = complexity(
            """
            pass
            class Foo:
                def foo():
                    pass
                    pass
            """).stats[1]
        assert stats.start_line == 4
        assert stats.end_line == 6

