#!/usr/bin/python3


from Phase import Phase
#from reporters import Reporter
#from phases.TreeActions import  
from phases.LinearizeActions import FunctionCategorize, RenderCategorizePropagate, FuncUnnest, FuncUnnest2, ParseLiveRanges, ChooseRegisters, ApplyRegistersToTree, TreeToSplicecode


##################################################################
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

##################################################################


class RenderCategorizePropagatePhase(Phase):
    '''
    Since this includes a context, place as late as possible, but before 
    other machine code phases (which rely on this)
    '''
    def __init__(self, mCodeContext, reporter, settings):
        self.mCodeContext = mCodeContext
        self.reporter = reporter
        self.settings = settings

        Phase.__init__(self,
            "RenderCategorizePropagate",
            "Passes rendering categorisation along the tree",
            True,
            placeAfterSeq=['MarkNormalize', 'FunctionCategorizePhase']
            )


    def run(self, compilationUnit):
      tree = compilationUnit.tree
      RenderCategorizePropagate(self.mCodeContext, tree, self.reporter)

################################################################
class FunctionUnnestPhase(Phase):
    '''
    Only needed if a code generator has a call convention using registers e.g. i64, but not standard i32.
    Take this,
       func1(param1, param2, func2())
    As machine code, func1 will set up param1 and param2 in registers. But the call to func2 then forces the param1/param2 registers to be backed up, to satisfy func2() call convention. Compare to an unnested version,
       tmp = func2()
       func1(param1, param2, tmp)
    where at most the func2() result needs to be moved to param slot 3.

    This would not apply to machine codeable functions, which can be slotted in place?
    Must be run after FunctionCategorize. Should come after Uniminus.
    '''
    def __init__(self, architectureContext):
        self.architectureContext = architectureContext
        Phase.__init__(self,
            "FunctionUnnest",
            "Unnest custom functions",
            True
            )


    def run(self, compilationUnit):
      tree = compilationUnit.tree
      FuncUnnest2(tree, compilationUnit.newNames, self.architectureContext)



################################################
class ParseLiveRangesPhase(Phase):
    '''
    Should be run after FuncUnnest.
    '''
    def __init__(self, reporter):
        self.reporter = reporter

        Phase.__init__(self,
            "ParseLiveRanges",
            "Identify and collect the live ranges of variables",
            True,
            placeAfterSeq=['FuncUnnest']
            )


    def run(self, compilationUnit):
      tree = compilationUnit.tree
      p = ParseLiveRanges(tree, self.reporter)
      compilationUnit.liveRanges = p.result()

################################################
class ChooseRegistersPhase(Phase):
    '''
    Must be run after ParseLiveRangesPhase.
    '''
    def __init__(self, architectureContext, reporter):
        self.reporter = reporter
        self.architectureContext = architectureContext
        Phase.__init__(self,
            "ChooseRegisters",
            "allocate registers or stack marks to unallocated vars",
            True,
            # otherwise, the phase returns nothing
            placeAfterSeq=['ParseLiveRangesPhase']
            )


    def run(self, compilationUnit):
      tree = compilationUnit.tree
      #print(compilationUnit.liveRanges)
      #? Using callNoSaveRequired registers is ok, but not all possible registers.
      # what we really need is registerNames, and where not callNoSaveRequired, to insert a push/pop save
      registerMap = ChooseRegisters(
        compilationUnit.liveRanges, 
        self.architectureContext.callNoSaveRequired
        )
      #print(str(registerMap.result()))

      #compilationUnit.liveRanges = alloc.result()
      ApplyRegistersToTree(tree, registerMap.result(), self.reporter)

###################################################
class ToSplicecode(Phase):
    '''
    Should be run after ChooseRegistersPhase.
    '''
    def __init__(self, reporter):
        self.reporter = reporter

        Phase.__init__(self,
            "ToSplicecode",
            "Convert an AST tree to splicecode",
            True,
            placeAfterSeq=['ChooseRegistersPhase']
            )


    def run(self, compilationUnit):
      tree = compilationUnit.tree
      p = TreeToSplicecode(tree, self.reporter)
      print('new splicecode:')
      print(p.result())
