###################################################
#                                                 #
#      GRAMMAR                                    #
#                                                 #
###################################################

#    program : PROGRAM variable SEMI block DOT
#
#    block : declarations compound_statement
#
#    declarations : VAR (variable_declaration SEMI)+
#                 | empty
#
#    variable_declaration : ID (COMMA ID)* COLON type_spec
#
#    type_spec : INTEGER | REAL
#
#    compound_statement : BEGIN statement_list END
#
#    statement_list : statement
#                   | statement SEMI statement_list
#
#    statement : compound_statement
#              | assignment_statement
#              | empty
#
#    assignment_statement : variable ASSIGN expr
#
#    empty :
#
#    expr : term ((PLUS | MINUS) term)*
#
#    term : factor ((MUL | INTEGER_DIV | FLOAT_DIV) factor)*
#
#    factor : PLUS factor
#           | MINUS factor
#           | INTEGER_CONST
#           | REAL_CONST
#           | LPAREN expr RPAREN
#           | variable
#
#    variable: ID

from core.visitors.node_visitor import NodeVisitor
from core.token import *

class Interpreter(NodeVisitor):
    def __init__(self, tree):
        self.tree = tree
        self.GLOBAL_SCOPE = {}

    def visit_Num(self, node):
        return node.value

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == INTEGER_DIV:
            return self.visit(node.left) // self.visit(node.right)
        elif node.op.type == FLOAT_DIV:
            return float(self.visit(node.left)) / float(self.visit(node.right))
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)

    def visit_UnaryOp(self, node):
        if node.op.type == PLUS:
            return +self.visit(node.expr)
        elif node.op.type == MINUS:
            return -self.visit(node.expr)

    def visit_Compound(self, node):
        for n in node.children:
            self.visit(n)

    def visit_Assign(self, node):
        self.GLOBAL_SCOPE[node.left.value] = self.visit(node.right)

    def visit_Var(self, node):
        val = self.GLOBAL_SCOPE.get(node.value)
        if val is None:
            raise NameError(repr(node.value))
        else:
            return val

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_VarDecl(self, node):
        # Do nothing
        pass

    def visit_Type(self, node):
        # Do nothing
        pass

    def visit_Program(self, node):
        self.visit(node.block)

    def visit_NoOp(self, node):
        pass

    def interpret(self):
        tree = self.tree
        if tree is None:
            return ''
        return self.visit(tree)