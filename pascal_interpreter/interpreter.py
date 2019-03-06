class Interpreter(object):
    '''
    Interpreter is configured with one parse tree (output of parser)
    `interpret` method may be called several times with different
    visitors in order to allow multiple passes through the parse tree
    '''
    def __init__(self, tree):
        self.tree = tree

    def interpret(self, visitor):
        # print(self.tree)
        return self.tree.accept(visitor)
