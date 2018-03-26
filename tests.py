import unittest

from calc8 import Token, Lexer, Parser

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

    def test_handle_identifier(self):
        token = self.lexer._handle_identifier()
        self.assertEqual(token, Token('BEGIN', 'BEGIN'))

        self.lexer._skip_whitespace()
        token = self.lexer._handle_identifier()
        self.assertEqual(token, Token('ID', 'A'))

    def test_get_next_token(self):
        token = self.lexer.get_next_token()
        self.assertEqual(token, Token('BEGIN', 'BEGIN'))
        token = self.lexer.get_next_token()
        self.assertEqual(token, Token('ID', 'A'))
        token = self.lexer.get_next_token()
        self.assertEqual(token, Token('ASSIGN', ':='))
        token = self.lexer.get_next_token()
        self.assertEqual(token, Token('INTEGER', 2))
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
        lexer = Lexer('-4 + (3 * 3)')
        self.parser = Parser(lexer)

    def test_init(self):
        self.assertEqual(self.parser.current_token, Token('MINUS', '-'))

    def test_eat(self):
        self.parser.eat('MINUS')
        self.assertEqual(self.parser.current_token, Token('INTEGER', 4))

        with self.assertRaises(Exception):
            self.eat('BEGIN')

if __name__ == '__main__':
    unittest.main()
