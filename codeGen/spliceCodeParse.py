from Position import Position
#from Reporter import Reporter
from reporters import Reporter
from codeGen import spliceCode
import sys


#! repeated data. see iterator
tokens = {
        'error' : 0,
        'newline' : 1,
        'comment' : 2,
        'item' : 3
        }

tokenToName = {v: k for k, v in tokens.items()}

#! needs symbol table, detect repeats, missing external decs, etc.
class SpliceCodeParse:
    '''
    Splicecode is final ordersed and implemented, lacks only generics of registers etc.
    This can check syntax, for handwriting say.
    '''
    def __init__(self, tokenItr, reporter):
        self.it = tokenItr
        self.reporter = reporter
        self.tok = tokens['error']
        self.prevLine = 1
        self.prevOffset = 1
        self.op1 = ""
        self.op2 = ""
        self.cmd = ""
        self.b = []
        # let's go
        self.root()

    def _next(self):
        self.prevLine = self.it.lineCount()
        self.prevOffset = self.it.lineOffset()
        self.tok = self.it.__next__()

    def position(self):
        return Position(self.it.source(), self.prevLine, self.prevOffset)

    def reportError(self, msg):
        self.reporter.error(msg, self.position())
        sys.exit("Error message")

    def isToken(self, tokenName):
       return (tokens[tokenName] == self.tok)

    def error(self):
      commit = self.isToken('error')
      if (commit):
        #print('parsed error')
        self._next()
      return commit

    def comment(self):
      commit = self.isToken('comment')
      if (commit):
        #print('parsed comment')
        self._next()
      return commit
 
    def newline(self):
      commit = self.isToken('newline')
      if (commit):
        #print('parsed newline')
        self._next()
      return commit

    def noOp(self):
      (
      self.comment()
      or self.newline()
      or self.error()
      )

    def operand(self):
      commit = self.isToken('item')
      if (commit):
        #print('parsed operand')
        tokenStr = self.it.textOf()
        self._next()
      return commit


    def tokenFromName(self, name):
      try:
        return spliceCode.nameToCode[name]
      except:
        return None

    def operandCount(self, token):
      try:
        return spliceCode.codeToOperandCount[token]
      except:
        return None

    def opLine(self):
      commit = self.isToken('item')
      if (commit):
        #print('parsed op line')
        tokenStr = self.it.textOf()
        self._next()
        #! can throw
        token = self.tokenFromName(tokenStr)
        if (not token):
            self.reportError('Unknown command name: {0}'.format(tokenStr))
        opCount = self.operandCount(token)
        if (not opCount):
            name = splaceCode.codeToName[token]
            self.reportError('Unknown operand count name: {0}'.format(name))
        i = opCount
        while i > 0:
          if(not self.operand()):
            self.reportError('Expected parameter parameterCount:{0}  found:{1}'.format(opCount, tokenToName[self.tok]))
          i -= 1
        #if (not(self.newline() or self.comment())):
        if (not(self.isToken('newline') or self.isToken('comment'))):
            print(self.it.textOf())
            self.reportError('Expected comment or newline  found:{0}'.format(tokenToName[self.tok]))
      return commit



    def root(self):
      try:
        while(True):
          (
          self.noOp()
          or self.opLine()
          )
      except StopIteration:
        self.reporter.info('bytecode lint ok')
      except:
        self.reporter.error('bytecode lint failed')
       
      
'''
def parse(source):
    srcStr = source.get()
    srcLex = srcStr.split()
    b = []
    i = 0
    limit = len(srcLex)
    while i < limit:
      lex = srcLex[i]
      token = spliceCode.nameToCode[lex]
      b.append(token)
      i += 1
      limit2 = i + spliceCode.codeToOperandCount[token]
      while i < limit2:
        #b.append(str(tokenArray[i]))
        i += 1
    #b.append('\n')

    return ''.join(b)
'''
