import ast
import os

from typing import OrderedDict


_SHOULD_LOG_SCOPE = ast.literal_eval(os.environ['_SHOULD_LOG_SCOPE'])


class Symbol(object):
    def __init__(self, name, type=None, category=None):
        self.name = name
        self.type = type
        self.category = category
        self.scope_level = 0

class BuiltinTypeSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<{class_name}(name='{name}')>".format(
            class_name=self.__class__.__name__,
            name=self.name,
        )

class VarSymbol(Symbol):
    def __init__(self, name, type):
        super().__init__(name, type)

    def __str__(self):
        return '<{name}:{type}>'.format(name=self.name, type=self.type)

    __repr__ = __str__

class ProcedureSymbol(Symbol):
    def __init__(self, name, params=None):
        super(ProcedureSymbol, self).__init__(name)
        # a list of formal parameters
        self.formal_params = params if params is not None else []
        # a reference to procedure's body (AST sub-tree)
        self.block_ast = None

    def __str__(self):
        return '<{class_name}(name={name}, parameters={params})>'.format(
            class_name=self.__class__.__name__,
            name=self.name,
            params=self.formal_params,
        )

    __repr__ = __str__

class ScopedSymbolTable(object):
    def __init__(self, level, name, enclosing_scope=None):
        self._symbols = OrderedDict()
        self.scope_level = level
        self.scope_name = name
        self.enclosing_scope = enclosing_scope
        if self.enclosing_scope == None:
            self._init_builtin()

    def log(self, msg):
        if _SHOULD_LOG_SCOPE:
            print(f'  {msg}')

    def _init_builtin(self):
        self.define(BuiltinTypeSymbol('INTEGER'))
        self.define(BuiltinTypeSymbol('REAL'))

    def __str__(self):
        h1 = 'SCOPE (SCOPED SYMBOL TABLE)'
        lines = ['\n', h1, '=' * len(h1)]
        for header_name, header_value in (
            ('Scope name', self.scope_name),
            ('Scope level', self.scope_level),
            (
                'Enclosing scope',
                self.enclosing_scope.scope_name if self.enclosing_scope else None
            )
        ):
            lines.append('%-15s: %s' % (header_name, header_value))
        h2 = 'Scope (Scoped symbol table) contents'
        lines.extend([h2, '-' * len(h2)])
        lines.extend(
            ('%7s: %r' % (key, value))
            for key, value in self._symbols.items()
        )
        lines.append('\n')
        s = '\n'.join(lines)
        return s

    __repr__ = __str__

    def define(self, symbol):
        self.log(f'Define: {symbol}')
        symbol.scope_level = self.scope_level

        self._symbols[symbol.name] = symbol

    def lookup(self, name, current_scope_only=False, with_scope=None):
        self.log(f'Lookup: {name}. (Scope name: {self.scope_name})')
        symbol = self._symbols.get(name)

        # 'symbol' is either an instance of the Symbol class or 'None'
        if symbol != None:
            if with_scope:
                return symbol, self.scope_level
            else:
                return symbol

        if current_scope_only:
            return None

        # recursively go up the chain and lookup the name
        if self.enclosing_scope is not None:
            return self.enclosing_scope.lookup(name, with_scope=with_scope)
