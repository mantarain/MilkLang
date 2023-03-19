
#| imports |#

from libs.strwtars import string_with_arrows

#| Base Error Class |#

class Error:
    def __init__(self, pStart, pEnd, error_name, details):
        self.pStart = pStart
        self.pEnd = pEnd
        self.error_name = error_name
        self.details = details

    def as_string(self):
        error  = f'{self.error_name}: {self.details}\n'
        error += f'File {self.pStart.fn}, line {self.pStart.ln + 1}'
        error += '\n\n' + string_with_arrows(self.pStart.ftxt, self.pStart, self.pEnd)
        return error

#| Error classes |#

class IllegalCharError(Error):
    def __init__(self, pStart, pEnd, details):
        super().__init__(pStart, pEnd, 'Illegal Character', details)

class ExpectedCharError(Error):
    def __init__(self, pStart, pEnd, details):
        super().__init__(pStart, pEnd, 'Expected Character', details)

class InvalidSyntaxError(Error):
    def __init__(self, pStart, pEnd, details=''):
        super().__init__(pStart, pEnd, 'Invalid Syntax', details)

#< Runtime Error Class >#

class RTError(Error):
    def __init__(self, pStart, pEnd, details, context):
        super().__init__(pStart, pEnd, 'Runtime Error', details)
        self.context = context
    
    def as_string(self):
        result  = self.generate_traceback()
        result += f'{self.error_name}: {self.details}'
        result += '\n\n' + string_with_arrows(self.pStart.ftxt, self.pStart, self.pEnd)
        return result

    def generate_traceback(self):
        result = ''
        pos = self.pStart
        ctx = self.context
    
        while ctx:
            result = f'  File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.displayName}\n' + result
            pos = ctx.parentEntryPos
            ctx = ctx.parent
        
        return 'Traceback (most recent call last):\n' + result