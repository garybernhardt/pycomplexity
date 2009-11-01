from textwrap import dedent

from complexity import Complexity


class describe_complexity:
    def it_computes_simple_statement_complexity(self):
        assert complexity('pass') == 1

    def it_computes_statement_sequence_complexity(self):
        assert complexity(
            """
            pass
            pass
            """) == 1

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
                if y:
                    1
                # implicit else
            """) == 3

    #it_includes_complexity_within_discarded_nodes


def complexity(code):
    return Complexity(dedent(code)).score

