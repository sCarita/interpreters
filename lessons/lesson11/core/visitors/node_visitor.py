class NodeVisitor(object):
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.undefined_visit)
        return visitor(node)

    def undefined_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')