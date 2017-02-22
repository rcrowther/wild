#!/usr/bin/python3


from Phase import Phase
#from TokenSyntaxer import TokenSyntaxer
#from reporters import Reporter
from phases.NASMActions import NASMPreprocess, UnaryMinus

# As Subcomponent
class UnaryMinusPhase(Phase):
    '''
    Compress plus/minus sign expression-wrapped Constant 
    ...to Constant with signed numeric content 
    (for consistency, the token syntaxer outputs like this).
    Must go after markNormalise (currently)
    '''
    def __init__(self, reporter, settings):
        self.reporter = reporter
        self.settings = settings

        Phase.__init__(self,
            "UnaryMinus",
            "Replace minus expression with constants with minus constant",
            True
            )


    def run(self, compilationUnit):
      tree = compilationUnit.tree
      UnaryMinus(tree, self.reporter)


