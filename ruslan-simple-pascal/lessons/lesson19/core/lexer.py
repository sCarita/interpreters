from core.token import TokenType, Token, RESERVED_KEYWORDS
from core.errors.lexer import LexerError

class Lexer(object):

    def __init__(self, text):
        # client string input, e.g. "4 + 2 * 3 - 6 / 2"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]
        # token line number and column number
        self.lineno = 1
        self.column = 1

    def error(self):
        s = "Lexer error on '{lexeme}' line: {lineno} column: {column}".format(
            lexeme=self.current_char,
            lineno=self.lineno,
            column=self.column,
        )
        raise LexerError(message=s)

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        if self.current_char == '\n':
            self.lineno += 1
            self.column = 0

        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]
            self.column += 1

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def skip_comment(self):
        while self.current_char != '}':
            self.advance()
        self.advance()

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        """Return a (multidigit) integer consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char == '.':
            result += self.current_char
            self.advance()

            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()

            token_type = TokenType.REAL_CONST
            token = Token(
                token_type, float(result),
                lineno=self.lineno, column=self.column
            )
        else:
            token_type = TokenType.INTEGER_CONST
            token = Token(
                token_type, int(result),
                lineno=self.lineno, column=self.column
            )

        return token

    def _id(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()

        token_type = RESERVED_KEYWORDS.get(result.upper())
        if token_type:
            return Token(
                token_type, result.upper(),
                lineno=self.lineno, column=self.column
            )
        else:
            return Token(
                TokenType.ID, result.upper(),
                lineno=self.lineno, column=self.column
            )

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '{':
                self.advance()
                self.skip_comment()
                continue

            if self.current_char.isdigit():
                return self.number()

            if self.current_char.isalpha():
                return self._id()

            if self.current_char == ':' and self.peek() == '=':
                self.advance()
                self.advance()
                token_type = TokenType.ASSIGN
                return Token(
                    token_type, ':=',
                    lineno=self.lineno, column=self.column
                )

            # single-character token
            try:
                # get enum member by value, e.g. TokenType(';') --> TokenType.SEMI
                token_type = TokenType(self.current_char)
            except ValueError:
                # no enum member with value equal to self.current_char
                self.error()
            else:
                # create a token with a single-character lexeme as its value
                token = Token(
                    type=token_type,
                    value=self.current_char,  # e.g. ';', '.', etc
                    lineno=self.lineno,
                    column=self.column,
                )
                self.advance()
                return token

        token_type = TokenType.EOF
        return Token(token_type, None)