#!/usr/bin/python3


from Phase import Phase
from TokenSyntaxer import TokenSyntaxer
#from reporters import Reporter
from phases.TreeActions import Intern

# As Subcomponent
class InternPhase(Phase):
    '''
    '''
    def __init__(self, expSymbolTable, reporter, settings):
        self.reporter = reporter
        self.settings = settings
        self.expSymbolTable = expSymbolTable

        Phase.__init__(self,
            "intern",
            "add symbols to the symbol table",
            True
            )


    def run(self, compilationUnit):
      tree = compilationUnit.tree
      Intern(tree, self.expSymbolTable, self.reporter)


