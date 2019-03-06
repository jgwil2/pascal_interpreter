from .visitor import Visitor

class Symbol(object):
    def __init__(self, name, type=None):
        self.name = name
        self.type = type

class BuiltinTypeSymbol(Symbol):
    def __init__(self, name):
        super(BuiltinTypeSymbol, self).__init__(name)

    def __str__(self):
        return self.name

    __repr__ = __str__

class VarSymbol(Symbol):
    def __init__(self, name, type):
        super(VarSymbol, self).__init__(name, type)

    def __str__(self):
        return '<{name}:{type}>'.format(name=self.name, type=self.type)

    __repr__ = __str__

class SymbolTable(object):
    def __init__(self):
        self._symbols = {}
        self._init_builtins()

    def _init_builtins(self):
        self.define(BuiltinTypeSymbol('INTEGER'))
        self.define(BuiltinTypeSymbol('REAL'))

    def __str__(self):
        s = 'Symbols: {symbols}'.format(
            symbols=[value for value in self._symbols.values()]
        )
        return s

    def define(self, symbol):
        # print('Define: %s' % symbol)
        self._symbols[symbol.name] = symbol

    def lookup(self, name):
        # print('Lookup: %s' % name)
        symbol = self._symbols.get(name)
        return symbol

class SymbolTableBuilderVisitor(Visitor):
    def __init__(self):
        self.symtable = SymbolTable()

    def visit_var_decl(self, node):
        type_name = node.type_node.value
        type_symbol = self.symtable.lookup(type_name)
        var_name = node.var_node.value
        var_symbol = VarSymbol(var_name, type_symbol)
        self.symtable.define(var_symbol)

    def visit_assignment(self, node):
        var_name = node.left.value
        var_symbol = self.symtable.lookup(var_name)
        if var_symbol is None:
            raise NameError(str(var_name))
        return node.right.accept(self)

    def visit_var(self, node):
        var_name = node.value
        var_symbol = self.symtable.lookup(var_name)
        if var_symbol is None:
            raise NameError(str(var_name))

    # TODO these methods should be implemented by the parent class
    def visit_bin_op(self, node):
        # no arithmetic
        node.left.accept(self)
        node.right.accept(self)

    def visit_unary_op(self, node):
        # no arithmetic
        node.expr.accept(self)

