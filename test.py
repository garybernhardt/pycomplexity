from textwrap import dedent

from complexity import Complexity


class describe_simple_statements:
    def test_pass(self):
        assert complexity('pass').score == 1

    def test_statement_sequence(self):
        assert complexity(
            """
            pass
            pass
            """).score == 1

    def test_constant(self):
        assert complexity("1").score == 1

    def test_assignment(self):
        assert complexity("x = 1").score == 1

    def test_name(self):
        assert complexity("a").score == 1

    def test_sequence_of_names(self):
        assert complexity(
            """
            a
            b
            c
            """).score == 1

    def test_logical_operators(self):
        assert complexity('a and b or (c or d and not e)').score == 1


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


class describe_exception_handling:
    def test_try(self):
        assert complexity(
            """
            try: 1
            except: 2
            """).score == 2

    def test_try_with_multiple_excepts(self):
        assert complexity(
            """
            try: 1
            except A: 2
            except B: 3
            except C: 4
            """).score == 4

    def test_try_with_multiple_exception_types_in_one_except(self):
        assert complexity(
            """
            try: 1
            except (A, B): 2
            """).score == 2

    def test_try_with_child_nodes(self):
        assert complexity(
            """
            try:
                if x: 1
                else: 2
            except: 2
            """).score == 3

    def test_try_with_finally(self):
        assert complexity(
            """
            try: 1
            except: 2
            finally: 3
            """).score == 2

    def test_try_with_else(self):
        assert complexity(
            """
            try: 1
            except: 2
            else: 3
            """).score == 2

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
            """).score == 6


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


class describe_functions:
    def test_that_they_are_scored(self):
        assert complexity(
            """
            def foo():
                0 if x else 1
            """).stats[0].score == 2
        assert complexity(
            """
            def foo():
                0 if x else 1 if y else 2
            """).stats[0].score == 3

    def test_that_they_know_their_names(self):
        assert complexity(
            """
            def foo(): pass
            """).stats[0].name == 'foo'

    def test_that_they_know_their_line_range(self):
        stats = complexity("def foo(): pass").stats[0]
        assert stats.start_line == 1
        assert stats.end_line == 1

        stats = complexity(
            """
            def foo(): pass
            """).stats[0]
        assert stats.start_line == 2
        assert stats.end_line == 2


class describe_classes:
    def test_that_they_are_scored(self):
        assert complexity(
            """
            class Foo:
                0 if x else 1
            """).stats[0].score == 2
        assert complexity(
            """
            class Foo:
                0 if x else 1 if y else 2
            """).stats[0].score == 3

    def test_that_they_know_their_names(self):
        assert complexity(
            """
            class Foo: pass
            """).stats[0].name == 'Foo'

    def test_that_they_know_their_line_range(self):
        stats = complexity("class Foo: pass").stats[0]
        assert stats.start_line == 1
        assert stats.end_line == 1

        stats = complexity(
            """
            class Foo:
                pass
            """).stats[0]
        assert stats.start_line == 2
        assert stats.end_line == 3

    def test_that_they_include_code_interspersed_with_methods(self):
        stats = complexity(
            """
            class Foo:
                0 if x else 1
                def foo(self): pass
                0 if x else 1
            """).stats[0]
        assert stats.score == 3
        assert stats.end_line == 5



class describe_methods:
    def test_that_they_are_scored(self):
        assert complexity(
            """
            class Foo:
                def foo():
                    0 if x else 1
            """).stats[1].score == 2
        assert complexity(
            """
            class Foo:
                def foo():
                    0 if x else 1 if y else 2
            """).stats[1].score == 3

    def test_that_they_know_their_names(self):
        assert complexity(
            """
            class Foo:
                def foo(): pass
            """).stats[1].name == 'Foo.foo'

    def test_that_they_know_their_line_range(self):
        stats = complexity(
            """
            class Foo():
                def foo():
                    pass
            """).stats[1]
        assert stats.start_line == 3
        assert stats.end_line == 4

        stats = complexity(
            """
            pass
            class Foo:
                def foo():
                    pass
                    pass
            """).stats[1]
        assert stats.start_line == 4
        assert stats.end_line == 6


class describe_integration:
    def test_multiple_ifs_in_a_for_loop(self):
        assert complexity(
            """
            for x in y:
                if x: pass
                # implicit else
                if y: pass
                # implicit else
            """).score == 4

    def test_a_big_hairy_mess(self):
        assert complexity(
            """
            while True: #1
                if x and y or (z and w): #4
                    try:
                        x or y
                        raise x
                    except: #1
                        5
                    finally:
                        break
                else:
                    [x for x in [x and y for x in y if z or w]] #5
                try:
                    return
                except A: #1
                    return
                except B: #1
                    (y for y in z) #1
                finally:
                    raise (x for x in z) #1
            """).score == 15


def complexity(code):
    return Complexity(dedent(code))

