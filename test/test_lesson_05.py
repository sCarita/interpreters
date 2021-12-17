import unittest
from lessons.lesson05.main import Lexer, Interpreter

class Test(unittest.TestCase):
    def calculate(self, text):
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        return interpreter.expr()

    def test_expressions(self):
        # Tests:
        # >> (1 + (2 + 3)) = 6
        # >> 1 + (2 + 3) = 6
        # >> (2 + 3) + 1 = 6
        # >> (1 + (2 + (2+2+2))) = 9
        # >> ((1*10) + (2 + (2+2+2))) = 18
        # >> ((1*10) * (2 + (2+2+2))) = 80

        self.assertEqual(self.calculate('(1 + (2 + 3))'), 6)
        self.assertEqual(self.calculate('1 + (2 + 3)'), 6)
        self.assertEqual(self.calculate('(2 + 3) + 1'), 6)
        self.assertEqual(self.calculate('(1 + (2 + (2+2+2)))'), 9)
        self.assertEqual(self.calculate('((1*10) + (2 + (2+2+2)))'), 18)
        self.assertEqual(self.calculate('((1*10) * (2 + (2+2+2)))'), 80)
        self.assertEqual(
            self.calculate('7 + 3 * (10 / (12 / (3 + 1) - 1))'), 22
        )

if __name__ == '__main__':
    # begin the unittest.main()
    unittest.main()