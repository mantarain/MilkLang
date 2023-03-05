
#| Imports |#

import string

#| Constants |#

LETTERS = string.ascii_letters
DIGITS = "0123456789"

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
Tokens["Tk_"] = ""
Tokens["Tk_"] = ""
Tokens["Tk_"] = ""
Tokens["Tk_"] = ""
Tokens["Tk_"] = ""
Tokens["Tk_"] = ""
