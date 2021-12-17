import sys
import os

from core.lexer import Lexer
from core.parser import Parser
from core.visitors.pascal import Interpreter

def main(program):
    print(os.getcwd())
    if program in os.listdir(f'./programs'):
        with open(f'./programs/{program}', 'r') as f:
            program = ''.join(f.readlines())

        lexer = Lexer(program)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        interpreter.interpret()
        print(interpreter.GLOBAL_SCOPE)
    else:
        raise Exception('No program was found.')


if __name__ == '__main__':
    main('test.pas')