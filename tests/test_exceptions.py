from tests.utils import complexity


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

