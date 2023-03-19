
#| Interpreter |#

#< Imports >#

from src.rtResult import *
from src.values import *
from src.tokens import *
from src.error import RTError

class Interpreter:
  def visit(self, node, context):
    method_name = f'visit_{type(node).__name__}'
    method = getattr(self, method_name, self.no_visit_method)
    return method(node, context)

  def no_visit_method(self, node, context):
    raise Exception(f'No visit_{type(node).__name__} method defined')

  ###################################

  def visit_NumberNode(self, node, context):
    return RTResult().success(
      Number(node.tk.value).set_context(context).set_pos(node.pStart, node.pEnd)
    )

  def visit_StringNode(self, node, context):
    return RTResult().success(
      String(node.tk.value).set_context(context).set_pos(node.pStart, node.pEnd)
    )

  def visit_ListNode(self, node, context):
    res = RTResult()
    elements = []

    for element_node in node.elementNodes:
      elements.append(res.register(self.visit(element_node, context)))
      if res.shouldReturn(): return res

    return res.success(
      List(elements).set_context(context).set_pos(node.pStart, node.pEnd)
    )

  def visit_VarAccessNode(self, node, context):
    res = RTResult()
    var_name = node.varNameTk.value
    value = context.symbolTable.get(var_name)

    if not value:
      return res.failure(RTError(
        node.pStart, node.pEnd,
        f"'{var_name}' is not defined",
        context
      ))

    value = value.copy().set_pos(node.pStart, node.pEnd).set_context(context)
    return res.success(value)

  def visit_VarAssignNode(self, node, context):
    res = RTResult()
    var_name = node.varNameTk.value
    value = res.register(self.visit(node.valueNode, context))
    if res.shouldReturn(): return res

    context.symbolTable.set(var_name, value)
    return res.success(value)

  def visit_BinOpNode(self, node, context):
    res = RTResult()
    left = res.register(self.visit(node.leftNode, context))
    if res.shouldReturn(): return res
    right = res.register(self.visit(node.rightNode, context))
    if res.shouldReturn(): return res

    if node.opTk.type == Tk_plus:
      result, error = left.added_to(right)
    elif node.opTk.type == Tk_minus:
      result, error = left.subbed_by(right)
    elif node.opTk.type == Tk_mul:
      result, error = left.multed_by(right)
    elif node.opTk.type == Tk_div:
      result, error = left.dived_by(right)
    elif node.opTk.type == Tk_pow:
      result, error = left.powed_by(right)
    elif node.opTk.type == Tk_DoubleEquals:
      result, error = left.get_comparison_eq(right)
    elif node.opTk.type == Tk_NotEquals:
      result, error = left.get_comparison_ne(right)
    elif node.opTk.type == Tk_LessThan:
      result, error = left.get_comparison_lt(right)
    elif node.opTk.type == Tk_MoreThan:
      result, error = left.get_comparison_gt(right)
    elif node.opTk.type == Tk_LessThanEquals:
      result, error = left.get_comparison_lte(right)
    elif node.opTk.type == Tk_MoreThanEquals:
      result, error = left.get_comparison_gte(right)
    elif node.opTk.matches(Tk_keyword, 'and'):
      result, error = left.anded_by(right)
    elif node.opTk.matches(Tk_keyword, 'or'):
      result, error = left.ored_by(right)

    if error: # type: ignore
      return res.failure(error)
    else:
      return res.success(result.set_pos(node.pStart, node.pEnd)) # type: ignore

  def visit_UnaryOpNode(self, node, context):
    res = RTResult()
    number = res.register(self.visit(node.node, context))
    if res.shouldReturn(): return res

    error = None

    if node.opTk.type == Tk_minus:
      number, error = number.multed_by(Number(-1))
    elif node.opTk.matches(Tk_keyword, 'not'):
      number, error = number.notted()

    if error:
      return res.failure(error)
    else:
      return res.success(number.set_pos(node.pStart, node.pEnd))

  def visit_IfNode(self, node, context):
    res = RTResult()

    for condition, expr, should_return_null in node.cases:
      condition_value = res.register(self.visit(condition, context))
      if res.shouldReturn(): return res

      if condition_value.is_true():
        expr_value = res.register(self.visit(expr, context))
        if res.shouldReturn(): return res
        return res.success(Number.null if should_return_null else expr_value) # type: ignore

    if node.elseCase:
      expr, should_return_null = node.elseCase
      expr_value = res.register(self.visit(expr, context))
      if res.shouldReturn(): return res
      return res.success(Number.null if should_return_null else expr_value) # type: ignore

    return res.success(Number.null) # type: ignore

  def visit_ForNode(self, node, context):
    res = RTResult()
    elements = []

    start_value = res.register(self.visit(node.start_value_node, context))
    if res.shouldReturn(): return res

    end_value = res.register(self.visit(node.end_value_node, context))
    if res.shouldReturn(): return res

    if node.step_value_node:
      step_value = res.register(self.visit(node.step_value_node, context))
      if res.shouldReturn(): return res
    else:
      step_value = Number(1)

    i = start_value.value

    if step_value.value >= 0:
      condition = lambda: i < end_value.value
    else:
      condition = lambda: i > end_value.value
    
    while condition():
      context.symbolTable.set(node.varNameTk.value, Number(i))
      i += step_value.value

      value = res.register(self.visit(node.body_node, context))
      if res.shouldReturn() and res.loopShouldContinue == False and res.loopShouldBreak == False: return res
      
      if res.loopShouldContinue:
        continue
      
      if res.loopShouldBreak:
        break

      elements.append(value)

    return res.success(
      Number.null if node.should_return_null else  # type: ignore
      List(elements).set_context(context).set_pos(node.pStart, node.pEnd)
    )

  def visit_WhileNode(self, node, context):
    res = RTResult()
    elements = []

    while True:
      condition = res.register(self.visit(node.condition_node, context))
      if res.shouldReturn(): return res

      if not condition.is_true():
        break

      value = res.register(self.visit(node.body_node, context))
      if res.shouldReturn() and res.loopShouldContinue == False and res.loopShouldBreak == False: return res

      if res.loopShouldContinue:
        continue
      
      if res.loopShouldBreak:
        break

      elements.append(value)

    return res.success(
      Number.null if node.should_return_null else  # type: ignore
      List(elements).set_context(context).set_pos(node.pStart, node.pEnd)
    )

  def visit_FuncDefNode(self, node, context):
    res = RTResult()

    func_name = node.varNameTk.value if node.varNameTk else None
    body_node = node.body_node
    arg_names = [arg_name.value for arg_name in node.arg_name_toks]
    func_value = Function(func_name, body_node, arg_names, node.should_auto_return).set_context(context).set_pos(node.pStart, node.pEnd)
    
    if node.varNameTk:
      context.symbolTable.set(func_name, func_value)

    return res.success(func_value)

  def visit_CallNode(self, node, context):
    res = RTResult()
    args = []

    value_to_call = res.register(self.visit(node.nodeToCall, context))
    if res.shouldReturn(): return res
    value_to_call = value_to_call.copy().set_pos(node.pStart, node.pEnd)

    for arg_node in node.argNodes:
      args.append(res.register(self.visit(arg_node, context)))
      if res.shouldReturn(): return res
    
    print(value_to_call)

    return_value = res.register(value_to_call.execute(args))
    if res.shouldReturn(): return res
    return_value = return_value.copy().set_pos(node.pStart, node.pEnd).set_context(context)
    return res.success(return_value)

  def visit_ReturnNode(self, node, context):
    res = RTResult()

    if node.node_to_return:
      value = res.register(self.visit(node.node_to_return, context))
      if res.shouldReturn(): return res
    else:
      value = Number.null # type: ignore
    
    return res.successReturn(value)

  def visit_ContinueNode(self, node, context):
    return RTResult().successContinue()

  def visit_BreakNode(self, node, context):
    return RTResult().successBreak()
