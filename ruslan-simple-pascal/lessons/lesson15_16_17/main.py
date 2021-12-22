import argparse
import subprocess
import os


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


def main(program):
    if program in os.listdir(f'./programs'):
        with open(f'./programs/{program}', 'r') as f:
            code = ''.join(f.readlines())

        lexer = Lexer(code)
        parser = Parser(lexer)

        print('⓵ Lexer + ⓶ Parser')
        tree = parser.parse()

        print('⓷ Semantics')
        semantic_analyzer = SemanticAnalyzer()
        semantic_analyzer.visit(tree)

        # print(semantic_analyzer.scope)

        viz = ASTVisualizer(tree)
        content = viz.gendot()

        with open(f'./ast_tree/dot/{program.split(".")[0]}_ast.dot', 'w') as f:
            f.write(content)

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