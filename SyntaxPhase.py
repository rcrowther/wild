#!/usr/bin/python3


from Phase import Phase
from wildio import *
from TokenSyntaxer import TokenSyntaxer
#from reporters import Reporter

# As Subcomponent
class SyntaxPhase(Phase):
    '''
    Takes a Compilation Unit (containing a tree and source data) and transforms it
    '''
    def __init__(self, reporter, settings):
        self.reporter = reporter
        self.settings = settings
        Phase.__init__(self,
            "parser",
            "read source files, make tree",
            True
            )

    def runForTokens(self, compilationUnit):
        s = compilationUnit.source
        it = StringIterator(s, s.get())
        tokenIt = TokenIterator(it)
        p = TokenSyntaxer(tokenIt, self.reporter)
        tokenStr = []
        for t in tokenIt:
          tokenStr.append(tokensToString(t))
        return ''.join(tokenStr)

    def run(self, compilationUnit):
        s = compilationUnit.source
        it = StringIterator(s, s.get())
        tokenIt = TokenIterator(it)
        p = TokenSyntaxer(tokenIt, self.reporter)
        compilationUnit.tree = p.ast()


