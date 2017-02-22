

from collections import namedtuple

ScopeData = namedtuple('ScopeData', 'name owner nestingDepth')
#! def toString(self): return "{0} (depth = {1})".format(name, nestingDepth)
 
#? kinds would contain scopes?
#! do using simple scopeOwner?
#! member search through owners too, recursivly?
class Scope():
    def __init__(self, nestLevel = 0):
      self.underlying = {}
      self.nestLevel = nestLevel

    def isEmpty(self):
      return (self.size() == 0)

    def size(self):
      return len(self.underlying)

    def append(self, name):
      e = ScopeData(name, self, nestLevel)
      self.underlying[name] = e
      return e

    def appendAll(self, names):
      for e in names:
        self.append(e)

    def appendIfUnique(self, name):
      assert(not(name in self.underlying))
      return append(self, name)

    def contains(self, name):
      return name in self.underlying.keys()

   #! silly?
    def get(self, name):
      if (name in self.underlying):
        name
      else:
        None

    def toList(self):
      return self.underlying

    def remove(self, name):
      self.underlying = {k : v if k != name for k, v in self.underlying.items()}

    def isSubScope(self, scope):
      #! seems to ask only... contains names? but owners?
      return

    def eq(self, scope):
      #! test sub both ways?
      pass

    def newNestedScope(self, scope):
      newScope = Scope(scope.nestLevel + 1)
      #! must inherit elements?
      #! this is only a snapshot
      newScope.appendAll(scope.underlying)
      return newScope

    def addString(self, b):
      first = True
      for e in self.underlying:
         if first:
            first = False
         else:
           b.append(', ')
         b,append(e)
      return b
       
    def toString(self):
      return ''.join(addString([]))

def newScope(names *):
   newScope = Scope()
   for e in names:
     newScope.append(e)
   return newScope

class EmptyScopeBase(Scope):
    def __init__(self):
      Scope.__init__(self)

    def append(name, owner):
      sys.exit('appending to EmptyScope!')
   
EmptyScope = EmptyScopeBase()
