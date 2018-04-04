######################################################################
#
# INTERPRETER
#
######################################################################

from keywords import PLUS, MINUS, MUL, DIV, INTEGER_DIV

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
            return left / right
        elif node.op.type == INTEGER_DIV:
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
