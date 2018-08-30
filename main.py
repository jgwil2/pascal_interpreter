import sys

from pascal_interpreter.interpreter import Interpreter
from pascal_interpreter.parser import Parser
from pascal_interpreter.lexer import Lexer
from pascal_interpreter.symbol_table import SymbolTableBuilderVisitor
from pascal_interpreter.visitor import Visitor

def interpret(text):
    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()
    interpreter = Interpreter(tree)
    symtable_builder = SymbolTableBuilderVisitor()
    visitor = Visitor()
    interpreter.interpret(symtable_builder)
    result = interpreter.interpret(visitor)
    print(symtable_builder.symtable)
    for k, v in sorted(visitor.GLOBAL_SCOPE.items()):
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
