from lingoshell.context import Context
from lingoshell.position import Position
from lingoshell.values import *
from lingoshell.tokens import *
from lingoshell.constants import *
from lingoshell.errors import *
from lingoshell.results import *
from lingoshell.nodes import *

from lingoshell.lexer import Lexer
from lingoshell.parser import Parser
from lingoshell.inter import Interpreter

global_symbol_table = SymbolTable()
global_symbol_table.set("LANG", String.EN)

global_symbol_table.set("NULL", Number.null)
global_symbol_table.set("FALSE", Number.false)
global_symbol_table.set("TRUE", Number.true)
global_symbol_table.set("MATH_PI", Number.math_PI)

global_symbol_table.set("PRINT", BuiltInFunction.print)
global_symbol_table.set("PRINT_RET", BuiltInFunction.print_ret)
global_symbol_table.set("INPUT", BuiltInFunction.input)
global_symbol_table.set("INPUT_INT", BuiltInFunction.input_int)
global_symbol_table.set("APPEND", BuiltInFunction.append)
global_symbol_table.set("POP", BuiltInFunction.pop)
global_symbol_table.set("EXTEND", BuiltInFunction.extend)
global_symbol_table.set("LEN", BuiltInFunction.len)
global_symbol_table.set("RUN", BuiltInFunction.run)


def run(fn, text):
    context = Context("<program>")
    context.symbol_table = global_symbol_table

    # Generate tokens
    lexer = Lexer(fn, text, context)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error

    # Run program
    interpreter = Interpreter()
    result = interpreter.visit(ast.node, context)

    return result.value, result.error
