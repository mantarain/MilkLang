
#| Imports |#

from src.lexer import Lexer

"""
from parser import Parser
from interpreter import Interpreter
from values import *
"""

#| Variable Table (Symbol Table) Class |#

class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent
    
    def get(self, name):
        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value
    
    def set(self, name, value):
        self.symbols[name] = value
    
    def remove(self, name):
        del self.symbols[name]

#| Builtin Funcs and Vars |#
"""
global_symbol_table = SymbolTable()
global_symbol_table.set("Null", Number.null) # type: ignore
global_symbol_table.set("False", Number.false) # type: ignore
global_symbol_table.set("True", Number.true) # type: ignore
global_symbol_table.set("Math.Pi", Number.math_PI) # type: ignore
global_symbol_table.set("print", BuiltInFunction.print) # type: ignore
global_symbol_table.set("printRet", BuiltInFunction.print_ret) # type: ignore
global_symbol_table.set("input", BuiltInFunction.input) # type: ignore
global_symbol_table.set("inputInt", BuiltInFunction.input_int) # type: ignore
global_symbol_table.set("clear", BuiltInFunction.clear) # type: ignore
global_symbol_table.set("cls", BuiltInFunction.clear) # type: ignore
global_symbol_table.set("isNum", BuiltInFunction.is_number) # type: ignore
global_symbol_table.set("isStr", BuiltInFunction.is_string) # type: ignore
global_symbol_table.set("isList", BuiltInFunction.is_list) # type: ignore
global_symbol_table.set("isFunc", BuiltInFunction.is_function) # type: ignore
global_symbol_table.set("append", BuiltInFunction.append) # type: ignore
global_symbol_table.set("pop", BuiltInFunction.pop) # type: ignore
global_symbol_table.set("extend", BuiltInFunction.extend) # type: ignore
global_symbol_table.set("len", BuiltInFunction.len) # type: ignore
global_symbol_table.set("run", BuiltInFunction.run) # type: ignore"""

#| Run |#

def run(fn, text):
    # Gen tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.tokenise()
    if error: return None, error

    return tokens, None