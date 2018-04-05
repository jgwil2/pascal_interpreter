# token types
(INTEGER, PLUS, MINUS, MUL, DIV, INTEGER_DIV, LPAREN, RPAREN, EOF, BEGIN,
    END, ID, ASSIGN, SEMI, DOT) = (
        'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', 'INTEGER_DIV', '(', ')',
        'EOF', 'BEGIN', 'END', 'ID', 'ASSIGN', 'SEMI', 'DOT'
)

KEYWORDS = {
    '+': PLUS,
    '-': MINUS,
    '*': MUL,
    DIV: DIV,
    '(': LPAREN,
    ')': RPAREN,
    ';': SEMI,
    '.': DOT,
    BEGIN: BEGIN,
    END: END
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
