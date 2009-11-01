from textwrap import dedent

from complexity import Complexity


class describe_simple_statements:
    def test_simple_statement(self):
        assert complexity('pass') == 1

    def test_statement_sequence(self):
        assert complexity(
            """
            pass
            pass
            """) == 1


class describe_conditionals:
    def test_simple_branch(self):
        assert complexity(
            """
            if x: 1
            # implicit else
            """) == 2

    def test_branch_with_else(self):
        assert complexity(
            """
            if x: 1
            else: 2
            """) == 2

    def test_branch_with_else_if(self):
        assert complexity(
            """
            if x: 1
            elif y: 2
            # implicit else
            """) == 3

    def test_branch_with_else_if_and_else(self):
        assert complexity(
            """
            if x: 1
            elif y: 2
            else: 3
            """) == 3

    def test_child_nodes_of_ifs(self):
        assert complexity(
            """
            if x:
                if y: 1
                else: 2
            else: 3
            """) == 3

    def test_child_nodes_of_elses(self):
        assert complexity(
            """
            if x: 1
            else:
                if y: 1
                # implicit else
            """) == 3


class describe_for_loops:
    def test_for_loops(self):
        assert complexity(
            """
            for x in y: 1
            # implicit else
            """) == 2

    def test_else_clauses_on_for_loops(self):
        assert complexity(
            """
            for x in y: 1
            else: 2
            """) == 2

    def test_child_nodes_of_for_loops(self):
        assert complexity(
            """
            for x in y:
                if x: 1
                else: 2
            # implicit else
            """) == 3

    def test_child_nodes_in_for_loop_else_clauses(self):
        assert complexity(
            """
            for x in y: 1
            else:
                if x: 2
                else: 3
            """) == 3


#test_inline_conditionals
#test_discarded_nodes
#test_compound_conditionals
#test__break_statements_in_for_loops
#test__continue_statements_in_for_loops
#test__while_loops
#test__for_loops_aborted_with_break_which_avoids_else_clause


def complexity(code):
    return Complexity(dedent(code)).score

