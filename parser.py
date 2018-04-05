######################################################################
#
# PARSER
#
######################################################################

from keywords import (INTEGER, PLUS, MINUS, MUL, DIV, INTEGER_DIV, LPAREN,
    RPAREN, EOF, BEGIN, END, ID, ASSIGN, SEMI, DOT)

class ASTNode(object):
    def isBaseNode(self):
        try:
            return hasattr(self.left, 'value') or hasattr(self.right, 'value')
        except AttributeError:
            return False

    def accept(self, visitor):
        pass

    def __str__(self):
        pass

    def __repr__(self):
        return self.__str__()

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
            self.error('Expected {}, got {}'.format(token_type,
                self.current_token.type))

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

        while self.current_token.type in (MUL, DIV, INTEGER_DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)
            elif token.type == INTEGER_DIV:
                self.eat(INTEGER_DIV)
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
