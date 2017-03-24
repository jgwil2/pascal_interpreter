''' SIMPLE PASCAL INTERPRETER - 8/12 '''

######################################################################
#
# LEXER
#
######################################################################

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

######################################################################
#
# PARSER
#
######################################################################

class AST(object):
    def isBaseNode(self):
        try:
            return hasattr(self.left, 'value') or hasattr(self.right, 'value')
        except AttributeError:
            return False

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

    def __str__(self):
        return '({left} {op} {right})'.format(
            left=str(self.left),
            op=self.op.value,
            right=str(self.right)
        )

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __str__(self):
        return str(self.value)

class Parser(object):
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
            node = Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
        return node

    def term(self):
        '''
        term: factor((MUL|DIV)factor)*
        '''
        node = self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)
            node = BinOp(node, token, self.factor())

        return node

    def expr(self):
        '''
        expr: term((PLUS|MINUS)term)*
        '''
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)
            node = BinOp(node, token, self.term())

        return node

    def parse(self):
        return self.expr()

######################################################################
#
# INTERPRETER
#
######################################################################

class Visitor(object):
    def visit(self, node):
        # node is operator (recursive case)
        try:
            left = self.visit(node.left)
            right = self.visit(node.right)
            return self.calculate(node, left, right)
        # node is operand (base case)
        except AttributeError:
            return node.value

    def calculate(self, node, left, right):
        pass

class CalculatorVisitor(Visitor):
    # FIXME calculate signature may be too long... named params?
    def calculate(self, node, left, right):
        if node.op.type == PLUS:
            return left + right
        elif node.op.type == MINUS:
            return left - right
        elif node.op.type == MUL:
            return left * right
        elif node.op.type == DIV:
            return left // right
        else:
            raise Exception('Invalid op type')


class PostfixNotationVisitor(Visitor):
    def calculate(self, node, left, right):
        return '{left} {right} {op}'.format(
            left=str(left),
            right=str(right),
            op=node.op.value
        )

class LispStyleNotationVisitor(Visitor):
    def calculate(self, node, left, right):
        return '({op} {left} {right})'.format(
            left=str(left),
            right=str(right),
            op=node.op.value
        )

class Interpreter(object):
    def __init__(self, parser, visitor):
        self.parser = parser
        self.visitor = visitor

    def interpret(self):
        tree = self.parser.parse()
        #print(tree)
        return self.visitor.visit(tree)

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
            parser = Parser(lexer)
            interpreter = Interpreter(parser, CalculatorVisitor())
            result = interpreter.interpret()
            print(result)
        except Exception as e:
            print(e)
            continue

if __name__ == '__main__':
    main()

