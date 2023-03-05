
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

Tokens = {}

#< Type tokens >#
Tokens["Tk_int"] = "Int"
Tokens["Tk_float"] = "Float"
Tokens["Tk_identifier"] = "Ident"
Tokens["Tk_keyword"] = "KeyW"

#< Operation tokens >#
Tokens["Tk_plus"] = "Plus"
Tokens["Tk_minus"] = "Minus"
Tokens["Tk_div"] = "Div"
Tokens["Tk_mul"] = "Mul"
Tokens["Tk_pow"] = "Pow"

#< Separator tokens >#
Tokens["Tk_Lparen"] = "Lparen"
Tokens["Tk_Rparen"] = "Rparen"
Tokens["Tk_Lbracket"] = "LBracket"
Tokens["Tk_RBracket"] = "RBracket"
Tokens["Tk_LBrace"] = "LBrace"
Tokens["Tk_RBrace"] = "RBrace"

#< Comparison tokens >#
Tokens["Tk_DoubleEquals"] = "DoubleEquals"
Tokens["Tk_NotEquals"] = "NotEquals"
Tokens["Tk_LessThan"] = "LessThan"
Tokens["Tk_MoreThan"] = "MoreThan"
Tokens["Tk_LessThanEquals"] = "LessThanEquals"
Tokens["Tk_MoreThanEquals"] = "MoreThanEquals"

#< Other tokens >#
Tokens["Tk_Newline"] = "Newline"
Tokens["Tk_EOF"] = "EOF"


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