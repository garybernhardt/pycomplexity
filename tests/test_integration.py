from tests.utils import complexity


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

    def test_lambdas_in_a_function(self):
        assert complexity(
            """
            def foo():
                x = lambda: x if x else x
                y if y else y
            """).stats.named('foo').score == 3

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

    def test_module_stat_comes_before_function_stat(self):
        stats = complexity("def foo(): pass\npass").stats
        stat_names = [stat.name for stat in stats.ordered_by_line()]
        assert stat_names == ['<module>', 'foo']

    def test_class_stat_comes_before_module_stat(self):
        stats = complexity("class Foo: pass\npass").stats
        stat_names = [stat.name for stat in stats.ordered_by_line()]
        assert stat_names == ['<module>', 'Foo']

