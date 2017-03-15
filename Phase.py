
from orderedDependency.GraphOrderable import GraphOrderable

# As Subcomponent
# TODO: dependancies?
class Phase(GraphOrderable):
    '''
    Acts on a Compilation Unit (containing a tree and source data)
    Usually the action would be a transformaton of the tree, but
    it may be for data gathering, or other purposes.
    A phase should never throw errors. If it could throw an error,
    the Phase should carry a reporter attribute, to report.
    run() should be implemented, to perform the action.

    @param isInternal this phase is not a plugin addittion.
    '''
    def __init__(self,
        name,
        description,
        isInternal,
        after = None,
        placeAfterSeq = [],
        placeBeforeSeq = []
        ):
        GraphOrderable.__init__(self, 
          name, 
          after, 
          placeAfterSeq, 
          placeBeforeSeq
          )
        #self.name = name
        self.description = description
        self.isInternal = isInternal

    def run(self, compilationUnit):
        pass
