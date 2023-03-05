#######################################
# IMPORTS
#######################################

import src.main.position
import string

#######################################
# CONSTANTS
#######################################

DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS

#######################################
# TOKENS
#######################################

Tk_INT   			= 'INT'
Tk_FLOAT    	= 'FLOAT'
Tk_STRING			= 'STRING'
Tk_IDENTIFIER	= 'IDENTIFIER'
Tk_KEYWORD		= 'KEYWORD'
Tk_PLUS     	= 'PLUS'
Tk_MINUS    	= 'MINUS'
Tk_MUL      	= 'MUL'
Tk_DIV      	= 'DIV'
Tk_POW				= 'POW'
Tk_EQ					= 'EQ'
Tk_LPAREN   	= 'LPAREN'
Tk_RPAREN   	= 'RPAREN'
Tk_LSQUARE    = 'LSQUARE'
Tk_RSQUARE    = 'RSQUARE'
Tk_LBrace     = 'LBrace'
Tk_RBrace     = 'Rbrace'
Tk_EE					= 'EE'
Tk_NE					= 'NE'
Tk_LT					= 'LT'
Tk_GT					= 'GT'
Tk_LTE				= 'LTE'
Tk_GTE				= 'GTE'
Tk_COMMA			= 'COMMA'
Tk_ARROW			= 'ARROW'
Tk_NEWLINE		= 'NEWLINE'
Tk_EOF				= 'EOF'

KEYWORDS = [
  'var',
  'and',
  'or',
  'not',
  'if',
  'elif',
  'else',
  'for',
  'to',
  'step',
  'while',
  'def',
  'then',
  'end',
  'return',
  'continue',
  'break',
]

#######################################
# TOKEN CLASS
#######################################

class Token:
  def __init__(self, type_, value=None, pos_start=None, pos_end=None):
    self.type = type_
    self.value = value

    if pos_start:
      self.pos_start = pos_start.copy()
      self.pos_end = pos_start.copy()
      self.pos_end.advance()

    if pos_end:
      self.pos_end = pos_end.copy()

  def matches(self, type_, value):
    return self.type == type_ and self.value == value
  
  def __repr__(self):
    if self.value: return f'{self.type}:{self.value}'
    return f'{self.type}'