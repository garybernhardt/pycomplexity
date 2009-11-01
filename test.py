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
            """) == 3

    def it_computes_branch_complexity_with_else_if_and_else(self):
        assert complexity(
            """
            if x: 1
            elif y: 2
            else: 3
            """) == 3


def complexity(code):
    return Complexity(dedent(code)).score

