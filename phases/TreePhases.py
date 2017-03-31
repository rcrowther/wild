


from Phase import Phase
from TokenSyntaxer import TokenSyntaxer
#from reporters import Reporter
from phases.TreeActions import MarkNormalize, RemoveComments, SplitVals

#! need a cleanup phase, at least to remove comments
###################################################
class RemoveCommentsPhase(Phase):
    '''
    Removes comments from the tree
    '''
    def __init__(self, reporter):
        self.reporter = reporter

        Phase.__init__(self,
            "RemoveComments",
            "Removes comments from the tree",
            True
            )


    def run(self, compilationUnit):
      tree = compilationUnit.tree
      RemoveComments(tree, self.reporter)



###################################################
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



##################################################
class SplitValuesPhase(Phase):
    '''
    '''
    def __init__(self, reporter):
        self.reporter = reporter

        Phase.__init__(self,
            "SplitValues",
            "Splits value expressions into definitions and assignments",
            True,
            placeAfterSeq=['MarkNormalize']
            )


    def run(self, compilationUnit):
      tree = compilationUnit.tree
      SplitVals(tree, self.reporter)





