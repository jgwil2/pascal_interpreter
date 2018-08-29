from .keywords import (INTEGER_CONST, FLOAT_CONST, EOF, ID, ASSIGN, KEYWORDS,
    Token)

class Lexer(object):
    def __init__(self, text):
        self.text = text.upper()
        self.pos = 0
        self.current_char = self.text[self.pos]

    def _pos_exceeds_eof(self, pos):
        return pos > len(self.text) - 1

    def _skip_whitespace(self):
        if self.current_char is not None and self.current_char in ' \r\n':
            self._advance_pos()
            self._skip_whitespace()

    def _skip_comment(self):
        self._advance_pos()
        if self.current_char != '}':
            self._skip_comment()
        else:
            self._advance_pos()

    def _advance_pos(self, number=1):
        try:
            self.pos += number
            self.current_char = self.text[self.pos]
        except IndexError:
            self.current_char = None

    def _peek(self, number=1):
        '''return char x number of positions ahead'''
        peek_pos = self.pos + number
        if self._pos_exceeds_eof(peek_pos):
            return None
        return self.text[peek_pos]

    def _is_digit(_, char):
        return char is not None and char.isdigit()

    def _handle_number(self):
        '''return a multidigit integer or float'''
        token_number = ''
        pos = self.pos

        while self._is_digit(self.current_char):
            token_number += self.current_char
            self._advance_pos()

            if self.current_char == '.':
                token_number += self.current_char
                self._advance_pos()
                while self._is_digit(self.current_char):
                    token_number += self.current_char
                    self._advance_pos()

                return Token(FLOAT_CONST, float(token_number))

        return Token(INTEGER_CONST, int(token_number))

    def _handle_word(self):
        '''return a keyword or identifier'''
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self._advance_pos()

        word = KEYWORDS.get(result, ID)
        return Token(word, result)

    def get_next_token(self):
        '''Lexical analyser'''
        self._skip_whitespace()

        if self.current_char == '{':
            self._skip_comment()
            return self.get_next_token()

        if self.current_char is None:
            return Token(EOF, None)

        if self.current_char.isdigit():
            return self._handle_number()

        if self.current_char == ':' and self._peek() == '=':
            self._advance_pos(2)
            return Token(ASSIGN, ':=')

        if self.current_char in KEYWORDS:
            token = Token(KEYWORDS[self.current_char], self.current_char)
            self._advance_pos()
            return token

        if self.current_char.isalpha():
            return self._handle_word()

        raise Exception('Error tokenizing input: {}'.format(self.current_char))
