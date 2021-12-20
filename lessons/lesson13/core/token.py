# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER = 'INTEGER'
PLUS = 'PLUS'
MINUS = 'MINUS'
MUL = 'MUL'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
ID = 'ID'
BEGIN = 'BEGIN'
END = 'END'
EOF = 'EOF'
ASSIGN = 'ASSIGN'
SEMI = 'SEMI'
DOT = 'DOT'
PROGRAM = 'PROGRAM'
VAR = 'VAR'
REAL = 'REAL'
COLON = 'COLON'
COMMA = 'COMMA'
INTEGER_CONST = 'INTEGER_CONST'
REAL_CONST = 'REAL_CONST'
INTEGER_DIV = 'INTEGER_DIV'
FLOAT_DIV = 'FLOAT_DIV'
PROCEDURE = 'PROCEDURE'

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