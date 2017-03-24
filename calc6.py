# token types
INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', '(', ')', 'EOF'
)

OP_DICT = {
    '+': PLUS,
    '-': MINUS,
    '*': MUL,
    '/': DIV,
    '(': LPAREN,
    ')': RPAREN
}

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=self.value
        )

    def __repr__(self):
        return self.__str__()

class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Error parsing input')

    # FIXME side effect
    def _advance_pos(self, token, number):
        self.pos += number
        return token

    def _skip_whitespace(self):
        current_char = self.text[self.pos]
        if (current_char == ' '):
            self.pos += 1
            return self._skip_whitespace()

        return current_char

    def get_next_token(self): 

        if self.pos > len(self.text) - 1:
            return Token(EOF, None)

        current_char = self._skip_whitespace()

        if current_char.isdigit():

            token_number = ''
            pos = self.pos

            while pos < len(self.text) and self.text[pos].isdigit():
                token_number += self.text[pos]
                pos += 1

            token = Token(INTEGER, int(token_number))
            return self._advance_pos(token, pos - self.pos)

        if current_char in OP_DICT: 
            token = Token(OP_DICT[current_char], current_char)
            return self._advance_pos(token, 1)

        self.error()

class Interpreter(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        '''
        factor: INTEGER | LPAREN expr RPAREN
        '''
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            result = token.value
        elif token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
        return result

    def term(self):
        '''
        term: factor((MUL|DIV)factor)*
        '''
        result = self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
                result = result * self.factor()
            elif token.type == DIV:
                self.eat(DIV)
                result = result / self.factor()

        return result

    def expr(self):
        '''
        expr: term((PLUS|MINUS)term)*
        '''
        result = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result = result + self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result = result - self.term()

        return result

def main():
    while True:
        try:
            text = input('calc >')
        except EOFError:
            break

        if not text:
            continue

        try:
            lexer = Lexer(text)
            interpreter = Interpreter(lexer)
            result = interpreter.expr()
            print(result)
        except Exception as e:
            print(e)
            continue

if __name__ == '__main__':
    main()

