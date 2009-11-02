from tests.utils import complexity


class describe_conditionals:
    def test_simple_branch(self):
        assert complexity(
            """
            if x: 1
            # implicit else
            """).score == 2

    def test_branch_with_else(self):
        assert complexity(
            """
            if x: 1
            else: 2
            """).score == 2

    def test_branch_with_else_if(self):
        assert complexity(
            """
            if x: 1
            elif y: 2
            # implicit else
            """).score == 3

    def test_branch_with_else_if_and_else(self):
        assert complexity(
            """
            if x: 1
            elif y: 2
            else: 3
            """).score == 3

    def test_child_nodes_of_ifs(self):
        assert complexity(
            """
            if x:
                if y: 1
                else: 2
            else: 3
            """).score == 3

    def test_child_nodes_of_elses(self):
        assert complexity(
            """
            if x: 1
            else:
                if y: 1
                # implicit else
            """).score == 3

    def test_compound_conditionals(self):
        assert complexity(
            """
            if x or y: 1
            """).score == 3

    def test_chained_compound_conditionals(self):
        assert complexity(
            """
            if a or b or c and d and e: 1
            """).score == 6

    def test_nested_compound_conditionals(self):
        assert complexity(
            """
            if x or (y or z): 1
            """).score == 4

    def test_logical_operator_inside_conditional_but_outside_test(self):
        assert complexity(
            """
            if x:
                x and y
            """).score == 2


class describe_inline_conditionals:
    def test_inline_conditionals(self):
        assert complexity("b if c else d").score == 2

    def test_nested_inline_conditionals(self):
        assert complexity(
            """
            (b
             if c
             else (d
                   if e
                   else f))
            """).score == 3

    def test_logical_operator_in_inline_conditional(self):
        assert complexity("a if b and c else d").score == 3

