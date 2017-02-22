#!/usr/bin/python3


from Phase import Phase
from graphviz.builder import GraphBuilder, DigraphBuilder

# As Subcomponent
class Phase(Phase):
    '''
    Plot something
    '''
    #! implement
    def __init__(self, settings):
        self.settings = settings

        Phase.__init__(self,
            "Graphviz?",
            "Do something",
            True
            )


    def run(self, compilationUnit):
      tree = compilationUnit.tree
      GraphBuilder(tree)


