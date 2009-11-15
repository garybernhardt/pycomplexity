from textwrap import dedent

from complexity import compute_code_complexity


def complexity(code):
    return compute_code_complexity(dedent(code))

