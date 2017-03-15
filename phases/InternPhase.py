#!/usr/bin/python3


from Phase import Phase
from TokenSyntaxer import TokenSyntaxer
#from reporters import Reporter
from phases.TreeActions import Intern

# As Subcomponent
#! Before or after normalisation? That is the question.
#! Normalisation changes var names, so likely after.
#! shame, because it's easier before.
#? Allow redefinitions? yes... += 
#! or is that extended definitions? (+= on strings?)
class InternPhase(Phase):
    '''
    '''
    def __init__(self, expSymbolTable, reporter, settings):
        self.reporter = reporter
        self.settings = settings
        self.expSymbolTable = expSymbolTable

        Phase.__init__(self,
            "Intern",
            "add symbols to the symbol table",
            True
            )


    def run(self, compilationUnit):
      tree = compilationUnit.tree
      Intern(tree, self.expSymbolTable, self.reporter)


