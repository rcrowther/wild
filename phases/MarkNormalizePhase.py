#!/usr/bin/python3


from Phase import Phase
from TokenSyntaxer import TokenSyntaxer
#from reporters import Reporter
from phases.TreeActions import MarkNormalize

# As Subcomponent
class MarkNormalizePhase(Phase):
    '''
    '''
    def __init__(self, reporter, settings):
        self.reporter = reporter
        self.settings = settings

        Phase.__init__(self,
            "markNormalize",
            "transform mark text to alphanumeric-dollar markup",
            True
            )


    def run(self, compilationUnit):
      tree = compilationUnit.tree
      MarkNormalize(tree, self.reporter)


