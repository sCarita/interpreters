import ast
import os

from core.ast import *
from core.errors.semantic import SemanticError
from core.errors.generic import ErrorCode
from core.symbol import (
    ScopedSymbolTable, VarSymbol, ProcedureSymbol, FunctionSymbol
)
from core.token import Token
from core.visitors.node_visitor import NodeVisitor


_SHOULD_LOG_SCOPE = ast.literal_eval(os.environ['_SHOULD_LOG_SCOPE'])


class SemanticAnalyzer(NodeVisitor):
    def __init__(self) -> None:
        self.current_scope: ScopedSymbolTable

    def error(self, error_code: ErrorCode, token: Token) -> SemanticError:
        raise SemanticError(
            error_code=error_code,
            token=token,
            message=f'{error_code.value} -> {token}',
        )

    def log(self, msg: str) -> None:
        if _SHOULD_LOG_SCOPE:
            print(f'⓷ Semantics | {msg}')

    def visit_BinOp(self, node: BinOp) -> None:
        self.visit(node.left)
        self.visit(node.right)

    def visit_Assign(self, node: Assign) -> None:
        self.visit(node.left)
        self.visit(node.right)

    def visit_Block(self, node: Block) -> None:
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_Compound(self, node: Compound) -> None:
        for child in node.children:
            self.visit(child)

    def visit_FunctionDecl(self, node: FunctionDecl) -> None:
        fn_name = node.fn_name
        return_type = node.return_type

        fn_symbol = FunctionSymbol(fn_name, return_type)
        self.current_scope.define(fn_symbol)

        self.log(f'ENTER scope: {fn_name}')
        # Scope for parameters and local variables
        procedure_scope = ScopedSymbolTable(
            name=fn_name,
            level=self.current_scope.scope_level + 1,
            enclosing_scope=self.current_scope
        )
        self.current_scope = procedure_scope

        # Insert parameters into the procedure scope
        self.log(f'{node.params}')
        for param in node.params:
            param_type = self.current_scope.lookup(param.type_node.value)
            param_name = param.var_node.value
            var_symbol = VarSymbol(param_name, param_type)

            self.current_scope.define(var_symbol)
            fn_symbol.formal_params.append(var_symbol)

        self.visit(node.block_node)

        self.current_scope = self.current_scope.enclosing_scope
        self.log(f'LEAVE scope: {fn_name}')

        fn_symbol.block_ast = node.block_node
        fn_symbol.return_type = node.return_type

    def visit_NoOp(self, node: NoOp) -> None:
        pass

    def visit_Num(self, node: Num) -> None:
        pass

    def visit_ProcedureCall(self, node: ProcedureCall) -> None:
        actual_params = node.actual_params
        procedure_decl = self.current_scope.lookup(node.proc_name)

        if procedure_decl == None:
            self.error(ErrorCode.ID_NOT_FOUND, node.token)

        if len(actual_params) != len(procedure_decl.formal_params):
            self.error(ErrorCode.INVALID_NUM_ARGS, node.token)

        for param_node in actual_params:
            self.visit(param_node)

        # accessed by the interpreter when executing procedure call
        node.proc_symbol = procedure_decl

    def visit_ProcedureDecl(self, node: ProcedureDecl) -> None:
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
        self.log(f'{node.params}')
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

    def visit_Program(self, node: Program) -> None:
        self.log('ENTER scope: global')
        global_scope = ScopedSymbolTable(
            name='global', level=1,
            enclosing_scope=None
        )
        self.current_scope = global_scope

        self.visit(node.block)

        self.current_scope = self.current_scope.enclosing_scope
        self.log('LEAVE scope: global')

    def visit_UnaryOp(self, node: UnaryOp) -> None:
        self.visit(node.expr)

    def visit_Var(self, node: Var) -> None:
        var_name = node.value
        var_symbol = self.current_scope.lookup(var_name)

        if var_symbol is None:
            self.error(ErrorCode.ID_NOT_FOUND, node.token)

    def visit_VarDecl(self, node: VarDecl) -> None:
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
