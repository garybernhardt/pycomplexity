from textwrap import dedent

from complexity import Complexity


class describe_simple_statements:
    def test_pass(self):
        assert complexity('pass') == 1

    def test_statement_sequence(self):
        assert complexity(
            """
            pass
            pass
            """) == 1

    def test_constant(self):
        assert complexity("1") == 1

    def test_assignment(self):
        assert complexity("x = 1") == 1

    def test_name(self):
        assert complexity("a") == 1

    def test_sequence_of_names(self):
        assert complexity(
            """
            a
            b
            c
            """) == 1

    def test_logical_operators(self):
        assert complexity('a and b or (c or d and not e)') == 1


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

    def test_compound_conditionals(self):
        assert complexity(
            """
            if x or y: 1
            """) == 3

    def test_chained_compound_conditionals(self):
        assert complexity(
            """
            if a or b or c and d and e: 1
            """) == 6

    def test_nested_compound_conditionals(self):
        assert complexity(
            """
            if x or (y or z): 1
            """) == 4


class describe_inline_conditionals:
    def test_inline_conditionals(self):
        assert complexity("b if c else d") == 2

    def test_nested_inline_conditionals(self):
        assert complexity(
            """
            (b
             if c
             else (d
                   if e
                   else f))
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
            """) == 3

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
            """) == 3

    def test_continue_statement_in_for_loop(self):
        assert complexity(
            """
            for x in y:
                if x:
                    continue
            """) == 3


# These are basically identical to the "for" loop tests, but abstracting them
# to remove the duplication would be just as long and more confusing.
class describe_while_loops:
    def test_while_loops(self):
        assert complexity(
            """
            while x: 1
            # implicit else
            """) == 2

    def test_else_clauses_on_while_loops(self):
        assert complexity(
            """
            while x: 1
            else: 2
            """) == 2

    def test_child_nodes_of_while_loops(self):
        assert complexity(
            """
            while x:
                if x: 1
                else: 2
            # implicit else
            """) == 3

    def test_child_nodes_in_while_loop_else_clauses(self):
        assert complexity(
            """
            while x: 1
            else:
                if x: 2
                else: 3
            """) == 3

    def test_break_statements_in_while_loops(self):
        # See discussion for "for" loops above.
        assert complexity(
            """
            while x:
                if x:
                    break
            """) == 3

    def test_break_statements_in_while_loops_with_else_clauses(self):
        # See discussion for for loops above.
        assert complexity(
            """
            while x:
                if x:
                    break
            else:
                pass
            """) == 3

    def test_continue_statement_in_while_loop(self):
        assert complexity(
            """
            while x:
                if x:
                    continue
            """) == 3


class describe_exception_handling:
    def test_try(self):
        assert complexity(
            """
            try: 1
            except: 2
            """) == 2

    def test_try_with_multiple_excepts(self):
        assert complexity(
            """
            try: 1
            except A: 2
            except B: 3
            except C: 4
            """) == 4

    def test_try_with_multiple_exception_types_in_one_except(self):
        assert complexity(
            """
            try: 1
            except (A, B): 2
            """) == 2

    def test_try_with_child_nodes(self):
        assert complexity(
            """
            try:
                if x: 1
                else: 2
            except: 2
            """) == 3

    def test_try_with_finally(self):
        assert complexity(
            """
            try: 1
            except: 2
            finally: 3
            """) == 2

    def test_try_with_else(self):
        assert complexity(
            """
            try: 1
            except: 2
            else: 3
            """) == 2

    def test_try_with_finally_and_child_nodes(self):
        # Try/finally/else/except are all deceiving. The try and finally don't
        # add any paths because they both always happen. An except adds one
        # (it can either happen or not), but an else doesn't (it's equivalent
        # to adding the code after the line in the try: that threw the
        # exception, so it doesn't add a path).
        assert complexity(
            """
            try:
                if a: 1
                else: 2
            except:
                if a: 1
                else: 2
            else:
                if a: 1
                else: 2
            finally:
                if a: 1
                else: 2
            """) == 6


class describe_integration:
    def test_multiple_ifs_in_a_for_loop(self):
        assert complexity(
            """
            for x in y:
                if x: pass
                # implicit else
                if y: pass
                # implicit else
            """) == 4


def complexity(code):
    return Complexity(dedent(code)).score

