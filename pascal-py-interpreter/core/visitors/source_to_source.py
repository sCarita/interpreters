from core.visitors.node_visitor import NodeVisitor
from core.symbol import ScopedSymbolTable, VarSymbol, ProcedureSymbol

class Source2Source(NodeVisitor):
    def __init__(self):
        self.current_scope = None
        self.new_source = ''

    def tabs(self, n):
        return '  ' * n

    def visit_Assign(self, node):
        self.new_source += self.tabs(self.current_scope.scope_level + 1)
        self.visit(node.left)
        self.new_source += ' := '
        self.visit(node.right)
        self.new_source += ';\n'

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.new_source += f' {node.op.value} '
        self.visit(node.right)

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.new_source += '\n'
        self.visit(node.compound_statement)

    def visit_Compound(self, node):
        self.new_source += self.tabs(self.current_scope.scope_level - 1)
        self.new_source += 'begin\n'

        for child in node.children:
            self.visit(child)

        if len(node.children) == 1:
            self.new_source += '\n'

        self.new_source += self.tabs(self.current_scope.scope_level - 1)
        self.new_source += 'end;\n'

    def visit_NoOp(self, node):
        pass

    def visit_Num(self, node):
        self.new_source += f'{node.value}'

    def visit_ProcedureDecl(self, node):
        proc_name = node.proc_name
        proc_symbol = ProcedureSymbol(proc_name)
        self.current_scope.define(proc_symbol)

        # Scope for parameters and local variables
        procedure_scope = ScopedSymbolTable(
            name=proc_name,
            level=self.current_scope.scope_level+1,
            enclosing_scope=self.current_scope
        )
        self.current_scope = procedure_scope

        # Insert parameters into the procedure scope
        aux_new_source = ''
        for param in node.params:
            param_type = self.current_scope.lookup(param.type_node.value)
            param_name = param.var_node.value
            var_symbol = VarSymbol(param_name, param_type)
            self.current_scope.define(var_symbol)
            proc_symbol.params.append(var_symbol)

            aux_new_source += f'{var_symbol.name} : {var_symbol.type},'
        aux_new_source = aux_new_source[:-1]

        self.new_source += self.tabs(self.current_scope.enclosing_scope.scope_level)
        self.new_source += (
            f'procedure {proc_symbol.name}'
            f'{self.current_scope.enclosing_scope.scope_level}'
            f'({aux_new_source});\n'
        )

        self.visit(node.block_node)
        self.current_scope = self.current_scope.enclosing_scope
        self.new_source = f'{self.new_source[:-1]}'
        self.new_source += f' {{END OF {node.proc_name}}}\n'

    def visit_Program(self, node):
        global_scope = ScopedSymbolTable(
            name='global', level=1,
            enclosing_scope=self.current_scope
        )
        self.current_scope = global_scope

        self.new_source += f'program {node.name}0;\n'

        self.visit(node.block)
        self.current_scope = self.current_scope.enclosing_scope

        self.new_source = f'{self.new_source[:-2]}. {{END OF {node.name}}}'

    def visit_UnaryOp(self, node):
        self.visit(node.expr)

    def visit_Var(self, node):
        var_name = node.value
        var_symbol, level = self.current_scope.lookup(var_name, with_scope=True)

        if var_symbol is None:
            raise Exception(
                f"SemanticError: Symbol(identifier) not found '{var_name}'"
            )

        self.new_source += f'<{var_symbol.name}{level}:{var_symbol.type}>'

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
            raise Exception(
                "Error: Duplicate identifier '%s' found" % var_name
            )

        self.current_scope.define(var_symbol)

        self.new_source += self.tabs(self.current_scope.scope_level)
        self.new_source += (
            f'var {var_symbol.name}{self.current_scope.scope_level}'
            f' : {var_symbol.type};\n'
        )

