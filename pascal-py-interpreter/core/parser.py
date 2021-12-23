from core.ast import *
from core.token import TokenType, Token
from core.errors.parser import ParserError
from core.errors.generic import ErrorCode
from core.lexer import Lexer

from typing import Union, List, Sequence

class Parser(object):

    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self, error_code: ErrorCode, token: Token) -> ParserError:
        raise ParserError(
            error_code=error_code,
            token=token,
            message=f'{error_code.value} -> {token}',
        )

    def eat(self, token_type: TokenType) -> None:
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(
                error_code=ErrorCode.UNEXPECTED_TOKEN,
                token=self.current_token
            )

    def factor(self) -> Union[UnaryOp, Num, Var, BinOp]:
        """factor : PLUS factor
                  | MINUS factor
                  | INTEGER_CONST
                  | REAL_CONST
                  | LPAREN expr RPAREN
                  | variable"""
        token = self.current_token

        if token.type in (TokenType.MINUS, TokenType.PLUS):
            self.eat(token.type)
            return UnaryOp(token, self.factor())
        elif token.type == TokenType.INTEGER_CONST:
            self.eat(TokenType.INTEGER_CONST)
            return Num(token)
        elif token.type == TokenType.REAL_CONST:
            self.eat(TokenType.REAL_CONST)
            return Num(token)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            subtree = self.expr()
            self.eat(TokenType.RPAREN)
            return subtree
        else:
            return self.variable()

    def term(self) -> Union[UnaryOp, Num, Var, BinOp]:
        """term : factor ((MUL | INTEGER_DIV | FLOAT_DIV) factor)*"""
        node = self.factor()

        while self.current_token.type in (
            TokenType.MUL, TokenType.INTEGER_DIV, TokenType.FLOAT_DIV
        ):
            token = self.current_token

            if token.type == TokenType.MUL:
                self.eat(TokenType.MUL)
            elif token.type == TokenType.INTEGER_DIV:
                self.eat(TokenType.INTEGER_DIV)
            elif token.type == TokenType.FLOAT_DIV:
                self.eat(TokenType.FLOAT_DIV)

            node = BinOp(left=node, right=self.factor(), op=token)

        return node

    def expr(self) -> Union[UnaryOp, Num, Var, BinOp]:
        """Arithmetic expression parser / interpreter.

        calc> 7 + 3 * (10 / (12 / (3 + 1) - 1))
        22

        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : (PLUS | MINUS)factor| INTEGER | LPAREN expr RPAREN
        """
        node = self.term()

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)

            node = BinOp(left=node, right=self.term(), op=token)

        return node

    def empty(self) -> NoOp:
        """
        empty :
        """
        return NoOp()

    def variable(self) -> Var:
        """
        variable: ID
        """
        node = Var(self.current_token)
        self.eat(TokenType.ID)
        return node

    def assignment_statement(self) -> Assign:
        """
        assignment_statement : variable ASSIGN expr
        """
        var = self.variable()

        token = self.current_token
        self.eat(TokenType.ASSIGN)

        expr = self.expr()
        return Assign(var, token, expr)

    def compound_statement(self) -> Compound:
        """compound_statement : BEGIN statement_list END"""
        self.eat(TokenType.BEGIN)
        nodes = self.statement_list()
        self.eat(TokenType.END)

        root = Compound()
        for node in nodes:
            root.children.append(node)

        return root

    def procall_statement(self) -> ProcedureCall:
        """
        proccall_statement : ID LPAREN (expr (COMMA expr)*)? RPAREN
        """
        actual_params = []
        token = self.current_token
        proc_name = f'{token.value}'

        self.eat(TokenType.ID)
        self.eat(TokenType.LPAREN)

        if self.current_token.type != TokenType.RPAREN:
            actual_params.append(self.expr())

        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            actual_params.append(self.expr())

        self.eat(TokenType.RPAREN)

        return ProcedureCall(proc_name, actual_params, token)

    def statement(self) -> Union[NoOp, Compound, ProcedureCall, Assign]:
        """
        statement : compound_statement
                  | proccall_statement
                  | assignment_statement
                  | empty
        """
        if self.current_token.type == TokenType.BEGIN:
            return self.compound_statement()
        elif (self.current_token.type == TokenType.ID and
            self.lexer.current_char == '('
        ):
            return self.procall_statement()
        elif self.current_token.type == TokenType.ID:
            return self.assignment_statement()
        else:
            return self.empty()

    def statement_list(self) -> List[
            Union[NoOp, Compound, ProcedureCall, Assign]
        ]:
        """statement_list : statement
                          | statement SEMI statement_list"""
        node = self.statement()
        results = [node]

        while self.current_token.type == TokenType.SEMI:
            self.eat(TokenType.SEMI)
            results.append(self.statement())

        if self.current_token.type == TokenType.ID:
            self.error(
                error_code=ErrorCode.UNEXPECTED_TOKEN,
                token=self.current_token
            )

        return results

    def type_spec(self) -> Type:
        """type_spec : INTEGER
                     | REAL
        """
        token = self.current_token
        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
        elif token.type == TokenType.REAL:
            self.eat(TokenType.REAL)

        return Type(token)

    def variable_declaration(self) -> List[VarDecl]:
        """variable_declaration : ID (COMMA ID)* COLON type_spec"""
        var_nodes = [Var(self.current_token)]  # first ID
        self.eat(TokenType.ID)

        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            var_nodes.append(Var(self.current_token))
            self.eat(TokenType.ID)

        self.eat(TokenType.COLON)
        type_node = self.type_spec()
        var_declarations = [
            VarDecl(var_node, type_node)
            for var_node in var_nodes
        ]

        return var_declarations

    def formal_parameters(self) -> List[Param]:
        """ formal_parameters : ID (COMMA ID)* COLON type_spec """
        var_nodes = [Var(self.current_token)]
        self.eat(TokenType.ID)

        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            var_nodes.append(Var(self.current_token))
            self.eat(TokenType.ID)

        self.eat(TokenType.COLON)
        param_type = self.type_spec()
        return [Param(var, param_type) for var in var_nodes]


    def formal_parameter_list(self) -> List[Param]:
        """ formal_parameter_list : formal_parameters
                                  | formal_parameters SEMI formal_parameter_list
        """
        if not self.current_token.type == TokenType.ID:
            return []

        param_nodes = self.formal_parameters()
        while self.current_token.type == TokenType.SEMI:
            self.eat(TokenType.SEMI)
            param_nodes.extend(self.formal_parameters())

        return param_nodes

    def declarations(self) -> List[Union[VarDecl, ProcedureDecl, FunctionDecl]]:
        """declarations : (VAR (variable_declaration SEMI)+)*
                    | (PROCEDURE ID (LPAREN formal_parameter_list RPAREN)? SEMI block SEMI)*
                    | (FUNCTION ID (LPAREN formal_parameter_list RPAREN)? COLON type_spec SEMI block SEMI)*
                    | empty
        """
        declarations: Sequence[Union[VarDecl, ProcedureDecl, FunctionDecl]]
        declarations = []

        # Parse variable declarations
        while self.current_token.type == TokenType.VAR:
            self.eat(TokenType.VAR)
            while self.current_token.type == TokenType.ID:
                var_decl = self.variable_declaration()
                declarations.extend(var_decl)
                self.eat(TokenType.SEMI)

        # Parse procedure/function declarations
        while self.current_token.type in (TokenType.PROCEDURE, TokenType.FUNCTION):
            op = self.current_token.type
            self.eat(self.current_token.type)

            proc_fn_name = f'{self.current_token.value}'
            self.eat(TokenType.ID)

            if self.current_token.type == TokenType.LPAREN:
                self.eat(TokenType.LPAREN)
                params = self.formal_parameter_list()
                self.eat(TokenType.RPAREN)

            if op == TokenType.FUNCTION:
                self.eat(TokenType.COLON)
                return_type = self.type_spec()

            self.eat(TokenType.SEMI)

            block_node = self.block()

            if op == TokenType.PROCEDURE:
                declarations.append(
                    ProcedureDecl(proc_fn_name, params, block_node)
                )
            else:
                declarations.append(
                    FunctionDecl(proc_fn_name, params, block_node, return_type)
                )

            self.eat(TokenType.SEMI)

        return declarations

    def block(self) -> Block:
        """block : declarations compound_statement"""
        declaration_nodes = self.declarations()
        compound_statement_node = self.compound_statement()
        node = Block(declaration_nodes, compound_statement_node)

        return node

    def program(self) -> Program:
        """program : PROGRAM variable SEMI block DOT"""
        self.eat(TokenType.PROGRAM)
        var_node = self.variable()
        prog_name = f'{var_node.value}'
        self.eat(TokenType.SEMI)

        block_node = self.block()
        program_node = Program(prog_name, block_node)

        self.eat(TokenType.DOT)
        return program_node

    def parse(self) -> Program:
        node = self.program()
        if self.current_token.type != TokenType.EOF:
            self.error(
                error_code=ErrorCode.UNEXPECTED_TOKEN,
                token=self.current_token
            )

        return node