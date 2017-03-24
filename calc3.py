# token types
INTEGER, OPERATION, EOF = 'INTEGER', 'OPERATION', 'EOF' 

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

class Interpreter(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None

    def error(self):
        raise Exception('error parsing input')

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

        if current_char in '+-*/': 
            token = Token(OPERATION, current_char)
            return self._advance_pos(token, 1)

        self.error()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self, next_token=None):
        if next_token is None:
            self.current_token = self.get_next_token()
            left = self.current_token
            self.eat(INTEGER)
        else:
            left = next_token

        op = self.current_token
        self.eat(OPERATION)

        right = self.current_token
        self.eat(INTEGER)

        if op.value == '+':
            result = left.value + right.value

        if op.value == '-':
            result = left.value - right.value

        if op.value == '*':
            result = left.value * right.value

        if op.value == '/':
            result = left.value / right.value

        if self.current_token.type == 'EOF':
            return result

        # should recursive impl be replaced w/ iterative for perf?
        return self.expr(Token(INTEGER, result))

def main():
    while True:
        try:
            text = input('calc >')
        except EOFError:
            break

        if not text:
            continue

        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()

