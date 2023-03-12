#######################################
# NODES
#######################################

class NumberNode:
  def __init__(self, tk):
    self.tk = tk

    self.pStart = self.tk.pStart
    self.pEnd = self.tk.pEnd

  def __repr__(self):
    return f'{self.tk}'

class StringNode:
  def __init__(self, tk):
    self.tk = tk

    self.pStart = self.tk.pStart
    self.pEnd = self.tk.pEnd

  def __repr__(self):
    return f'{self.tk}'

class ListNode:
  def __init__(self, elementNodes, pStart, pEnd):
    self.elementNodes = elementNodes

    self.pStart = pStart
    self.pEnd = pEnd

class VarAccessNode:
  def __init__(self, varNameTk):
    self.varNameTk = varNameTk

    self.pStart = self.varNameTk.pStart
    self.pEnd = self.varNameTk.pEnd

class VarAssignNode:
  def __init__(self, varNameTk, valueNode):
    self.varNameTk = varNameTk
    self.valueNode = valueNode

    self.pStart = self.varNameTk.pStart
    self.pEnd = self.valueNode.pEnd

class BinOpNode:
  def __init__(self, leftNode, opTk, rightNode):
    self.leftNode = leftNode
    self.opTk = opTk
    self.rightNode = rightNode

    self.pStart = self.leftNode.pStart
    self.pEnd = self.rightNode.pEnd

  def __repr__(self):
    return f'({self.leftNode}, {self.opTk}, {self.rightNode})'

class UnaryOpNode:
  def __init__(self, opTk, node):
    self.opTk = opTk
    self.node = node

    self.pStart = self.opTk.pStart
    self.pEnd = node.pEnd

  def __repr__(self):
    return f'({self.opTk}, {self.node})'

class IfNode:
  def __init__(self, cases, elseCase):
    self.cases = cases
    self.elseCase = elseCase

    self.pStart = self.cases[0][0].pStart
    self.pEnd = (self.elseCase or self.cases[len(self.cases) - 1])[0].pEnd

class ForNode:
  def __init__(self, varNameTk, startValueNode, endValueNode, stepValueNode, bodyNode, shouldReturnNull):
    self.varNameTk = varNameTk
    self.startValueNode = startValueNode
    self.endValueNode = endValueNode
    self.stepValueNode = stepValueNode
    self.bodyNode = bodyNode
    self.shouldReturnNull = shouldReturnNull

    self.pStart = self.varNameTk.pStart
    self.pEnd = self.bodyNode.pEnd

class WhileNode:
  def __init__(self, conditionNode, bodyNode, shouldReturnNull):
    self.conditionNode = conditionNode
    self.bodyNode = bodyNode
    self.shouldReturnNull = shouldReturnNull

    self.pStart = self.conditionNode.pStart
    self.pEnd = self.bodyNode.pEnd

class FuncDefNode:
  def __init__(self, varNameTk, argNameTks, bodyNode, shouldAutoReturn):
    self.varNameTk = varNameTk
    self.argNameTks = argNameTks
    self.bodyNode = bodyNode
    self.shouldAutoReturn = shouldAutoReturn

    if self.varNameTk:
      self.pStart = self.varNameTk.pStart
    elif len(self.argNameTks) > 0:
      self.pStart = self.argNameTks[0].pStart
    else:
      self.pStart = self.bodyNode.pStart

    self.pEnd = self.bodyNode.pEnd

class CallNode:
  def __init__(self, nodeToCall, argNodes):
    self.nodeToCall = nodeToCall
    self.argNodes = argNodes

    self.pStart = self.nodeToCall.pStart

    if len(self.argNodes) > 0:
      self.pEnd = self.argNodes[len(self.argNodes) - 1].pEnd
    else:
      self.pEnd = self.nodeToCall.pEnd

class ReturnNode:
  def __init__(self, node_to_return, pStart, pEnd):
    self.nodeToReturn = node_to_return

    self.pStart = pStart
    self.pEnd = pEnd

class ContinueNode:
  def __init__(self, pStart, pEnd):
    self.pStart = pStart
    self.pEnd = pEnd

class BreakNode:
  def __init__(self, pStart, pEnd):
    self.pStart = pStart
    self.pEnd = pEnd
