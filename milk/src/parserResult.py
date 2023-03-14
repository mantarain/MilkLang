
#| Parser helper class |#

class ParseResult:
  def __init__(self):
    self.error = None
    self.node = None
    self.lastRegisteredAdvanceCount = 0
    self.advanceCount = 0
    self.reverseCount = 0

  def register_advancement(self):
    self.lastRegisteredAdvanceCount = 1
    self.advanceCount += 1

  def register(self, res):
    self.lastRegisteredAdvanceCount = res.advanceCount
    self.advanceCount += res.advanceCount
    if res.error: self.error = res.error
    return res.node

  def try_register(self, res):
    if res.error:
      self.reverseCount = res.advanceCount
      return None
    return self.register(res)

  def success(self, node):
    self.node = node
    return self

  def failure(self, error):
    if not self.error or self.lastRegisteredAdvanceCount == 0:
      self.error = error
    return self
