


# needs history?
# would include modules as a class? 
# packages?
# abstract?
# alias?
# super
# this
# method
# module positioning? Not here, keep pure for derivation calculation?

# TOCDR: Kinds need to be created with name but no parents or other type
# data, if used before declaration?
# Multipokle pararents, or single arents and interface? Will this make any difference, given both need searching?
# Maintain individual lists, or links (links, probably)?
# How to efficiently search? Usual way, provide data to determine direction of search, but what would that be?
# better to search down or up tree? Can this be determined from the type and the target? Would need to compare levels, but not possible with a graph search, is it?
# What is Scala linearisation, again?
class BaseKind():
    '''
    Represents a kind (type)
    Kinds carry their ancestory in parents.  
    '''
    # see baseTypeSeq
    def __init__(self, name, parents = []):
        self.name = name
        '''
        Parents of this kind.    
        Array of Kinds. Will end in 'Any'.
        '''
        self.parents = parents
     
    def addString(self, b):
     #if (self != Any):
      b.append(self.name)
      return b

    '''
    def _toFrameString(self, b):
        if (self != Any):
            b.append(self.name)
        return b
    '''
    def toString(self):
        return ''.join(self.addString([]))


'''
Base of all real kinds (non-func?).
has no parents.
'''
Any = BaseKind('Any', [])

# May be NoKind e.g. func returns, or or some kind based in Any.
# Used for basic initialising. 
UnknownKind = BaseKind('UNKNOWN_KIND', [Any])



# For example, no statement needed for contents or non-return funcs.
NoKind = BaseKind('NO_KIND', [Any])


#class SimpleKind(BaseKind):
#    '''
#    No content, so primitive type
#    '''
#    def __init__(self, name):
#        BaseKind.__init__(self, name)


# kind is a tree because it prints? is that enough?
# how does a container kind inherit?
class Kind(BaseKind):
    '''
    Contains a list of types
    '''
    def __init__(self, name, parents = []):
        BaseKind.__init__(self, name, parents)
        # content kinds can be multiple for fields 
        # e.g. Tuples, Records
        self.contentKinds = []

    # Can only be done once?
    def setContentKinds(self, names):
        for n in names:
            k = Kind(name)
            self.contentKinds.append(k)
        return self.contentKinds

    def appendContentKind(self, name):
        k = Kind(name)
        self.contentKinds.append(k)
        return k

    def addString(self, b):
        if (self != Any):
            b.append(self.name)
            if (self.contentKinds):
               b.append('[')
               first = True
               for k in self.contentKinds:
                   if (first):
                       first = False
                   else:
                       b.append(' ')
                   k.addString(b)
               b.append(']')
        return b

    '''
    def _toFrameString(self, b):
        if (self != Any):
            b.append(self.name)
            if (self.contentKinds):
               b.append('[')
               first = True
               for k in self.contentKinds:
                   if (first):
                       first = False
                   else:
                       b.append(' ')
                   k._toFrameString(b)
               b.append(']')
        return b
     '''

## Basics/Atoms


StringKind = Kind('String', [Any]) 
IntegerKind = Kind('Int', [Any])
FloatKind = Kind('Float', [Any])
_utf8 = Kind('UTF', [StringKind, Any])
_utf8.contentKinds.append(Kind('8', [Any]))
