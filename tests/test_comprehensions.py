from tests.utils import complexity


class describe_list_comprehensions:
    def test_list_comprehension(self):
        assert complexity("[x for x in y]").score == 2

    def test_list_comprehension_with_inline_conditional(self):
        assert complexity("[x if y else z for x in x]").score == 3

    def test_nested_list_comprehensions(self):
        assert complexity("[x for x in [y for y in z]]").score == 3

    def test_list_comprehensions_with_multiple_fors(self):
        assert complexity("[x for x in y for y in z]").score == 3

    def test_list_comprehension_with_conditional(self):
        assert complexity("[x for x in y if x]").score == 3

    def test_list_comprehension_with_multiple_conditionals(self):
        assert complexity("[x for x in y if x and y]").score == 4

    def test_list_comprehension_with_multiple_conditionals_and_fors(self):
        assert complexity(
            """
            [x for x in x
             for y in y
             if x and y]
            """).score == 5


class describe_generator_expression:
    def test_generator_expression(self):
        assert complexity("(x for x in y)").score == 2

    def test_with_inline_conditional(self):
        assert complexity("(x if y else z for x in x)").score == 3

    def test_nested(self):
        assert complexity("(x for x in (y for y in z))").score == 3

    def test_with_multiple_fors(self):
        assert complexity("(x for x in y for y in z)").score == 3

    def test_with_conditional(self):
        assert complexity("(x for x in y if x)").score == 3

    def test_with_multiple_conditionals(self):
        assert complexity("(x for x in y if x and y)").score == 4

    def test_with_multiple_conditionals_and_fors(self):
        assert complexity(
            """
            (x for x in x
             for y in y
             if x and y)
            """).score == 5

