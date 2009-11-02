from tests.utils import complexity


class describe_for_loops:
    def test_for_loops(self):
        assert complexity(
            """
            for x in y: 1
            # implicit else
            """).score == 2

    def test_else_clauses_on_for_loops(self):
        assert complexity(
            """
            for x in y: 1
            else: 2
            """).score == 2

    def test_child_nodes_of_for_loops(self):
        assert complexity(
            """
            for x in y:
                if x: 1
                else: 2
            # implicit else
            """).score == 3

    def test_child_nodes_in_for_loop_else_clauses(self):
        assert complexity(
            """
            for x in y: 1
            else:
                if x: 2
                else: 3
            """).score == 3

    def test_break_statements_in_for_loops(self):
        # This seems like it should be more complex than an if with "pass"es,
        # but it's not. The break just reroutes the "if" path: instead of
        # going to the end of the loop and back up top, it goes straight back
        # up.
        assert complexity(
            """
            for x in y:
                if x:
                    break
            """).score == 3

    def test_break_statements_in_for_loops_with_else_clauses(self):
        # A "break" in a for loop skips the "else". My intuitive
        # interpretation is that this should increase CC by one. However, it's
        # basically a GOTO, and GOTOs don't increase the CC. Drawing the graph
        # out seems to confirm that a "break" with an "else" does not add a
        # path.
        assert complexity(
            """
            for x in y:
                if x:
                    break
            else:
                pass
            """).score == 3

    def test_continue_statement_in_for_loop(self):
        assert complexity(
            """
            for x in y:
                if x:
                    continue
            """).score == 3


# These are basically identical to the "for" loop tests, but abstracting them
# to remove the duplication would be just as long and more confusing.
class describe_while_loops:
    def test_while_loops(self):
        assert complexity(
            """
            while x: 1
            # implicit else
            """).score == 2

    def test_else_clauses_on_while_loops(self):
        assert complexity(
            """
            while x: 1
            else: 2
            """).score == 2

    def test_child_nodes_of_while_loops(self):
        assert complexity(
            """
            while x:
                if x: 1
                else: 2
            # implicit else
            """).score == 3

    def test_child_nodes_in_while_loop_else_clauses(self):
        assert complexity(
            """
            while x: 1
            else:
                if x: 2
                else: 3
            """).score == 3

    def test_break_statements_in_while_loops(self):
        # See discussion for "for" loops above.
        assert complexity(
            """
            while x:
                if x:
                    break
            """).score == 3

    def test_break_statements_in_while_loops_with_else_clauses(self):
        # See discussion for for loops above.
        assert complexity(
            """
            while x:
                if x:
                    break
            else:
                pass
            """).score == 3

    def test_continue_statement_in_while_loop(self):
        assert complexity(
            """
            while x:
                if x:
                    continue
            """).score == 3

