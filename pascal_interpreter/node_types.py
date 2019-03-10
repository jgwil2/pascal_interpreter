class ASTNode(object):
    '''
    Base class for abstract syntax tree nodes. Each instance must
    implement `__str__` and `accept` methods. `accept` method takes a
    `visitor` object and calls the visitor's `visit_{node_name}` method.
    '''
    def accept(self, visitor):
        pass

    def __str__(self):
        pass

    def __repr__(self):
        return self.__str__()

class Program(ASTNode):
    '''
    represents a PROGRAM block
    '''
    def __init__(self, name, block):
        self.name = name
        self.block = block

    def __str__(self):
        return 'PROGRAM: {{\r\nNAME: {},\r\nBLOCK: {{\r\n{}\r\n}}\r\n}}'.format(self.name, self.block)

    def accept(self, visitor):
        return visitor.visit_program(self)

class Block(ASTNode):
    '''
    represents variable declarations and compound statement block
    '''
    def __init__(self, declarations, compound_statement):
        self.declarations = declarations
        self.compound_statement = compound_statement

    def __str__(self):
        return 'VAR: {{\r\n{}\r\n}}\r\n{}'.format(
            ',\r\n'.join(map(str, self.declarations)),
            self.compound_statement
        )

    def accept(self, visitor):
        return visitor.visit_block(self)

class VarDecl(ASTNode):
    '''
    represents a variable declaration
    '''
    def __init__(self, var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node

    def __str__(self):
        return '{}: {}'.format(self.var_node, self.type_node)

    def accept(self, visitor):
        return visitor.visit_var_decl(self)

class ProcedureDecl(ASTNode):
    '''
    represents a procedure declaration
    '''
    def __init__(self, proc_name, block_node):
        self.proc_name = proc_name
        self.block_node = block_node

    def __str__(self):
        return '{}: {}'.format(self.proc_name, self.block_node)

    def accept(self, visitor):
        return visitor.visit_proc_decl(self)

class Type(ASTNode):
    '''
    represents a variable type
    '''
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __str__(self):
        return self.value

class CompoundStatement(ASTNode):
    '''
    represents a BEGIN..END block
    '''
    def __init__(self):
        self.children = []

    def __str__(self):
        return 'BEGIN\r\n' + ',\r\n'.join(map(str, self.children)) + '\r\nEND'

    def accept(self, visitor):
        return visitor.visit_compound_statement(self)

class AssignmentStatement(ASTNode):
    '''
    represents a variable assignment
    '''
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
    '''
    represents a variable
    '''
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
    '''
    represents an empty statement
    '''
    def __str__(self):
        return ''

    def accept(self, visitor):
        return visitor.visit_no_op(self)

class BinOp(ASTNode):
    '''
    represents a binary operation
    '''
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
    '''
    represents a unary operation
    '''
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

    def __str__(self):
        return '{op} {expr}'.format(
            op=self.op.value,
            expr=self.expr
        )

    def accept(self, visitor):
        return visitor.visit_unary_op(self)

class Num(ASTNode):
    '''
    represents a number
    '''
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __str__(self):
        return str(self.value)

    def accept(self, visitor):
        return visitor.visit_num(self)
