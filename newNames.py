
# TODO: A class is surely way too heavy.
# A global func could do this
# unless we get to multithreading?
# ... But to wrap in Python, it's a class.
# TODO: is triple '$' a good idea?
# One per compilation unit, and also one in the parser?
class NewName():
    def __init__(self):
      self._unprefixedCounter = 0
      # String -> Int
      self._prefixCounters = {}

    def get(self):
      self._unprefixedCounter += 1
      return '$' + str(self._unprefixedCounter) + '$'


    def getPrefixed(self, prefix):
      b = []
      for c in prefix:
          if(
          c == '<'
          or c == '>'
          or c == '['
          or c == ']'
          ):
              b.append('$')
          else:
              b.append(c)
      safePrefix = ''.join(b)
      if (not (safePrefix in self._prefixCounters)):
          self._prefixCounters[safePrefix] = 0
      self._prefixCounters[safePrefix] += 1
      return safePrefix + str(self._prefixCounters[safePrefix])


