import sys

from interpreter import Interpreter, Visitor
from lexer import Lexer
from parser import Parser

def interpret(text):
    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()
    interpreter = Interpreter(tree)
    calculator_visitor = Visitor()
    result = interpreter.interpret(calculator_visitor)
    # print(result)
    for k, v in sorted(calculator_visitor.GLOBAL_SCOPE.items()):
        print('%s: %s' % (k, v))

# TODO add debug argument to print full stacktrace
def main():
    if len(sys.argv) > 1:
        text = open(sys.argv[1], 'r').read()
        interpret(text)
    else:
        while True:
            try:
                text = input('calc >')
            except EOFError:
                break

            if not text:
                continue

            try:
                interpret(text)
            except Exception as e:
                print(e)
                continue

if __name__ == '__main__':
    main()
