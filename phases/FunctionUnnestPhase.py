#!/usr/bin/python3


from Phase import Phase
from TokenSyntaxer import TokenSyntaxer
#from reporters import Reporter
from phases.TreeActions import FuncUnnest

# As Subcomponent
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
    def __init__(self):

        Phase.__init__(self,
            "funcUnnest",
            "Unnest custom functions",
            True
            )


    def run(self, compilationUnit):
      tree = compilationUnit.tree
      FuncUnnest(tree)


