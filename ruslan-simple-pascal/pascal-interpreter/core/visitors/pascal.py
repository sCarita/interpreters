import os

from core.visitors.node_visitor import NodeVisitor
from core.token import TokenType
from core.stack import Stack
from core.activation_record import ActivationRecord, ARType

_SHOULD_LOG_STACK = os.environ['_SHOULD_LOG_STACK']

class Interpreter(NodeVisitor):
    def __init__(self, tree):
        self.tree = tree
        self.call_stack = Stack()

    def log(self, msg):
        if _SHOULD_LOG_STACK:
            print(f'⓸ Interpreter | {msg}')

    def visit_Assign(self, node):
        ar = self.call_stack.peek()
        var_name = node.left.value
        var_value = self.visit(node.right)

        ar[var_name] = var_value

    def visit_BinOp(self, node):
        if node.op.type == TokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == TokenType.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == TokenType.INTEGER_DIV:
            return self.visit(node.left) // self.visit(node.right)
        elif node.op.type == TokenType.FLOAT_DIV:
            return float(self.visit(node.left)) / float(self.visit(node.right))
        elif node.op.type == TokenType.MUL:
            return self.visit(node.left) * self.visit(node.right)

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_Compound(self, node):
        for n in node.children:
            self.visit(n)

    def visit_NoOp(self, node):
        pass

    def visit_Num(self, node):
        return node.value

    def visit_ProcedureCall(self, node):
        proc_name = node.proc_name
        formal_params = node.proc_symbol.formal_params
        actual_params = node.actual_params

        ar = ActivationRecord(
            proc_name,
            ARType.PROCEDURE,
            nesting_level=node.proc_symbol.scope_level + 1
        )
        for f_p, a_p in zip(formal_params, actual_params):
            ar[f_p.name] = self.visit(a_p)

        self.call_stack.push(ar)

        self.log(f'ENTER: PROCEDURE {proc_name}')
        self.log(str(self.call_stack))

        self.visit(node.proc_symbol.block_ast)

        self.log(f'LEAVE: PROCEDURE {proc_name}')
        self.log(str(self.call_stack))

        self.call_stack.pop()


    def visit_ProcedureDecl(self, node):
        pass

    def visit_Program(self, node):
        prog_name = node.name
        self.log(f'ENTER: PROGRAM {prog_name}')

        ar = ActivationRecord(
            name=prog_name,
            type=ARType.PROGRAM,
            nesting_level=1,
        )
        self.call_stack.push(ar)

        self.log(str(self.call_stack))

        self.visit(node.block)

        self.log(f'LEAVE: PROGRAM {prog_name}')
        self.log(str(self.call_stack))

        self.call_stack.pop()

    def visit_Type(self, node):
        # Do nothing
        pass

    def visit_UnaryOp(self, node):
        if node.op.type == TokenType.PLUS:
            return +self.visit(node.expr)
        elif node.op.type == TokenType.MINUS:
            return -self.visit(node.expr)

    def visit_Var(self, node):
        ar = self.call_stack.peek()
        var_name = node.value
        val = ar.get(var_name)

        if val is None:
            raise NameError(repr(node.value))
        else:
            return val

    def visit_VarDecl(self, node):
        # Do nothing
        pass

    def interpret(self):
        tree = self.tree
        if tree is None:
            return ''
        return self.visit(tree)