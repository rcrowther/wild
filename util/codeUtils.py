
def multilineToString(text):
    '''
    if newlines returns an abbreviation
    '''
    idx = text.find('\n')
    cut = min(idx, 17)
    return text[:cut] + '...' if (idx != -1) else text


class StdPrint():
    '''
    '''
    def __init__(self, entitySuffix):
        self.entitySuffix = entitySuffix


    def addString(self, b):
       b.append('addString undefined!')
       return b

    def __str__(self):
      '''
      Print this element.
      For the whole tree, see VisitorBuilder
      '''
      b = []
      b.append(self.entitySuffix)
      b.append('(')
      self.addString(b)
      b.append(')')
      return "".join(b)


class StdSeqPrint(StdPrint):
    '''
    '''
    def __init__(self, entitySuffix):
        StdPrint.__init__(self, entitySuffix)

    def addStringWithSeparator(self, b, sep):
       '''
       first = True
       for k, v in self.settings.items():
       for e in seq:
          if (first):
            first = False
          else:
            b.append(', ')
          b.append(str(e))
       return b
       '''
       b.append('addStringWithSeparator undefined!')
       return b

    def addString(self, b):
       return self.addStringWithSeparator(b, ', ')





