from textwrap import dedent

from complexity import Complexity


class describe_simple_statements:
    def it_computes_simple_statement_complexity(self):
        assert complexity('pass') == 1

    def it_computes_statement_sequence_complexity(self):
        assert complexity(
            """
            pass
            pass
            """) == 1


class describe_conditionals:
    def it_computes_simple_branch_complexity(self):
        assert complexity(
            """
            if x: 1
            # implicit else
            """) == 2

    def it_computes_branch_complexity_with_else(self):
        assert complexity(
            """
            if x: 1
            else: 2
            """) == 2

    def it_computes_branch_complexity_with_else_if(self):
        assert complexity(
            """
            if x: 1
            elif y: 2
            # implicit else
            """) == 3

    def it_computes_branch_complexity_with_else_if_and_else(self):
        assert complexity(
            """
            if x: 1
            elif y: 2
            else: 3
            """) == 3

    def it_includes_complexity_of_child_nodes_of_ifs(self):
        assert complexity(
            """
            if x:
                if y: 1
                else: 2
            else: 3
            """) == 3

    def it_includes_complexity_of_child_nodes_of_elses(self):
        assert complexity(
            """
            if x: 1
            else:
                if y: 1
                # implicit else
            """) == 3


class describe_for_loops:
    def it_computes_complexity_of_for_loops(self):
        assert complexity(
            """
            for x in y: 1
            # implicit else
            """) == 2

    def it_computes_complexity_of_else_clauses_on_for_loops(self):
        assert complexity(
            """
            for x in y: 1
            else: 2
            """) == 2

    def it_computes_complexity_of_child_nodes_of_for_loops(self):
        assert complexity(
            """
            for x in y:
                if x: 1
                else: 2
            # implicit else
            """) == 3

    def it_computes_complexity_of_child_nodes_of_for_loop_else_clauses(self):
        assert complexity(
            """
            for x in y: 1
            else:
                if x: 2
                else: 3
            """) == 3


#it_includes_complexity_within_discarded_nodes
#it_includes_complexity_of_compound_conditionals
#it_includes_break_statements_in_for_loops
#it_includes_continue_statements_in_for_loops
#it_includes_while_loops
#it_includes_for_loops_aborted_with_break_which_avoids_else_clause


def complexity(code):
    return Complexity(dedent(code)).score

