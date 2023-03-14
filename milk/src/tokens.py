
#| Imports |#

import string

#| Constants |#

LETTERS = string.ascii_letters
DIGITS = "0123456789"
LETTERS_DIGITS = LETTERS + DIGITS
KEYWORDS = [
    "let",
    "and",
    "or",
    "not",
    "if",
    "elif",
    "else",
    "for",
    "while",
    "func",
    "then",
    "return",
    "continue",
    "break"

]

#| Tokens and Keywords |#

#< Type tokens >#
Tk_int = "Int"
Tk_float = "Float"
Tk_string = "String"
Tk_identifier = "Ident"
Tk_keyword = "KeyW"

#< Operation tokens >#
Tk_plus = "Plus"
Tk_minus = "Minus"
Tk_div = "Div"
Tk_mul = "Mul"
Tk_pow = "Pow"

#< Container tokens >#
Tk_Lparen = "Lparen"
Tk_Rparen = "Rparen"
Tk_Lbracket = "LBracket"
Tk_RBracket = "RBracket"
Tk_LBrace = "LBrace"
Tk_RBrace = "RBrace"

#< Comparison tokens >#
Tk_DoubleEquals = "DoubleEquals"
Tk_NotEquals = "NotEquals"
Tk_LessThan = "LessThan"
Tk_MoreThan = "MoreThan"
Tk_LessThanEquals = "LessThanEquals"
Tk_MoreThanEquals = "MoreThanEquals"

#< Other tokens >#
Tk_Newline = "Newline"
Tk_Equals = "Equals"
Tk_Comma = "Comma"
Tk_Arrow = "Arrow"
Tk_EOF = "EOF"


#| Token Class |#
# Stores token data in a class for use in parser

class Token:
    def __init__(self, type_, value=None, pStart=None, pEnd=None):
        self.type = type_
        self.value = value

        if pStart:
            self.pStart = pStart.copy()
            self.pEnd = pStart.copy()
            self.pEnd.advance()
        
        if pEnd:
            self.pEnd = pEnd.copy()
    
    def matches(self, type_, value):
        return self.type == type_ and self.value == value
  
    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'