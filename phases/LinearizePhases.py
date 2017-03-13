#!/usr/bin/python3


from Phase import Phase
#from reporters import Reporter
from phases.TreeActions import ParseLiveRanges, RegisterAllocate, FuncUnnest

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
            "funcUnnest",
            "Unnest custom functions",
            True
            )


    def run(self, compilationUnit):
      tree = compilationUnit.tree
      FuncUnnest(tree, compilationUnit.newNames, self.architectureContext)


# As Subcomponent
class ParseLiveRangesPhase(Phase):
    '''
    Must be run after Unnest.
    '''
    def __init__(self, reporter):
        self.reporter = reporter

        Phase.__init__(self,
            "ParseLiveRanges",
            "Identify and collect the live ranges of variables",
            True
            )


    def run(self, compilationUnit):
      tree = compilationUnit.tree
      p = ParseLiveRanges(tree, self.reporter)
      print(p.toString())
      ranges = p.result()

