
#| Imports |#

from src.tokens import *
from src.error import *
from src.position import *

#| Lexer Class |#

class Lexer:
    def __init__(self, fn, text) -> None:
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.currentChar = None
        self.advance()
    
    def advance(self):
        self.pos.advance(self.currentChar)
        self.currentChar = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
    
    def tokenise(self):
        tokens = []

        while self.currentChar != None:
            #< Multii-Character Tokens >#

            if self.currentChar in " \t":
                self.advance()
            
            elif self.currentChar == "#":
                self.skipComment()
            
            elif self.currentChar in ";\n":
                tokens.append(Token(Tk_Newline,pStart=self.pos))
                self.advance()
            
            elif self.currentChar in DIGITS:
                tokens.append(self.mkNumber())
            
            elif self.currentChar in LETTERS:
                tokens.append(self.mkIdent())
            
            elif self.currentChar == '"':
                tokens.append(self.mkString()) # TODO: make string with single quotes as well
            
            elif self.currentChar == "!":
                token, error = self.mkNotEquals()
                if error: return [], error
                tokens.append(token)
            
            elif self.currentChar == "=":
                tokens.append(self.mkEquals())
            
            elif self.currentChar == "<":
                tokens.append(self.mkLessThan())
            
            elif self.currentChar == ">":
                tokens.append(self.mkMoreThan())
            
            elif self.currentChar == "-":
                tokens.append(self.mkMinorArrow())
            
            #| Single Character Tokens |#

            #< Math Op Tokens >#
            elif self.currentChar == "+":
                tokens.append(Token(Tk_plus, pStart=self.pos))
                self.advance()
            
            elif self.currentChar == "*":
                tokens.append(Token(Tk_mul, pStart=self.pos))
                self.advance()
            
            elif self.currentChar == "/":
                tokens.append(Token(Tk_div, pStart=self.pos))
                self.advance()
            
            elif self.currentChar == "^":
                tokens.append(Token(Tk_pow, pStart=self.pos))
                self.advance()
            
            #< Container Tokens >#

            elif self.currentChar == "(":
                tokens.append(Token(Tk_Lparen, pStart=self.pos))
                self.advance()
            
            elif self.currentChar == ")":
                tokens.append(Token(Tk_Rparen, pStart=self.pos))
                self.advance()
            
            elif self.currentChar == "[":
                tokens.append(Token(Tk_Lbracket, pStart=self.pos))
                self.advance()
            
            elif self.currentChar == "]":
                tokens.append(Token(Tk_RBracket, pStart=self.pos))
                self.advance()
            
            elif self.currentChar == "{":
                tokens.append(Token(Tk_LBrace, pStart=self.pos))
                self.advance()
            
            elif self.currentChar == "}":
                tokens.append(Token(Tk_RBrace, pStart=self.pos))
                self.advance()
            
            elif self.currentChar == ",":
                tokens.append(Token(Tk_Comma, pStart=self.pos))
                self.advance()
            
            else:
                pStart = self.pos.copy()
                char = self.currentChar
                self.advance()
                return [], IllegalCharError(pStart, self.pos, "'" + char + "'")
        
        tokens.append(Token(Tk_EOF, pStart=self.pos))
        return tokens, None
    
    def mkNumber(self):
        numStr = ''
        dotCount = 0
        pStart = self.pos.copy()

        while self.currentChar != None and self.currentChar in DIGITS + '.':
            if self.currentChar == '.':
                if dotCount == 1: break
                dotCount += 1
            numStr += self.currentChar
            self.advance()
        
        if dotCount == 0:
            return Token(Tk_int, int(numStr), pStart, self.pos)
        else:
            return Token(Tk_float, float(numStr), pStart, self.pos)
    
    def mkString(self):
        string = ""
        pStart = self.pos.copy()
        escChar = False
        self.advance()

        escapeChars = {
            "n": "\n",
            "t": "\t"
        }

        while self.currentChar != None and (self.currentChar != '"' or escChar):
            if escChar:
                string += escapeChars.get(self.currentChar, self.currentChar)
            else:
                if self.currentChar == '\\':
                    escChar = True
                else:
                    string += self.currentChar
            self.advance()
            escChar = False
    
        self.advance()
        return Token(Tk_string, string, pStart, self.pos)
    
    def mkIdent(self):
        idStr = ""
        pStart = self.pos.copy()

        while self.currentChar != None and self.currentChar in LETTERS_DIGITS + "_":
            idStr += self.currentChar
            self.advance()
        
        tkType = Tk_keyword if idStr in KEYWORDS else Tk_identifier
        return Token(tkType, idStr, pStart, self.pos)
    
    def mkMinorArrow(self):
        tkType = Tk_minus
        pStart = self.pos.copy()
        self.advance()

        if self.currentChar == ">":
            self.advance()
            tkType = Tk_Arrow
        
        return Token(tkType, pStart=pStart, pEnd=self.pos)
    
    def mkNotEquals(self):
        pStart = self.pos.copy()
        self.advance()

        if self.currentChar == "=":
            self.advance()
            return Token(Tk_NotEquals, pStart=pStart, pEnd=self.pos), None
        
        self.advance()
        return None, ExpectedCharError(pStart, self.pos, "'=' after '!'")
    
    def mkEquals(self):
        tkType = Tk_Equals
        pStart = self.pos.copy()
        self.advance()

        if self.currentChar == "=":
            self.advance()
            tkType = Tk_DoubleEquals
        
        return Token(tkType, pStart=pStart, pEnd=self.pos)
    
    def mkLessThan(self):
        tkType = Tk_LessThan
        pStart = self.pos.copy()
        self.advance()

        if self.currentChar == "=":
            self.advance()
            tkType = Tk_LessThanEquals
        
        return Token(tkType, pStart=pStart, pEnd=self.pos)
    
    def mkMoreThan(self):
        tkType = Tk_MoreThan
        pStart = self.pos.copy()
        self.advance()

        if self.currentChar == "=":
            self.advance()
            tkType = Tk_MoreThanEquals
        
        return Token(tkType, pStart=pStart, pEnd=self.pos)
    
    def skipComment(self):
        self.advance()

        while self.currentChar != "\n":
            self.advance()
        
        self.advance()
