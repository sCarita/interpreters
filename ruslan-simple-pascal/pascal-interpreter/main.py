import argparse
import subprocess
import os
import sys


# Command line arguments
parser = argparse.ArgumentParser(
    description='SPI - Simple Pascal Interpreter'
)
# >> argument definition
parser.add_argument('inputfile', help='Pascal source file')
parser.add_argument(
    '--scope',
    help='Print scope information',
    action='store_true',
)
parser.add_argument(
    '--stack',
    help='Print stack information',
    action='store_true',
)
parser.add_argument(
    '--viz',
    help='Generate AST visualization for analysis',
    action='store_true',
)
# >> argument parsing
args = parser.parse_args()

# Define environment variable to control logging
os.environ['_SHOULD_LOG_SCOPE'] = f'{args.scope}'
os.environ['_SHOULD_LOG_STACK'] = f'{args.stack}'


from core.lexer import Lexer
from core.parser import Parser
from core.visitors.pascal import Interpreter
from core.visitors.semantic import SemanticAnalyzer
from core.visitors.ast import ASTVisualizer
from core.errors.lexer import LexerError
from core.errors.parser import ParserError
from core.errors.semantic import SemanticError


def main(program):
    if program in os.listdir(f'./programs'):
        with open(f'./programs/{program}', 'r') as f:
            code = ''.join(f.readlines())

        print('⓵ Lexer + ⓶ Parser')
        lexer = Lexer(code)
        try:
            parser = Parser(lexer)
            tree = parser.parse()
        except (LexerError, ParserError) as e:
            print(e.message)
            sys.exit(1)

        if args.viz:
            print('⌀ Abstract Syntax Tree Visualizer')
            viz = ASTVisualizer(tree)
            content = viz.gendot()

            with open(f'./ast_tree/dot/{program.split(".")[0]}_ast.dot', 'w') as f:
                f.write(content)

        print('⓷ Semantics')
        semantic_analyzer = SemanticAnalyzer()
        try:
            semantic_analyzer.visit(tree)
        except SemanticError as e:
            print(e.message)
            sys.exit(1)

        subprocess.run([
            'dot', '-Tpng', '-o', f'./ast_tree/png/{program.split(".")[0]}_ast.png',
            f'./ast_tree/dot/{program.split(".")[0]}_ast.dot'
        ])

        print('⓸ Interpreter')
        interpreter = Interpreter(tree)
        interpreter.interpret()

    else:
        raise Exception('No program was found.')


if __name__ == '__main__':
    print(f'🎛 interpreting {args.inputfile}')
    main(args.inputfile)