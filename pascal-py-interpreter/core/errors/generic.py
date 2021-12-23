from enum import Enum
from typing import Optional
from core.token import Token

class ErrorCode(Enum):
    UNEXPECTED_TOKEN = 'Unexpected token'
    ID_NOT_FOUND     = 'Identifier not found'
    DUPLICATE_ID     = 'Duplicate id found'
    INVALID_NUM_ARGS = (
        'Number of arguments is invalid given the procdure declaration'
    )

class Error(Exception):
    def __init__(
        self,
        error_code: Optional[ErrorCode] = None,
        token: Optional[Token] = None,
        message: Optional[str] = None
    ) -> None:
        self.error_code = error_code
        self.token = token
        # add exception class name before the message
        self.message = f'{self.__class__.__name__}: {message}'
        super().__init__(self.message)

class LexerError(Error):
    pass

class ParserError(Error):
    pass

class SemanticError(Error):
    pass