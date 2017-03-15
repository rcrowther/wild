


from Phase import Phase
from TokenSyntaxer import TokenSyntaxer
#from reporters import Reporter
from phases.TreeActions import MarkNormalize, UnaryMinus, FunctionCategorize

# As Subcomponent
class MarkNormalizePhase(Phase):
    '''
    Substitues symbols for marks in normalised alphanumeric form e.g. '+' becomes '$$plus$'
    Searches for significant symbols such as ! or ?, ten strips them, adding values to the tree.
    '''
    def __init__(self, reporter, settings):
        self.reporter = reporter
        self.settings = settings

        Phase.__init__(self,
            "MarkNormalize",
            "transform mark text to alphanumeric-dollar markup",
            True
            )


    def run(self, compilationUnit):
      tree = compilationUnit.tree
      MarkNormalize(tree, self.reporter)





# As Subcomponent
class UnaryMinusPhase(Phase):
    '''
    Crush plus/minus sign expression-wrapped Constant 
    to Constant with signed numeric content 
    (for consistency, the token syntaxer outputs like this).
    Must go after markNormalise (currently)
    '''
    def __init__(self, reporter, settings):
        self.reporter = reporter
        self.settings = settings

        Phase.__init__(self,
            "UnaryMinus",
            "Replace minus expression with constants with minus constant",
            True,
            placeAfterSeq=['MarkNormalize']
            )


    def run(self, compilationUnit):
      tree = compilationUnit.tree
      UnaryMinus(tree, self.reporter)



#from phases.NASMActions import FunctionCategorize

# Deprecated?
class FunctionCategorizePhase(Phase):
    '''
    Since this includes a context, place as late as possible, but before 
    other machine code phases (which rely on this)
    '''
    def __init__(self, mCodeContext, reporter, settings):
        self.mCodeContext = mCodeContext
        self.reporter = reporter
        self.settings = settings

        Phase.__init__(self,
            "FunctionCategorize",
            "decides how an operator in a tree node should be rendered",
            True,
            placeAfterSeq=['MarkNormalize']
            )


    def run(self, compilationUnit):
      tree = compilationUnit.tree
      FunctionCategorize(self.mCodeContext, tree, self.reporter)


