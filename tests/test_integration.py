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
            """).stats[0].score == 3

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

