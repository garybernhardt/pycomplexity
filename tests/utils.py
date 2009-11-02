from textwrap import dedent

from complexity import Complexity


def complexity(code):
    return Complexity(dedent(code))

