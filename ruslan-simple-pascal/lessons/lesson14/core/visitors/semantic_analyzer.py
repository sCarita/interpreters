from core.visitors.node_visitor import NodeVisitor
from core.symbol import ScopedSymbolTable, VarSymbol, ProcedureSymbol

class SemanticAnalyzer(NodeVisitor):
    def __init__(self):
        # self.scope = ScopedSymbolTable(name='global', level=1)
        pass

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

    def visit_ProcedureDecl(self, node):
        proc_name = node.proc_name
        proc_symbol = ProcedureSymbol(proc_name)
        self.current_scope.define(proc_symbol)

        print('ENTER scope: %s' %  proc_name)
        # Scope for parameters and local variables
        procedure_scope = ScopedSymbolTable(name=proc_name, level=2)
        self.current_scope = procedure_scope

        # Insert parameters into the procedure scope
        for param in node.params:
            param_type = self.current_scope.lookup(param.type_node.value)
            param_name = param.var_node.value
            var_symbol = VarSymbol(param_name, param_type)
            self.current_scope.define(var_symbol)
            proc_symbol.params.append(var_symbol)

        self.visit(node.block_node)

        print(procedure_scope)
        print('LEAVE scope: %s' %  proc_name)

    def visit_Program(self, node):
        print('ENTER scope: global')
        global_scope = ScopedSymbolTable(name='global', level=1)
        self.current_scope = global_scope

        self.visit(node.block)

        print(global_scope)
        print('LEAVE scope: global')

    def visit_UnaryOp(self, node):
        self.visit(node.expr)

    def visit_Var(self, node):
        var_name = node.value
        var_symbol = self.current_scope.lookup(var_name)
        if var_symbol is None:
            raise Exception(
                "SemanticError: Symbol(identifier) not found '%s'" % var_name
            )

    def visit_VarDecl(self, node):
        var_name = node.var_node.value

        type_name = node.type_node.value
        type_symbol = self.current_scope.lookup(type_name)

        var_sym = VarSymbol(var_name, type_symbol)

        # Signal an error if the table alrady has a symbol
        # with the same name
        if self.current_scope.lookup(var_name) is not None:
            raise Exception(
                "Semantic Error: Duplicate identifier '%s' found" % var_name
            )

        self.current_scope.define(var_sym)
