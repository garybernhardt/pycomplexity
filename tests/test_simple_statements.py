from tests.utils import complexity


class describe_simple_statements:
    def test_pass(self):
        assert complexity('pass').score == 1

    def test_statement_sequence(self):
        assert complexity(
            """
            pass
            pass
            """).score == 1

    def test_constant(self):
        assert complexity("1").score == 1

    def test_assignment(self):
        assert complexity("x = 1").score == 1

    def test_name(self):
        assert complexity("a").score == 1

    def test_sequence_of_names(self):
        assert complexity(
            """
            a
            b
            c
            """).score == 1

    def test_logical_operators(self):
        assert complexity('a and b or (c or d and not e)').score == 1

