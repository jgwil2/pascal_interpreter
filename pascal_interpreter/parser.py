from .keywords import (INTEGER_CONST, FLOAT_CONST, PLUS, MINUS, MUL, FLOAT_DIV,
    INTEGER_DIV, LPAREN, RPAREN, EOF, PROGRAM, VAR, INTEGER, REAL, BEGIN, END,
    ID, ASSIGN, SEMI, DOT, COLON, COMMA)

from .node_types import (Program, Block, VarDecl, Type, CompoundStatement,
    AssignmentStatement, Var, NoOp, BinOp, UnaryOp, Num)

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise Exception('Expected {}, got {}: {}'.format(token_type,
                self.current_token.type, self.current_token))

    def program(self):
        '''
        program: PROGRAM variable SEMI block DOT
        '''
        self.eat(PROGRAM)
        var_node = self.variable()
        prog_name = var_node.value
        self.eat(SEMI)
        block_node = self.block()
        node = Program(prog_name, block_node)
        self.eat(DOT)
        return node

    def block(self):
        '''
        block: declarations compound_statement
        '''
        declaration_nodes = self.declarations()
        compound_statement_node = self.compound_statement()
        node = Block(declaration_nodes, compound_statement_node)
        return node

    def declarations(self):
        '''
        declarations: VAR (variable_declaration SEMI)+
                    | empty
        '''
        declarations = []
        if self.current_token.type == VAR:
            self.eat(VAR)
            while self.current_token.type == ID:
                var_decl = self.variable_declaration()
                declarations.extend(var_decl)
                self.eat(SEMI)

        return declarations

    def variable_declaration(self):
        '''
        variable_declaration: ID (COMMA ID)* COLON type_spec
        '''
        var_nodes = [Var(self.current_token)]
        self.eat(ID)

        while self.current_token.type == COMMA:
            self.eat(COMMA)
            var_nodes.append(Var(self.current_token))
            self.eat(ID)

        self.eat(COLON)
        var_type = self.type_spec()

        return [VarDecl(var_node, var_type) for var_node in var_nodes]

    def type_spec(self):
        '''
        type_spec: INTEGER
                 | REAL
        '''
        token = self.current_token
        if self.current_token.type == INTEGER:
            self.eat(INTEGER)
        if self.current_token.type == REAL:
            self.eat(REAL)

        return Type(token)

    def compound_statement(self):
        '''
        compound_statement: BEGIN statement_list END
        '''
        self.eat(BEGIN)
        nodes = self.statement_list()
        self.eat(END)

        root = CompoundStatement()
        for node in nodes:
            root.children.append(node)

        return root

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
            raise Exception('Invalid syntax at {}'.format(self.current_token))

        return results

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

    def assignment_statement(self):
        '''
        assignment_statement: variable ASSIGN expr
        '''
        left = self.variable()
        token = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        node = AssignmentStatement(left, token, right)
        return node

    def variable(self):
        '''
        variable: ID
        '''
        node = Var(self.current_token)
        self.eat(ID)
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

    def term(self):
        '''
        term: factor((MUL|FLOAT_DIV|INTEGER_DIV)factor)*
        '''
        node = self.factor()

        while self.current_token.type in (MUL, FLOAT_DIV, INTEGER_DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == FLOAT_DIV:
                self.eat(FLOAT_DIV)
            elif token.type == INTEGER_DIV:
                self.eat(INTEGER_DIV)
            node = BinOp(node, token, self.factor())

        return node

    def factor(self):
        '''
        factor: PLUS factor
              | MINUS factor
              | INTEGER_CONST
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
        elif token.type == INTEGER_CONST:
            self.eat(INTEGER_CONST)
            node = Num(token)
        elif token.type == FLOAT_CONST:
            node = Num(token)
            self.eat(FLOAT_CONST)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
        else:
            node = self.variable()
        return node

    def empty(self):
        '''
        an empty production
        '''
        return NoOp()

    def parse(self):
        node = self.program()
        if self.current_token.type != EOF:
            raise Exception('Parser did not reach end of file')
        return node
