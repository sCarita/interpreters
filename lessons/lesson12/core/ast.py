###############################################################################
#                                                                             #
#  ABSTRACT SYNTAX TREE OBJECTS                                               #
#                                                                             #
###############################################################################

class AST(object):
    pass

class BinOp(AST):
    def __init__(self, left=None, right=None, op=None):
        self.left = left
        self.token = self.op = op
        self.right = right

    def __str__(self):
        return ('BinOp('
            f'\n l={str(self.left)}, '
            f'\n r={str(self.right)}, '
            f'\n op={self.op.value}\n)'
        )

class UnaryOp(AST):
    def __init__(self, op, expr):
        # represents our unary operator
        self.token = self.op = op
        # represents another AST Token
        self.expr = expr

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __str__(self):
        return f'Num({self.value})'

class Assign(AST):
    def __init__(self, left, op, right):
        # Its left variable is for storing a Var node and
        # its right variable is for storing a node returned
        # by the expr parser method
        self.left = left
        self.token = self.op = op
        self.right = right

class Var(AST):
    """The Var node is constructed out of ID token."""
    def __init__(self, token):
        # The self.value holds the variable s name.
        self.token = token
        self.value = token.value

class NoOp(AST):
    """Represent an empty statement"""
    pass

class Compound(AST):
    """Represents a 'BEGIN ... END' block"""
    def __init__(self):
        self.children = []

class Program(AST):
    def __init__(self, name, block):
        self.name = name
        self.block = block

class Block(AST):
    def __init__(self, declarations, compound_statement):
        self.declarations = declarations
        self.compound_statement = compound_statement

class VarDecl(AST):
    def __init__(self, var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node

class Type(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class ProcedureDecl(AST):
    def __init__(self, proc_name, block_node):
        self.proc_name = proc_name
        self.block_node = block_node