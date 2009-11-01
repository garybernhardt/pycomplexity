import pprint
import compiler
from compiler.visitor import ASTVisitor


class Stats(object):

    def __init__(self, name):
        self.name = name
        self.classes = []
        self.functions = []
        self.complexity = 1

    def __str__(self):
        return 'Stats: name=%r, classes=%r, functions=%r, complexity=%r' \
                % (self.name, self.classes, self.functions, self.complexity)

    __repr__ = __str__


class ClassStats(Stats):

    def __str__(self):
        return 'Stats: name=%r, methods=%r, complexity=%r, inner_class=%r' \
                % (self.name, self.functions, self.complexity, self.classes)

    __repr__ = __str__


class DefStats(Stats):
    def __init__(self, name, first_line, last_line):
        super(DefStats, self).__init__(name)
        self.first_line = first_line
        self.last_line = last_line

    def __str__(self):
        return 'DefStats: name=%r, complexity=%r' \
                % (self.name, self.complexity)

    __repr__ = __str__


class CCVisitor(ASTVisitor):
    """Encapsulates the cyclomatic complexity counting."""

    def __init__(self, ast, stats=None, description=None):
        ASTVisitor.__init__(self)
        if isinstance(ast, basestring):
            ast = compiler.parse(ast)

        self.stats = stats or Stats(description or '<module>')
        for child in ast.getChildNodes():
            compiler.walk(child, self, walker=self)

    def dispatchChildren(self, node):
        for child in node.getChildNodes():
            self.dispatch(child)

    def visitFunction(self, node):
        if not hasattr(node, 'name'): # lambdas
            node.name = '<lambda>'
        stats = DefStats(node.name,
                         node.lineno,
                         self.highest_line_in_node(node))
        stats = CCVisitor(node, stats).stats
        self.stats.functions.append(stats)

    def highest_line_in_node(self, node, highest=0):
        children = node.getChildNodes()
        if node.lineno > highest:
            highest = node.lineno
        child_lines = map(self.highest_line_in_node,
                       node.getChildNodes())
        lines = [node.lineno] + child_lines
        return max(lines)

    visitLambda = visitFunction

    def visitClass(self, node):
        stats = ClassStats(node.name)
        stats = CCVisitor(node, stats).stats
        self.stats.classes.append(stats)

    def visitIf(self, node):
        self.stats.complexity += len(node.tests)
        self.dispatchChildren(node)

    def __processDecisionPoint(self, node):
        self.stats.complexity += 1
        self.dispatchChildren(node)

    visitFor = visitGenExprFor = visitGenExprIf \
            = visitListCompFor = visitListCompIf \
            = visitWhile = _visitWith = __processDecisionPoint

    def visitAnd(self, node):
        self.dispatchChildren(node)
        self.stats.complexity += 1

    def visitOr(self, node):
        self.dispatchChildren(node)
        self.stats.complexity += 1


def debug(fn):
    def new_fn(self, *args):
        result = fn(self, *args)
        print 'called %s with %s and got %s' % (fn.__name__,
                                                repr(args),
                                                repr(result))
        return result
    return new_fn


class Complexity:
    EMPTY_NODE_SCORE = 1
    IMPLICIT_ELSE_SCORE = EMPTY_NODE_SCORE

    def __init__(self, code):
        ast = compiler.parse(code)
        self.score = self.score_node(ast.node)

    def score_node(self, node):
        node_type = node.__class__.__name__
        node_function = getattr(self, 'score_%s' % node_type.lower())
        return node_function(node)

    @debug
    def score_stmt(self, node):
        return max(self.EMPTY_NODE_SCORE,
                   sum(self.score_node(node)
                   for node in node.getChildNodes()))

    @debug
    def score_pass(self, node):
        return 0

    @debug
    def score_discard(self, node):
        print dir(node)
        return 0

    @debug
    def score_if(self, node):
        test_scores = sum(self.score_node(statement)
                          for condition, statement in node.tests)
        if node.else_ is None:
            else_score = self.IMPLICIT_ELSE_SCORE
        else:
            else_score = self.score_node(node.else_)
        return test_scores + else_score

    @debug
    def score_for(self, node):
        body_score = self.score_node(node.body)
        if node.else_ is None:
            else_score = self.IMPLICIT_ELSE_SCORE
        else:
            else_score = self.score_node(node.else_)
        return body_score + else_score


def measure_complexity(ast, module_name=None):
    return CCVisitor(ast, description=module_name).stats


class Table(object):

    def __init__(self, headings, rows):
        self.headings = headings
        self.rows = rows

        max_col_sizes = [len(x) for x in headings]
        for row in rows:
            for i, col in enumerate(row):
                max_col_sizes[i] = max(max_col_sizes[i], len(str(col)))
        self.max_col_sizes = max_col_sizes

    def __iter__(self):
        for row in self.rows:
            yield row

    def __nonzero__(self):
        return len(self.rows)


class PrettyPrinter(object):
    def flatten_stats(self, stats):
        def flatten(stats):
            for s in stats.classes:
                name = s.name
                for x in s.functions:
                    fname = '.'.join([name, x.name])
                    yield fname, x.complexity, x.first_line, x.last_line
            for s in stats.functions:
                name = s.name
                yield name, s.complexity, s.first_line, s.last_line

        return [t for t in flatten(stats)]


def complexity_name(complexity):
    if complexity > 14:
        return 'high_complexity'
    elif complexity > 7:
        return 'medium_complexity'
    else:
        return 'low_complexity'


def show_complexity():
    import vim

    current_file = vim.eval('expand("%:p")')
    code = open(current_file).read()
    try:
        lines = PrettyPrinter().flatten_stats(
        measure_complexity(code, current_file))
    except (IndentationError, SyntaxError):
        return

    vim.command('sign unplace *')

    for name, complexity, start, end in lines:
        complexity = complexity_name(complexity)
        for line in range(start, end + 1):
            vim.command(':sign place %i line=%i name=%s file=%s' %
                        (line, line, complexity, vim.eval('expand("%:p")')))

