
import collections

class Flags:
    '''
    Base tree. 
    Tree enables constant iteration, so includes every syntax rule.
    The base class does very little and is never instatiated.
    @args dictionary of name -> value
    '''
    def __init__(self, args = {}):
      self.keys = collections.OrderedDict()
      self.data = 0
      i = 0
      for k, v in args.items():
        self.keys[k] = i
        self.data = (v << i) + self.data
        i += 1

    def get(self, k):
      return ((1 << self.keys[k]) & self.data) != 0

    def on(self, k):
       self.data = (1 << self.keys[k]) | self.data

    def off(self, k):
       self.data = ~(1 << self.keys[k]) & self.data




    def addStringSettingsData(self, b, data):
       b.append('"')
       b.append(data.description)
       b.append('", ')
       b.append(str(data.value))
       return b

    def toString(self):
       b = []
       first = True
       b.append('Flags(')
       for k, v in self.settings.items():
          if (first):
            first = False
          else:
            b.append(', ')
          b.append(str(k))
          b.append(' -> (')
          self.addStringSettingsData(b, v)
          b.append(')')
       b.append(')')
       return ''.join(b)
