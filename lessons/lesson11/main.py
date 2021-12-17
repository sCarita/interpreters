import sys
import os

from core.lexer import Lexer
from core.parser import Parser
from core.visitors.pascal import Interpreter
from core.visitors.symbol_table_builder import SymbolTableBuilder

def main(program):
    if program in os.listdir(f'./programs'):
        with open(f'./programs/{program}', 'r') as f:
            program = ''.join(f.readlines())

        lexer = Lexer(program)
        parser = Parser(lexer)

        tree = parser.parse()
        symtab_builder = SymbolTableBuilder()
        symtab_builder.visit(tree)
        print('')
        print('Symbol Table contents:')
        print(symtab_builder.symtab)

        interpreter = Interpreter(tree)
        interpreter.interpret()

        print('')
        print('Run-time GLOBAL_MEMORY contents:')
        for k, v in sorted(interpreter.GLOBAL_SCOPE.items()):
            print('{} = {}'.format(k, v))
    else:
        raise Exception('No program was found.')


if __name__ == '__main__':
    print(f'interpreting {sys.argv[1]}')
    main(sys.argv[1])