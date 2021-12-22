import ast
import os

from core.visitors.node_visitor import NodeVisitor
from core.symbol import ScopedSymbolTable, VarSymbol, ProcedureSymbol
from core.errors.semantic import SemanticError
from core.errors.generic import ErrorCode


_SHOULD_LOG_SCOPE = ast.literal_eval(os.environ['_SHOULD_LOG_SCOPE'])


class SemanticAnalyzer(NodeVisitor):
    def __init__(self):
        self.current_scope = None
        pass

    def error(self, error_code, token):
        raise SemanticError(
            error_code=error_code,
            token=token,
            message=f'{error_code.value} -> {token}',
        )

    def log(self, msg):
        if _SHOULD_LOG_SCOPE:
            print(f'⓷ Semantics | {msg}')

    def visit_Assign(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_NoOp(self, node):
        pass

    def visit_Num(self, node):
        pass

    def visit_ProcedureCall(self, node):
        actual_params = node.actual_params
        procedure_decl = self.current_scope.lookup(node.proc_name)

        if procedure_decl == None:
            self.error(ErrorCode.ID_NOT_FOUND, node.token)

        if len(actual_params) != len(procedure_decl.formal_params):
            self.error(ErrorCode.INVALID_NUM_ARGS, node.token)

        for param_node in actual_params:
            self.visit(param_node)

        # accessed by the interpreter when executing procedure call
        print(procedure_decl)
        node.proc_symbol = procedure_decl

    def visit_ProcedureDecl(self, node):
        proc_name = node.proc_name
        proc_symbol = ProcedureSymbol(proc_name)
        self.current_scope.define(proc_symbol)

        self.log(f'ENTER scope: {proc_name}')
        # Scope for parameters and local variables
        procedure_scope = ScopedSymbolTable(
            name=proc_name,
            level=self.current_scope.scope_level + 1,
            enclosing_scope=self.current_scope
        )
        self.current_scope = procedure_scope

        # Insert parameters into the procedure scope
        self.log(node.params)
        for param in node.params:
            param_type = self.current_scope.lookup(param.type_node.value)
            param_name = param.var_node.value
            var_symbol = VarSymbol(param_name, param_type)

            self.current_scope.define(var_symbol)
            proc_symbol.formal_params.append(var_symbol)

        self.visit(node.block_node)

        self.current_scope = self.current_scope.enclosing_scope
        self.log('LEAVE scope: %s' %  proc_name)

        proc_symbol.block_ast = node.block_node

    def visit_Program(self, node):
        self.log('ENTER scope: global')
        global_scope = ScopedSymbolTable(
            name='global', level=1,
            enclosing_scope=self.current_scope
        )
        self.current_scope = global_scope

        self.visit(node.block)

        self.current_scope = self.current_scope.enclosing_scope
        self.log('LEAVE scope: global')

    def visit_UnaryOp(self, node):
        self.visit(node.expr)

    def visit_Var(self, node):
        var_name = node.value
        var_symbol = self.current_scope.lookup(var_name)

        if var_symbol is None:
            self.error(ErrorCode.ID_NOT_FOUND, node.token)

    def visit_VarDecl(self, node):
        type_name = node.type_node.value
        type_symbol = self.current_scope.lookup(type_name)

        # We have all the information we need to create a variable symbol.
        # Create the symbol and insert it into the symbol table.
        var_name = node.var_node.value
        var_symbol = VarSymbol(var_name, type_symbol)

        # Signal an error if the table alrady has a symbol
        # with the same name
        if self.current_scope.lookup(var_name, current_scope_only=True):
            self.error(ErrorCode.DUPLICATE_ID, node.var_node.token)

        self.current_scope.define(var_symbol)
