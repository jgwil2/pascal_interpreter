import unittest

from pascal_interpreter.lexer import Lexer
from pascal_interpreter.parser import Parser
from pascal_interpreter.keywords import Token

class TestLexer(unittest.TestCase):

    def setUp(self):
        self.lexer = Lexer('BEGIN a := 2; END.')

    def test_lexer_length(self):
        self.assertEqual(len(self.lexer.text), 18)

    def test_skip_whitespace(self):
        self.lexer = Lexer('          BEGIN a := 2; END.')
        self.assertEqual(self.lexer.current_char, ' ')

        self.lexer._skip_whitespace()
        self.assertEqual(self.lexer.current_char, 'B')

        self.lexer = Lexer('BEGIN\r\n  a := 2;\r\nEND.')
        self.lexer._advance_pos(5)
        self.lexer._skip_whitespace()
        self.assertEqual(self.lexer.current_char, 'A')

    def test_skip_comment(self):
        self.lexer = Lexer('{ test comment } begin a := 2; end.')
        token = self.lexer.get_next_token()
        self.assertEqual(token, Token('BEGIN', 'BEGIN'))

    def test_advance_pos(self):
        self.lexer._advance_pos()
        self.assertEqual(self.lexer.current_char, 'E')

        self.lexer._advance_pos(2)
        self.assertEqual(self.lexer.current_char, 'I')

        self.lexer._advance_pos(20)
        self.assertIsNone(self.lexer.current_char)

    def test_peek(self):
        char = self.lexer._peek()
        self.assertEqual(char, 'E')

        self.lexer.pos = len(self.lexer.text) - 1
        char = self.lexer._peek()
        self.assertIsNone(char)

    def test_handle_number(self):
        self.lexer = Lexer('42')
        token = self.lexer._handle_number()
        self.assertEqual(token, Token('INTEGER_CONST', 42))

        self.lexer = Lexer('1.24')
        token = self.lexer._handle_number()
        self.assertEqual(token, Token('FLOAT_CONST', 1.24))

    def test_handle_word(self):
        token = self.lexer._handle_word()
        self.assertEqual(token, Token('BEGIN', 'BEGIN'))

        self.lexer._skip_whitespace()
        token = self.lexer._handle_word()
        self.assertEqual(token, Token('ID', 'A'))

    def test_get_next_token(self):
        token = self.lexer.get_next_token()
        self.assertEqual(token, Token('BEGIN', 'BEGIN'))
        token = self.lexer.get_next_token()
        self.assertEqual(token, Token('ID', 'A'))
        token = self.lexer.get_next_token()
        self.assertEqual(token, Token('ASSIGN', ':='))
        token = self.lexer.get_next_token()
        self.assertEqual(token, Token('INTEGER_CONST', 2))
        token = self.lexer.get_next_token()
        self.assertEqual(token, Token('SEMI', ';'))
        token = self.lexer.get_next_token()
        self.assertEqual(token, Token('END', 'END'))
        token = self.lexer.get_next_token()
        self.assertEqual(token, Token('DOT', '.'))
        token = self.lexer.get_next_token()
        self.assertEqual(token, Token('EOF', None))

class TestParser(unittest.TestCase):

    def setUp(self):
        with open('test_vars.pas', 'r') as f:
            test_script = f.read()
        lexer = Lexer(test_script)
        self.parser = Parser(lexer)

    def test_init(self):
        lexer = Lexer('-4 + (3 * 3)')
        self.parser = Parser(lexer)
        self.assertEqual(self.parser.current_token, Token('MINUS', '-'))

    def test_eat(self):
        lexer = Lexer('-4 + (3 * 3)')
        self.parser = Parser(lexer)
        self.parser.eat('MINUS')
        self.assertEqual(self.parser.current_token, Token('INTEGER_CONST', 4))

        with self.assertRaises(Exception):
            self.eat('BEGIN')

    def test_tree_name(self):
        tree = self.parser.parse()
        self.assertEqual(tree.name, 'TESTVARS')


if __name__ == '__main__':
    unittest.main()
