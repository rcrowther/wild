#!/usr/bin/python3


from Phase import Phase
#from TokenSyntaxer import TokenSyntaxer
#from reporters import Reporter
from phases.NASMActions import FunctionCategorize

# Deprecated?
class FunctionCategorizePhase(Phase):
    '''
    '''
    def __init__(self, mCodeContext, reporter, settings):
        self.mCodeContext = mCodeContext
        self.reporter = reporter
        self.settings = settings

        Phase.__init__(self,
            "Function Categorize",
            "decides how the operator in tree node should be rendered",
            True
            )


    def run(self, compilationUnit):
      tree = compilationUnit.tree
      FunctionCategorize(self.mCodeContext, tree, self.reporter)


