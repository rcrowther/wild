#!/usr/bin/python3


from Phase import Phase
#from TokenSyntaxer import TokenSyntaxer
#from reporters import Reporter
from phases.NASMActions import NASMPreprocess

# As Subcomponent
class NASMPreprocessPhase(Phase):
    '''
    NASM cann't handle $$...$ marrkup. An opening $ is ok,
    but, when removed, that leavees an initial $. So, for now,
    prefixing with 'X' (e.g. 'c' nummber literals)
    '''
    def __init__(self, reporter, settings):
        self.reporter = reporter
        self.settings = settings

        Phase.__init__(self,
            "NASMPreprocess",
            "various procession of the final tree targetted at the NASM assembler",
            True
            )


    def run(self, compilationUnit):
      tree = compilationUnit.tree
      NASMPreprocess(tree, self.reporter)


