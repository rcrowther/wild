
from Kinds import Kind, Any, IntegerKind, StringKind

from collections import namedtuple

#SymbolData = namedtuple('SymbolData', 'isDefined dataRef')


class DuplicateDefinitionException(Exception):
    pass

def newData(isDefined, refData = None):
    return {'isDefined' : isDefined, 'refData' : refData}


# where to hold pos?
# and scope? Here, I think...
class SymbolTable():
    '''
    @param preset dict of key, refData. clear() restores to these.
    '''
    def __init__(self, presetAttrs = {}):
      self.underlying = {}
      self.presets = {}
      for k, v in presetAttrs.items():
        self.presets[k] = newData(True, v)
      self.clear()

    def define(self, k): 
      '''
      If defined already, throws exception
      Updates existing data, or creates if not existing.
      '''
      if k in self.underlying:
        if (self.underlying[k]['isDefined'] == False):
          self.underlying[k]['isDefined'] = True
        else:
          raise DuplicateDefinitionException()
      else:
        self.underlying[k] = newData(True)

    def add(self, k):
      '''
      Only adds if not existing.
      '''
      #NB: items may be called before definition
      # Python dictionaries do not allow duplicate keys
      # However, we need to test so no value data
      # is overwritten
      if (not self.exists(k)):
        self.underlying[k] = newData(False)

    def clear(self):
      '''
      Replace all entries with presets.
      '''
      self.underlying = self.presets

    def get(self, k): 
      return self.underlying[k]

    def exists(self, k):
      return k in self.underlying

    #def dataAddString(self, b, data):
    #   b.append(str(data['isDefined']))
    #   return b

    def toString(self):
       b = []
       first = True
       b.append('{')
       for k, v in self.underlying.items():
          if (first):
            first = False
          else:
            b.append(', ')
          b.append(str(k))
          b.append(' -> ')
          b.append(str(v))

       b.append('}')
       return ''.join(b)

# These work anywhere
keyKinds = [
Any,
IntegerKind,
StringKind
]
kindSymbolTable = SymbolTable({e.name : e for e in keyKinds})

keyExpressionActions = [
'+',
'-',
'*',
'%'
]
expressionActionSymbolTable = SymbolTable({e : None for e in keyExpressionActions})


