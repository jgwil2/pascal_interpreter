''' SIMPLE PASCAL INTERPRETER - 8/12 '''

######################################################################
#
# LEXER
#
######################################################################

# token types
(INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF, BEGIN,
    END, ID, ASSIGN, SEMI, DOT) = (
        'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', '(', ')', 'EOF', 'BEGIN',
        'END', 'ID', 'ASSIGN', 'SEMI', 'DOT'
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

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.type == other.type
            and self.value == other.value
        )

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=self.value
        )

    def __repr__(self):
        return self.__str__()

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
        if self.current_char in ' \r\n':
            self._advance_pos()
            return self._skip_whitespace()

    def _advance_pos(self, number=1):
        try:
            self.pos += number
            self.current_char = self.text[self.pos]
        except IndexError:
            self.current_char = None

    def _peek(self):
        peek_pos = self.pos + 1
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
        if self.current_char is None:
            return Token(EOF, None)

        self._skip_whitespace()

        if self.current_char.isdigit():
            token_number = ''
            pos = self.pos

            while pos < len(self.text) and self.text[pos].isdigit():
                token_number += self.text[pos]
                pos += 1

            token = Token(INTEGER, int(token_number))
            self._advance_pos(pos - self.pos)
            return token

        if self.current_char in OP_DICT:
            token = Token(OP_DICT[self.current_char], self.current_char)
            self._advance_pos()
            return token

        if self.current_char == ':' and self._peek() == '=':
            self._advance_pos(2)
            return Token(ASSIGN, ':=')

        if self.current_char == ';':
            self._advance_pos()
            return Token(SEMI, ';')

        if self.current_char == '.':
            self._advance_pos()
            return Token(DOT, '.')

        if self.current_char.isalpha():
            return self._handle_identifier()

        self.error()

######################################################################
#
# PARSER
#
######################################################################

class ASTNode(object):
    def isBaseNode(self):
        try:
            return hasattr(self.left, 'value') or hasattr(self.right, 'value')
        except AttributeError:
            return False

    def accept(self, visitor):
        pass

class Compound(ASTNode):
    '''represents a BEGIN..END block'''
    def __init__(self):
        self.children = []

    def __str__(self):
        return 'BEGIN ' + ' '.join(map(str, self.children)) + ' END'

    def accept(self, visitor):
        return visitor.visit_compound(self)

class Assignment(ASTNode):
    '''represents a variable assignment'''
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

    def accept(self, visitor):
        return visitor.visit_assignment(self)

class Var(ASTNode):
    '''represents a variable'''
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __str__(self):
        return '{value}'.format(
            value=self.value
        )

    def accept(self, visitor):
        return visitor.visit_var(self)

class NoOp(ASTNode):
    '''represents an empty statement'''
    def __str__(self):
        return ''

    def accept(self, visitor):
        return visitor.visit_no_op(self)

class BinOp(ASTNode):
    '''represents a binary operation'''
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

    def accept(self, visitor):
        return visitor.visit_bin_op(self)

class UnaryOp(ASTNode):
    '''represents a unary operation'''
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

    def __str__(self):
        return '{op} {expr}'.format(
            op=self.op,
            expr=self.expr
        )

    def accept(self, visitor):
        return visitor.visit_unary_op(self)

class Num(ASTNode):
    '''represents a number'''
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __str__(self):
        return str(self.value)

    def accept(self, visitor):
        return visitor.visit_num(self)

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, error_message='Invalid syntax'):
        raise Exception(error_message)

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error('Expected {}, got {}'.format(token_type, self.current_token.type))

    def factor(self):
        '''
        factor: PLUS factor
              | MINUS factor
              | INTEGER
              | LPAREN expr RPAREN
              | variable
        '''
        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            node = UnaryOp(token, self.factor())
        elif token.type == MINUS:
            self.eat(MINUS)
            node = UnaryOp(token, self.factor())
        elif token.type == INTEGER:
            self.eat(INTEGER)
            node = Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
        else:
            node = self.variable()
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

    def variable(self):
        '''
        variable: ID
        '''
        node = Var(self.current_token)
        self.eat(ID)
        return node

    def empty(self):
        '''an empty production'''
        return NoOp()

    def assignment_statement(self):
        '''
        assignment_statement: variable ASSIGN expr
        '''
        left = self.variable()
        token = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        node = Assignment(left, token, right)
        return node

    def statement(self):
        '''
        statement: compound_statement
                 | assignment_statement
                 | empty
        '''
        if self.current_token.type == BEGIN:
            node = self.compound_statement()
        elif self.current_token.type == ID:
            node = self.assignment_statement()
        else:
            node = self.empty()
        return node

    def statement_list(self):
        '''
        statement_list: statement
                      | statement SEMI statement_list
        '''
        node = self.statement()
        results = [node]

        while self.current_token.type == SEMI:
            self.eat(SEMI)
            results.append(self.statement())

        if self.current_token.type == ID:
            self.error()

        return results

    def compound_statement(self):
        '''
        compound_statement: BEGIN statement_list END
        '''
        self.eat(BEGIN)
        nodes = self.statement_list()
        self.eat(END)

        root = Compound()
        for node in nodes:
            root.children.append(node)

        return root

    def program(self):
        '''
        program: compound_statement DOT
        '''
        node = self.compound_statement()
        self.eat(DOT)
        return node

    def parse(self):
        node = self.program()
        if self.current_token.type != EOF:
            self.error()
        return node

######################################################################
#
# INTERPRETER
#
######################################################################

class Visitor(object):
    '''
    base class for Visitors - Visitors must define their own
    calculate method which is used to perform binary ops
    Interpreter is configured with one Visitor
    '''
    GLOBAL_SCOPE = {}

    def visit_compound(self, node):
        for child in node.children:
            child.accept(self)

    def visit_assignment(self, node):
        var_name = node.left.value
        self.GLOBAL_SCOPE[var_name] = node.right.accept(self)
        return self.GLOBAL_SCOPE[var_name]

    def visit_var(self, node):
        var_name = node.value
        val = self.GLOBAL_SCOPE.get(var_name)
        if val is None:
            raise NameError(repr(var_name))
        return val

    def visit_no_op(self, node):
        pass

    def visit_bin_op(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)
        return self.calculate(node, left, right)

    def visit_unary_op(self, node):
        op = node.op.type
        if op == PLUS:
            return +node.expr.accept(self)
        elif op == MINUS:
            return -node.expr.accept(self)
        else:
            raise Exception('Invalid op type')

    def visit_num(self, node):
        return node.value

class CalculatorVisitor(Visitor):
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
        # print(tree)
        return tree.accept(self.visitor)

# TODO add debug argument to print full stacktrace
def main():
    import sys
    if len(sys.argv) > 1:
        text = open(sys.argv[1], 'r').read()
        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser, CalculatorVisitor())
        result = interpreter.interpret()
        print(result)
        print(interpreter.visitor.GLOBAL_SCOPE)
    else:
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
                print(interpreter.visitor.GLOBAL_SCOPE)
            except Exception as e:
                print(e)
                continue

if __name__ == '__main__':
    main()
