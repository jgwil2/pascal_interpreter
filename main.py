from interpreter import Interpreter, CalculatorVisitor
from lexer import Lexer
from parser import Parser

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
