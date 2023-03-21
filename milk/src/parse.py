
# | Parses code into nodes for interpreting |#

# < Imports >#

from src.nodes import *
from src.error import *
from src.tokens import *
from src.parserResult import *

# < Parser Class >#


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tkIndx = -1
        self.advance()

    def advance(self):
        self.tkIndx += 1
        self.updateCurrentTk()
        return self.currentTk

    def reverse(self, amount=1):
        self.tkIndx -= amount
        self.updateCurrentTk()
        return self.currentTk

    def updateCurrentTk(self):
        if self.tkIndx >= 0 and self.tkIndx < len(self.tokens):
            self.currentTk = self.tokens[self.tkIndx]

    def parse(self):
        res = self.statements()
        if not res.error and self.currentTk.type != Tk_EOF:
            return res.failure(InvalidSyntaxError(
                self.currentTk.pStart, self.currentTk.pEnd,
                "Token cannot appear after previous tokens"
            ))
        return res

    ###################################

    def statements(self):
        res = ParseResult()
        statements = []
        pStart = self.currentTk.pStart.copy()

        while self.currentTk.type == Tk_Newline:
            res.register_advancement()
            self.advance()

        statement = res.register(self.statement())
        if res.error:
            return res
        statements.append(statement)

        more_statements = True

        while True:
            newline_count = 0
            while self.currentTk.type == Tk_Newline:
                res.register_advancement()
                self.advance()
                newline_count += 1
            if newline_count == 0:
                more_statements = False

            if not more_statements:
                break
            statement = res.try_register(self.statement())
            if not statement:
                self.reverse(res.reverseCount)
                more_statements = False
                continue
            statements.append(statement)

        return res.success(ListNode(
            statements,
            pStart,
            self.currentTk.pEnd.copy()
        ))

    def statement(self):
        res = ParseResult()
        pStart = self.currentTk.pStart.copy()

        if self.currentTk.matches(Tk_keyword, 'return'):
            res.register_advancement()
            self.advance()

            expr = res.try_register(self.expr())
            if not expr:
                self.reverse(res.reverseCount)
            return res.success(ReturnNode(expr, pStart, self.currentTk.pStart.copy()))

        if self.currentTk.matches(Tk_keyword, 'continue'):
            res.register_advancement()
            self.advance()
            return res.success(ContinueNode(pStart, self.currentTk.pStart.copy()))

        if self.currentTk.matches(Tk_keyword, 'break'):
            res.register_advancement()
            self.advance()
            return res.success(BreakNode(pStart, self.currentTk.pStart.copy()))

        expr = res.register(self.expr())
        if res.error:
            return res.failure(InvalidSyntaxError(
                self.currentTk.pStart, self.currentTk.pEnd,
                "Expected 'RETURN', 'CONTINUE', 'BREAK', 'var', 'if', 'for', 'while', 'def', int, float, identifier, '+', '-', '(', '[' or 'not'"
            ))
        return res.success(expr)

    def expr(self):
        res = ParseResult()

        if self.currentTk.matches(Tk_keyword, 'var'):
            res.register_advancement()
            self.advance()

            if self.currentTk.type != Tk_identifier:
                return res.failure(InvalidSyntaxError(
                    self.currentTk.pStart, self.currentTk.pEnd,
                    "Expected identifier"
                ))

            var_name = self.currentTk
            res.register_advancement()
            self.advance()

            if self.currentTk.type != Tk_Equals:
                return res.failure(InvalidSyntaxError(
                    self.currentTk.pStart, self.currentTk.pEnd,
                    "Expected '='"
                ))

            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res
            return res.success(VarAssignNode(var_name, expr))

        node = res.register(self.bin_op(
            self.comp_expr, ((Tk_keyword, 'and'), (Tk_keyword, 'or'))))

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.currentTk.pStart, self.currentTk.pEnd,
                "Expected 'var', 'if', 'for', 'while', 'def', int, float, identifier, '+', '-', '(', '[' or 'not'"
            ))

        return res.success(node)

    def comp_expr(self):
        res = ParseResult()

        if self.currentTk.matches(Tk_keyword, 'not'):
            op_tok = self.currentTk
            res.register_advancement()
            self.advance()

            node = res.register(self.comp_expr())
            if res.error:
                return res
            return res.success(UnaryOpNode(op_tok, node))

        node = res.register(self.bin_op(self.arith_expr, (Tk_DoubleEquals, Tk_NotEquals,
                            Tk_LessThan, Tk_MoreThan, Tk_LessThanEquals, Tk_MoreThanEquals)))

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.currentTk.pStart, self.currentTk.pEnd,
                "Expected int, float, identifier, '+', '-', '(', '[', 'if', 'for', 'while', 'def' or 'not'"
            ))

        return res.success(node)

    def arith_expr(self):
        return self.bin_op(self.term, (Tk_plus, Tk_minus))

    def term(self):
        return self.bin_op(self.factor, (Tk_mul, Tk_div))

    def factor(self):
        res = ParseResult()
        tk = self.currentTk

        if tk.type in (Tk_plus, Tk_minus):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(tk, factor))

        return self.power()

    def power(self):
        return self.bin_op(self.call, (Tk_pow, ), self.factor)

    def call(self):
        res = ParseResult()
        atom = res.register(self.atom())
        if res.error:
            return res

        if self.currentTk.type == Tk_Lparen:
            res.register_advancement()
            self.advance()
            arg_nodes = []

            if self.currentTk.type == Tk_Rparen:
                res.register_advancement()
                self.advance()
            else:
                arg_nodes.append(res.register(self.expr()))
                if res.error:
                    return res.failure(InvalidSyntaxError(
                        self.currentTk.pStart, self.currentTk.pEnd,
                        "Expected ')', 'var', 'if', 'for', 'while', 'def', int, float, identifier, '+', '-', '(', '[' or 'not'"
                    ))

                while self.currentTk.type == Tk_Comma:
                    res.register_advancement()
                    self.advance()

                    arg_nodes.append(res.register(self.expr()))
                    if res.error:
                        return res

                if self.currentTk.type != Tk_Rparen:
                    return res.failure(InvalidSyntaxError(
                        self.currentTk.pStart, self.currentTk.pEnd,
                        "Expected ',' or ')'"
                    ))

                res.register_advancement()
                self.advance()
            return res.success(CallNode(atom, arg_nodes))
        return res.success(atom)

    def atom(self):
        res = ParseResult()
        tk = self.currentTk

        if tk.type in (Tk_int, Tk_float):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tk))

        elif tk.type == Tk_string:
            res.register_advancement()
            self.advance()
            return res.success(StringNode(tk))

        elif tk.type == Tk_identifier:
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(tk))

        elif tk.type == Tk_Lparen:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res
            if self.currentTk.type == Tk_Rparen:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.currentTk.pStart, self.currentTk.pEnd,
                    "Expected ')'"
                ))

        elif tk.type == Tk_Lbracket:
            list_expr = res.register(self.list_expr())
            if res.error:
                return res
            return res.success(list_expr)

        elif tk.matches(Tk_keyword, 'if'):
            if_expr = res.register(self.if_expr())
            if res.error:
                return res
            return res.success(if_expr)

        elif tk.matches(Tk_keyword, 'for'):
            for_expr = res.register(self.for_expr())
            if res.error:
                return res
            return res.success(for_expr)

        elif tk.matches(Tk_keyword, 'while'):
            while_expr = res.register(self.while_expr())
            if res.error:
                return res
            return res.success(while_expr)

        elif tk.matches(Tk_keyword, 'def'):
            func_def = res.register(self.func_def())
            if res.error:
                return res
            return res.success(func_def)

        return res.failure(InvalidSyntaxError(
            tk.pStart, tk.pEnd,
            "Expected int, float, identifier, '+', '-', '(', '[', IF', 'for', 'while', 'def'"
        ))

    def list_expr(self):
        res = ParseResult()
        element_nodes = []
        pStart = self.currentTk.pStart.copy()

        if self.currentTk.type != Tk_Lbracket:
            return res.failure(InvalidSyntaxError(
                self.currentTk.pStart, self.currentTk.pEnd,
                f"Expected '['"
            ))

        res.register_advancement()
        self.advance()

        if self.currentTk.type == Tk_RBracket:
            res.register_advancement()
            self.advance()
        else:
            element_nodes.append(res.register(self.expr()))
            if res.error:
                return res.failure(InvalidSyntaxError(
                    self.currentTk.pStart, self.currentTk.pEnd,
                    "Expected ']', 'var', 'if', 'for', 'while', 'def', int, float, identifier, '+', '-', '(', '[' or 'not'"
                ))

            while self.currentTk.type == Tk_Comma:
                res.register_advancement()
                self.advance()

                element_nodes.append(res.register(self.expr()))
                if res.error:
                    return res

            if self.currentTk.type != Tk_RBracket:
                return res.failure(InvalidSyntaxError(
                    self.currentTk.pStart, self.currentTk.pEnd,
                    f"Expected ',' or ']'"
                ))

            res.register_advancement()
            self.advance()

        return res.success(ListNode(
            element_nodes,
            pStart,
            self.currentTk.pEnd.copy()
        ))

    def if_expr(self):
        res = ParseResult()
        all_cases = res.register(self.if_expr_cases('if'))
        if res.error:
            return res
        cases, else_case = all_cases  # type: ignore
        return res.success(IfNode(cases, else_case))

    def if_expr_b(self):
        return self.if_expr_cases('elif')

    def if_expr_c(self):
        res = ParseResult()
        else_case = None

        if self.currentTk.matches(Tk_keyword, 'else'):
            res.register_advancement()
            self.advance()

            if self.currentTk.type == Tk_Newline:
                res.register_advancement()
                self.advance()

                statements = res.register(self.statements())
                if res.error:
                    return res
                else_case = (statements, True)

                if self.currentTk.matches(Tk_keyword, 'end'):
                    res.register_advancement()
                    self.advance()
                else:
                    return res.failure(InvalidSyntaxError(
                        self.currentTk.pStart, self.currentTk.pEnd,
                        "Expected 'END'"
                    ))
            else:
                expr = res.register(self.statement())
                if res.error:
                    return res
                else_case = (expr, False)

        return res.success(else_case)

    def if_expr_b_or_c(self):
        res = ParseResult()
        cases, else_case = [], None

        if self.currentTk.matches(Tk_keyword, 'elif'):
            all_cases = res.register(self.if_expr_b())
            if res.error:
                return res
            cases, else_case = all_cases  # type: ignore
        else:
            else_case = res.register(self.if_expr_c())
            if res.error:
                return res

        return res.success((cases, else_case))

    def if_expr_cases(self, case_keyword):
        res = ParseResult()
        cases = []
        else_case = None

        if not self.currentTk.matches(Tk_keyword, case_keyword):
            return res.failure(InvalidSyntaxError(
                self.currentTk.pStart, self.currentTk.pEnd,
                f"Expected '{case_keyword}'"
            ))

        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error:
            return res

        if not self.currentTk.matches(Tk_keyword, 'then'):
            return res.failure(InvalidSyntaxError(
                self.currentTk.pStart, self.currentTk.pEnd,
                f"Expected 'THEN'"
            ))

        res.register_advancement()
        self.advance()

        if self.currentTk.type == Tk_Newline:
            res.register_advancement()
            self.advance()

            statements = res.register(self.statements())
            if res.error:
                return res
            cases.append((condition, statements, True))

            if self.currentTk.matches(Tk_keyword, 'end'):
                res.register_advancement()
                self.advance()
            else:
                all_cases = res.register(self.if_expr_b_or_c())
                if res.error:
                    return res
                new_cases, else_case = all_cases  # type: ignore
                cases.extend(new_cases)
        else:
            expr = res.register(self.statement())
            if res.error:
                return res
            cases.append((condition, expr, False))

            all_cases = res.register(self.if_expr_b_or_c())
            if res.error:
                return res
            new_cases, else_case = all_cases  # type: ignore
            cases.extend(new_cases)

        return res.success((cases, else_case))

    def for_expr(self):
        res = ParseResult()

        if not self.currentTk.matches(Tk_keyword, 'for'):
            return res.failure(InvalidSyntaxError(
                self.currentTk.pStart, self.currentTk.pEnd,
                f"Expected 'for'"
            ))

        res.register_advancement()
        self.advance()

        if self.currentTk.type != Tk_identifier:
            return res.failure(InvalidSyntaxError(
                self.currentTk.pStart, self.currentTk.pEnd,
                f"Expected identifier"
            ))

        var_name = self.currentTk
        res.register_advancement()
        self.advance()

        if self.currentTk.type != Tk_Equals:
            return res.failure(InvalidSyntaxError(
                self.currentTk.pStart, self.currentTk.pEnd,
                f"Expected '='"
            ))

        res.register_advancement()
        self.advance()

        start_value = res.register(self.expr())
        if res.error:
            return res

        if not self.currentTk.matches(Tk_keyword, 'to'):
            return res.failure(InvalidSyntaxError(
                self.currentTk.pStart, self.currentTk.pEnd,
                f"Expected 'TO'"
            ))

        res.register_advancement()
        self.advance()

        end_value = res.register(self.expr())
        if res.error:
            return res

        if self.currentTk.matches(Tk_keyword, 'step'):
            res.register_advancement()
            self.advance()

            step_value = res.register(self.expr())
            if res.error:
                return res
        else:
            step_value = None

        if not self.currentTk.matches(Tk_keyword, 'then'):
            return res.failure(InvalidSyntaxError(
                self.currentTk.pStart, self.currentTk.pEnd,
                f"Expected 'THEN'"
            ))

        res.register_advancement()
        self.advance()

        if self.currentTk.type == Tk_Newline:
            res.register_advancement()
            self.advance()

            body = res.register(self.statements())
            if res.error:
                return res

            if not self.currentTk.matches(Tk_keyword, 'end'):
                return res.failure(InvalidSyntaxError(
                    self.currentTk.pStart, self.currentTk.pEnd,
                    f"Expected 'END'"
                ))

            res.register_advancement()
            self.advance()

            return res.success(ForNode(var_name, start_value, end_value, step_value, body, True))

        body = res.register(self.statement())
        if res.error:
            return res

        return res.success(ForNode(var_name, start_value, end_value, step_value, body, False))

    def while_expr(self):
        res = ParseResult()

        if not self.currentTk.matches(Tk_keyword, 'while'):
            return res.failure(InvalidSyntaxError(
                self.currentTk.pStart, self.currentTk.pEnd,
                f"Expected 'while'"
            ))

        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error:
            return res

        if not self.currentTk.matches(Tk_keyword, 'then'):
            return res.failure(InvalidSyntaxError(
                self.currentTk.pStart, self.currentTk.pEnd,
                f"Expected 'THEN'"
            ))

        res.register_advancement()
        self.advance()

        if self.currentTk.type == Tk_Newline:
            res.register_advancement()
            self.advance()

            body = res.register(self.statements())
            if res.error:
                return res

            if not self.currentTk.matches(Tk_keyword, 'end'):
                return res.failure(InvalidSyntaxError(
                    self.currentTk.pStart, self.currentTk.pEnd,
                    f"Expected 'END'"
                ))

            res.register_advancement()
            self.advance()

            return res.success(WhileNode(condition, body, True))

        body = res.register(self.statement())
        if res.error:
            return res

        return res.success(WhileNode(condition, body, False))

    def func_def(self):
        res = ParseResult()

        if not self.currentTk.matches(Tk_keyword, 'def'):
            return res.failure(InvalidSyntaxError(
                self.currentTk.pStart, self.currentTk.pEnd,
                f"Expected 'def'"
            ))

        res.register_advancement()
        self.advance()

        if self.currentTk.type == Tk_identifier:
            var_name_tok = self.currentTk
            res.register_advancement()
            self.advance()
            if self.currentTk.type != Tk_Lparen:
                return res.failure(InvalidSyntaxError(
                    self.currentTk.pStart, self.currentTk.pEnd,
                    f"Expected '('"
                ))
        else:
            var_name_tok = None
            if self.currentTk.type != Tk_Lparen:
                return res.failure(InvalidSyntaxError(
                    self.currentTk.pStart, self.currentTk.pEnd,
                    f"Expected identifier or '('"
                ))

        res.register_advancement()
        self.advance()
        arg_name_toks = []

        if self.currentTk.type == Tk_identifier:
            arg_name_toks.append(self.currentTk)
            res.register_advancement()
            self.advance()

            while self.currentTk.type == Tk_Comma:
                res.register_advancement()
                self.advance()

                if self.currentTk.type != Tk_identifier:
                    return res.failure(InvalidSyntaxError(
                        self.currentTk.pStart, self.currentTk.pEnd,
                        f"Expected identifier"
                    ))

                arg_name_toks.append(self.currentTk)
                res.register_advancement()
                self.advance()

            if self.currentTk.type != Tk_Rparen:
                return res.failure(InvalidSyntaxError(
                    self.currentTk.pStart, self.currentTk.pEnd,
                    f"Expected ',' or ')'"
                ))
        else:
            if self.currentTk.type != Tk_Rparen:
                return res.failure(InvalidSyntaxError(
                    self.currentTk.pStart, self.currentTk.pEnd,
                    f"Expected identifier or ')'"
                ))

        res.register_advancement()
        self.advance()

        if self.currentTk.type == Tk_Arrow:
            res.register_advancement()
            self.advance()

            body = res.register(self.expr())
            if res.error:
                return res

            return res.success(FuncDefNode(
                var_name_tok,
                arg_name_toks,
                body,
                True
            ))

        if self.currentTk.type != Tk_Newline:
            return res.failure(InvalidSyntaxError(
                self.currentTk.pStart, self.currentTk.pEnd,
                f"Expected '->' or NEWLINE"
            ))

        res.register_advancement()
        self.advance()

        body = res.register(self.statements())
        if res.error:
            return res

        if not self.currentTk.matches(Tk_keyword, 'end'):
            return res.failure(InvalidSyntaxError(
                self.currentTk.pStart, self.currentTk.pEnd,
                f"Expected 'END'"
            ))

        res.register_advancement()
        self.advance()

        return res.success(FuncDefNode(
            var_name_tok,
            arg_name_toks,
            body,
            False
        ))

    ###################################

    def bin_op(self, func_a, ops, func_b=None):
        if func_b == None:
            func_b = func_a

        res = ParseResult()
        left = res.register(func_a())
        if res.error:
            return res

        while self.currentTk.type in ops or (self.currentTk.type, self.currentTk.value) in ops:
            op_tok = self.currentTk
            res.register_advancement()
            self.advance()
            right = res.register(func_b())
            if res.error:
                return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)
