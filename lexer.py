######################################################################
#
# LEXER
#
######################################################################

from keywords import (INTEGER, PLUS, MINUS, MUL, DIV, INTEGER_DIV, LPAREN,
    RPAREN, EOF, BEGIN, END, ID, ASSIGN, SEMI, DOT, KEYWORDS, Token)

class Lexer(object):
    def __init__(self, text):
        self.text = text.upper()
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Error parsing input')

    def _pos_exceeds_eof(self, pos):
        return pos > len(self.text) - 1

    def _skip_whitespace(self):
        if self.current_char is not None and self.current_char in ' \r\n':
            self._advance_pos()
            return self._skip_whitespace()

    def _advance_pos(self, number=1):
        try:
            self.pos += number
            self.current_char = self.text[self.pos]
        except IndexError:
            self.current_char = None

    def _peek(self, number=1):
        peek_pos = self.pos + number
        if self._pos_exceeds_eof(peek_pos):
            return None
        return self.text[peek_pos]

    def _handle_identifier(self):
        RESERVED_KEYWORDS = {
            'BEGIN': Token(BEGIN, BEGIN),
            'END': Token(END, END)
        }

        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self._advance_pos()

        return RESERVED_KEYWORDS.get(result, Token(ID, result))

    def get_next_token(self):
        '''
        Lexical analyser
        '''
        self._skip_whitespace()

        if self.current_char is None:
            return Token(EOF, None)

        if self.current_char.isdigit():
            token_number = ''
            pos = self.pos

            while pos < len(self.text) and self.text[pos].isdigit():
                token_number += self.text[pos]
                pos += 1

            token = Token(INTEGER, int(token_number))
            self._advance_pos(pos - self.pos)
            return token

        if self.current_char in KEYWORDS:
            token = Token(KEYWORDS[self.current_char], self.current_char)
            self._advance_pos()
            return token

        if (self.current_char == 'D'
            and self._peek() == 'I'
            and self._peek(2) == 'V'):
            self._advance_pos(3)
            return Token(INTEGER_DIV, INTEGER_DIV)

        if self.current_char == ':' and self._peek() == '=':
            self._advance_pos(2)
            return Token(ASSIGN, ':=')

        if self.current_char.isalpha():
            return self._handle_identifier()

        self.error()
