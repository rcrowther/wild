
#! how it should be
#! unused
class OrderedDependency():
    
    def eq(self, that):
       pass
    
    def isFirst(self, that):
       pass
    
    def isLast(self, that):
       pass
    
    def isBefore(self, xs):
       pass
    
    def isAfter(self, xs):
       pass
    
    def before(self, that):
       '''
       Immediate edges, not the whole tree
       '''
       pass
    
    def after(self, that):
       '''
       Immediate edges, not the whole tree
       '''
       pass
    
    def requireBefore(self, xs):
       '''
       Must appear somewhere before
       '''
       pass
    
    def requireAfter(self, xs):
       '''
       Must appear somewhere after
       '''
       pass
    
    def placeBefore(self, xs):
       '''
       Place before, if appears
       '''
       pass
    
    def placeAfter(self, xs):
       '''
       Place after, if appears
       '''
       pass
