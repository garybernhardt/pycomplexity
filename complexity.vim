" complexity.vim
" Gary Bernhardt (http://blog.extracheese.org)
"
" This will add cyclomatic complexity annotations to your source code. It is
" no longer wrong (as previous versions were!)

if !has('signs')
    finish
endif
if !has('python')
    finish
endif
python << endpython
import vim
#!/usr/bin/env python
from tempfile import mkstemp
import sys
import os
import compiler#{{{
from compiler.visitor import ASTVisitor

def compute_code_complexity(code):
    return ModuleComplexity(code).compute_complexity()

#}}}

class ASTComplexity(ASTVisitor):
    def __init__(self, node):
        ASTVisitor.__init__(self)
        self.score = 1
        self._in_conditional = False
        self.results = ComplexityResults()
        self.process_root_node(node)

    def process_root_node(self, node):
        for child in node.getChildNodes():
            compiler.walk(child, self, walker=self)

    def dispatch_children(self, node):#{{{
        for child in node.getChildNodes():
            self.dispatch(child)

    def visitFunction(self, node):
        score=ASTComplexity(node).score
        score = ComplexityScore(name=node.name,
                                type_='function',
                                score=score,
                                start_line=node.lineno,
                                end_line=self.highest_line_in_node(node))
        self.results.add(score)

    def visitClass(self, node):
        complexity = ASTComplexity(node)
        self.results.add(ComplexityScore(
            name=node.name,
            type_='class',
            score=complexity.score,
            start_line=node.lineno,
            end_line=self.highest_line_in_node(node)))
        for score in complexity.results.ordered_by_line():
            score.name = '%s.%s' % (node.name, score.name)
            self.results.add(score)

    def highest_line_in_node(self, node, highest=0):
        children = node.getChildNodes()
        if node.lineno > highest:
            highest = node.lineno
        child_lines = map(self.highest_line_in_node,
                          node.getChildNodes())
        lines = [node.lineno] + child_lines
        return max(lines)

    def visitIf(self, node):
        tests = self._tests_for_if(node)
        self.score += len(tests)
        self._in_conditional = True
        for test in tests:
            self.dispatch(test)
        self._in_conditional = False
        self.dispatch_children(node)

    def _tests_for_if(self, if_node):
        try:
            return [test for test, body in if_node.tests]
        except AttributeError:
            return [if_node.test]

    visitGenExprIf = visitListCompIf = visitIfExp = visitIf

    def __processDecisionPoint(self, node):
        self.score += 1
        self.dispatch_children(node)

    visitFor = visitGenExprFor \
            = visitListCompFor \
            = visitWhile = __processDecisionPoint

    def _visit_logical_operator(self, node):
        self.dispatch_children(node)
        if self._in_conditional:
            self.score += len(node.getChildren()) - 1

    visitAnd = _visit_logical_operator
    visitOr = _visit_logical_operator

    def visitTryExcept(self, node):
        self.dispatch_children(node)
        self.score += len(node.handlers)
#}}}

class ModuleComplexity:
    def __init__(self, code):
        self.code = code
        self.node = compiler.parse(code)

    def compute_complexity(self):
        complexity = ASTComplexity(self.node)
        self.add_module_results(complexity, self.code)
        return complexity

    def add_module_results(self, complexity, code_or_node):
        end_line = max(1, code_or_node.count('\n') + 1)
        complexity.results.add(
            ComplexityScore(name='<module>',
                            type_='module',
                            score=complexity.score,
                            start_line=1,
                            end_line=end_line))

class ComplexityResults:#{{{
    def __init__(self):
        self._scores = []

    def add(self, score):
        self._scores.append(score)

    def ordered_by_line(self):
        OBJECT_SORT_PRIORITY = ['module', 'function', 'class']
        def sort_key(score):
            return (score.start_line,
                    OBJECT_SORT_PRIORITY.index(score.type_))
        return sorted(self._scores, key=sort_key)

    def named(self, name):
        return [s for s in self._scores if s.name == name][0]


class ComplexityScore:
    def __init__(self, name, type_, score, start_line, end_line):
        self.name = name
        self.type_ = type_
        self.score = score
        self.start_line = start_line
        self.end_line = end_line

    def __repr__(self):
        return (
            'ComplexityScore(name=%s, score=%s, start_line=%s, end_line=%s)'
            % (repr(self.name),
               repr(self.score),
               repr(self.start_line),
               repr(self.end_line)))


def complexity_name(complexity):
    if complexity > 14:
        return 'high_complexity'
    elif complexity > 7:
        return 'medium_complexity'
    else:
        return 'low_complexity'


def show_complexity():
    current_file = vim.current.buffer.name
    try:
        scores = compute_scores_for(current_file)
    except (IndentationError, SyntaxError):
        return

    old_complexities = get_old_complexities(current_file)
    new_complexities = compute_new_complexities(scores)
    line_changes = compute_line_changes(old_complexities, new_complexities)
    update_line_markers(line_changes)


def compute_scores_for(filename):
    code = open(filename).read()
    scores = compute_code_complexity(code).results.ordered_by_line()
    return scores


def get_old_complexities(current_file):
    lines = list_current_signs(current_file)

    old_complexities = {}
    for line in lines:
        if '=' not in line:
            continue

        tokens = line.split()
        variables = dict(token.split('=') for token in tokens)
        line = int(variables['line'])
        complexity = variables['name']
        old_complexities[line] = complexity

    return old_complexities


def list_current_signs(current_file):
    vim.command('redir => s:complexity_sign_list')
    vim.command('silent sign place file=%s' % current_file)
    vim.command('redir END')

    sign_list = vim.eval('s:complexity_sign_list')
    lines = [line.strip() for line in sign_list.split('\n')]
    return lines


def compute_line_changes(cached_complexities, new_scores):
    changes = {}
    for line, complexity in new_scores.iteritems():
        if complexity != cached_complexities.get(line, None):
            changes[line] = complexity

    return changes


def compute_new_complexities(scores):
    new_scores = {}
    for score in scores:
        for line in range(score.start_line, score.end_line + 1):
            new_scores[line] = complexity_name(score.score)
    return new_scores


def update_line_markers(line_changes):
    filename = vim.current.buffer.name
    for line, complexity in line_changes.iteritems():
        vim.command(':sign unplace %i' % line)
        vim.command(':sign place %i line=%i name=%s file=%s' %
                    (line, line, complexity, filename))#}}}


def main():
    if sys.stdin.isatty() and len(sys.argv) < 2:
        print "Missing filename"
        return

    temporary_file = None
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        content = sys.stdin.read()
        temporary_fd, file_name = mkstemp()
        temporary_file = os.fdopen(temporary_fd, "w")
        temporary_file.write(content)
        temporary_file.close()

    try:
        for score in compute_scores_for(file_name):
            print score.start_line, score.end_line, score.score, score.type_
    except:
        pass
    finally:
        if temporary_file is not None:
            os.unlink(file_name)


if __name__ == '__main__':
    main()

endpython

function! ShowComplexity()
    python << END
show_complexity()
END
" no idea why it is needed to update colors each time
" to actually see the colors
hi low_complexity guifg=#004400 guibg=#004400
hi medium_complexity guifg=#bbbb00 guibg=#bbbb00
hi high_complexity guifg=#ff2222 guibg=#ff2222
endfunction

hi SignColumn guifg=fg guibg=bg
hi low_complexity guifg=#004400 guibg=#004400
hi medium_complexity guifg=#bbbb00 guibg=#bbbb00
hi high_complexity guifg=#ff2222 guibg=#ff2222
sign define low_complexity text=XX texthl=low_complexity
sign define medium_complexity text=XX texthl=medium_complexity
sign define high_complexity text=XX texthl=high_complexity

autocmd! BufReadPost,BufWritePost,FileReadPost,FileWritePost *.py call ShowComplexity()

