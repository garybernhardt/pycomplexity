import compiler
from compiler.visitor import ASTVisitor


class NodeVisitor(ASTVisitor):
    def __init__(self, code, stats=None, description=None):
        ASTVisitor.__init__(self)
        ast = compiler.parse(code)
        self.node_types = set()
        self.visit_node(ast.node)
        #for child in ast.getChildNodes():
            #compiler.walk(child, self, walker=self)
        all_types = set(line.strip()
                        for line
                        in file('python_ast_node_types.txt').readlines())
        self.untouched_nodes = sorted(all_types - self.node_types)

    def visit_node(self, node):
        self.node_types.add(node.__class__.__name__)
        for child in node.getChildNodes():
            self.visit_node(child)


visitor = NodeVisitor(file('everything.py').read())
print 'Nodes not touched: %s' % visitor.untouched_nodes

