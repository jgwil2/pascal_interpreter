# token types
(
    INTEGER_CONST,
    FLOAT_CONST,
    PLUS,
    MINUS,
    MUL,
    FLOAT_DIV,
    INTEGER_DIV,
    LPAREN,
    RPAREN,
    EOF,
    PROGRAM,
    VAR,
    INTEGER,
    REAL,
    BEGIN,
    END,
    ID,
    ASSIGN,
    SEMI,
    DOT,
    COLON,
    COMMA
) = (
    'INTEGER_CONST',
    'FLOAT_CONST',
    'PLUS',
    'MINUS',
    'MUL',
    'FLOAT_DIV',
    'INTEGER_DIV',
    '(',
    ')',
    'EOF',
    'PROGRAM',
    'VAR',
    'INTEGER',
    'REAL',
    'BEGIN',
    'END',
    'ID',
    'ASSIGN',
    'SEMI',
    'DOT',
    'COLON',
    'COMMA'
)

KEYWORDS = {
    '+': PLUS,
    '-': MINUS,
    '*': MUL,
    '/': FLOAT_DIV,
    'DIV': INTEGER_DIV,
    '(': LPAREN,
    ')': RPAREN,
    ';': SEMI,
    '.': DOT,
    ':': COLON,
    ',': COMMA,
    PROGRAM: PROGRAM,
    VAR: VAR,
    INTEGER: INTEGER,
    REAL: REAL,
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
