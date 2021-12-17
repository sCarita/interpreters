# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', '(', ')', 'EOF'
)

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

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
            Token(MUL, '*')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

###############################################################################
#                                                                             #
#  LEXER                                                                      #
#                                                                             #
###############################################################################

class Lexer(object):
    def __init__(self, text):
        # client string input, e.g. "4 + 2 * 3 - 6 / 2"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Return a (multidigit) integer consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            self.error()

        return Token(EOF, None)

###############################################################################
#                                                                             #
#  PARSER                                                                     #
#                                                                             #
###############################################################################

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """factor : (PLUS|MINUS)factor | INTEGER | LPAREN expr RPAREN"""
        token = self.current_token
        if token.type in (MINUS, PLUS):
            self.eat(token.type)
            return UnaryOp(token, self.factor())
        elif token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            subtree = self.expr()
            self.eat(RPAREN)
            return subtree

    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        node = self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)

            node = BinOp(left=node, right=self.factor(), op=token)

        return node

    def expr(self):
        """Arithmetic expression parser / interpreter.

        calc> 7 + 3 * (10 / (12 / (3 + 1) - 1))
        22

        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : INTEGER | LPAREN expr RPAREN
        """
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinOp(left=node, right=self.term(), op=token)

        return node

    def parse(self):
        return self.expr()

###############################################################################
#                                                                             #
#  INTERPRETER                                                                #
#                                                                             #
###############################################################################

class NodeVisitor(object):
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.undefined_visit)
        return visitor(node)

    def undefined_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser

    def visit_Num(self, node):
        return node.value

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == DIV:
            return self.visit(node.left) / self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)

    def visit_UnaryOp(self, node):
        if node.op.type == PLUS:
            return +self.visit(node.expr)
        elif node.op.type == MINUS:
            return -self.visit(node.expr)

    def interpret(self):
        ir = self.parser.parse()
        return self.visit(ir)

class ReversePolishNotation(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.path = []

    def visit_Num(self, node):
        self.path.append(str(node.value))

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)
        self.path.append(str(node.op.value))

    def translate(self):
        ir = self.parser.parse()
        self.visit(ir)
        return ' '.join(self.path)

class ReversePolishNotation2(NodeVisitor):
    def __init__(self, tree):
        self.tree = tree

    def visit_BinOp(self, node):
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)
        return '{left} {right} {op}'.format(
            left=left_val,
            right=right_val,
            op=node.op.value,
        )

    def visit_Num(self, node):
        return node.value

    def translate(self):
        return self.visit(self.tree)

class LispNotation(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.path = []

    def visit_Num(self, node):
        return str(node.value)

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return f'({node.op.value} {left} {right})'

    def translate(self):
        ir = self.parser.parse()
        return self.visit(ir)


def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue

        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        print(result)


if __name__ == '__main__':
    main()