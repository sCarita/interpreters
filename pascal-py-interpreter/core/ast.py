###############################################################################
#                                                                             #
#  ABSTRACT SYNTAX TREE OBJECTS                                               #
#                                                                             #
###############################################################################
from typing import Union, List
from core.token import Token

class AST(object):
    pass

class Num(AST):
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value

class Var(AST):
    """The Var node is constructed out of ID token."""
    def __init__(self, token: Token) -> None:
        # The self.value holds the variable s name.
        self.token = token
        self.value = token.value

class UnaryOp(AST):
    def __init__(
        self,
        op: Token,
        expr: Union['UnaryOp', Num, Var, 'BinOp']
    ) -> None:
        # represents our unary operator
        self.token = self.op = op
        # represents another AST Token
        self.expr = expr

class BinOp(AST):
    def __init__(
        self,
        left: Union[UnaryOp, Num, Var, 'BinOp'],
        right: Union[UnaryOp, Num, Var, 'BinOp'],
        op: Token
    ) -> None:
        self.left = left
        self.token = self.op = op
        self.right = right

class Assign(AST):
    def __init__(
        self,
        left: Var,
        op: Token,
        right: Union[UnaryOp, Num, Var, BinOp]
    ) -> None:
        self.left = left
        self.token = self.op = op
        self.right = right

class Type(AST):
    def __init__(self, token: Token) -> None:
        self.token = token
        self.value = token.value

class VarDecl(AST):
    def __init__(self, var_node: Var, type_node: Type) -> None:
        self.var_node = var_node
        self.type_node = type_node

class NoOp(AST):
    """Represent an empty statement"""
    pass

class Param(AST):
    def __init__(self, var_node: Var, type_node: Type) -> None:
        self.var_node = var_node
        self.type_node = type_node

class ProcedureCall(AST):
    def __init__(
        self,
        proc_name: str,
        actual_params: List[Union[UnaryOp, Num, Var, BinOp]],
        token: Token
    ) -> None:
        self.proc_name = proc_name
        self.actual_params = actual_params  # a list of AST nodes
        self.token = token
        # a reference to procedure declaration symbol
        self.proc_symbol = None

class Compound(AST):
    """Represents a 'BEGIN ... END' block"""
    def __init__(self) -> None:
        self.children: List[Union[NoOp, Compound, ProcedureCall, Assign]]
        self.children = []

class ProcedureDecl(AST):
    def __init__(
        self,
        proc_name: str,
        params: List[Param],
        block_node: 'Block'
    ) -> None:
        self.proc_name = proc_name
        self.params = params # List of Param instances
        self.block_node = block_node

class FunctionDecl(AST):
    def __init__(
        self,
        fn_name: str,
        params: List[Param],
        block_node: 'Block',
        return_type: Type
    ) -> None:
        self.fn_name = fn_name
        self.params = params # List of Param instances
        self.block_node = block_node
        self.return_type = return_type

class Block(AST):
    def __init__(
        self,
        declarations: List[Union[VarDecl, ProcedureDecl, FunctionDecl]],
        compound_statement: Compound
    ) -> None:
        self.declarations = declarations
        self.compound_statement = compound_statement

class Program(AST):
    def __init__(self, name: str, block: Block) -> None:
        self.name = name
        self.block = block
