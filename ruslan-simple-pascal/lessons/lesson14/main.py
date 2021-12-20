import subprocess
import sys
import os

from core.lexer import Lexer
from core.parser import Parser
from core.visitors.pascal import Interpreter
from core.visitors.semantic_analyzer import SemanticAnalyzer
from core.visitors.ast_visualizer import ASTVisualizer

def main(program):
    if program in os.listdir(f'./programs'):
        with open(f'./programs/{program}', 'r') as f:
            code = ''.join(f.readlines())

        lexer = Lexer(code)
        parser = Parser(lexer)

        tree = parser.parse()
        semantic_analyzer = SemanticAnalyzer()
        try:
            semantic_analyzer.visit(tree)
        except Exception as e:
            print(e)

        # print(semantic_analyzer.scope)

        viz = ASTVisualizer(tree)
        content = viz.gendot()

        with open(f'./ast_tree/dot/{program.split(".")[0]}_ast.dot', 'w') as f:
            f.write(content)

        subprocess.run([
            'dot', '-Tpng', '-o', f'./ast_tree/png/{program.split(".")[0]}_ast.png',
            f'./ast_tree/dot/{program.split(".")[0]}_ast.dot'
        ])

        # interpreter = Interpreter(tree)
        # interpreter.interpret()

        # print('')
        # print('Run-time GLOBAL_MEMORY contents:')
        # for k, v in sorted(interpreter.GLOBAL_SCOPE.items()):
        #     print('{} = {}'.format(k, v))
    else:
        raise Exception('No program was found.')


if __name__ == '__main__':
    print(f'interpreting {sys.argv[1]}')
    main(sys.argv[1])