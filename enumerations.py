
from enum import Enum

class ConstantKind(Enum):
    integerNum = 1
    floatNum = 2
# No!
#CODEPOINT_CONSTANT = 3
    string = 3

#? deprecated?
class FuncRenderType(Enum):
    # Used as default - Constants/Marks?
    NOT_FUNC = 0
    # is a call. This may be adapted by a phase if the
    # func code is capable of being rendered directly to
    # machine code 
    CALL = 1
    # was/is CONSTANT trre node
    #MACHINE_CONSTANT = 1
    #CODE_CONSTANT = 1
    #MACHINE_DATACALL = 1
    #CODE_DATACALL = 1
    #MACHINE_FUNCCALL = 1
    #CODE_FUNCCALL = 1
    DEF = 2
    # a call renderable directly to 32 bit machine code
    MCODE32 = 5
    # a call renderable directly to 64 bit machine code
    MCODE64 = 6


class RenderKind(Enum):
    '''
    annotates tree nodes, which are a loose collection of structures,
    into general machine-orientated structures. See also 'MachineRenderKind'
    '''
    # should never be unknown, except as initialiser.
    unknown = 0
    constant = 1
    data = 2
    function = 3

#? may also include strings?
class MachineRenderKind(Enum):
    # Used as default 
    undetermined = 0
    # is a call. This may be adapted by a phase if the
    # func code is capable of being rendered directly to
    # machine code 
    # a call renderable directly to 8 bit machine code
    num8bit = 1
    # a call renderable directly to 32 bit machine code
    num32bit = 2
    # a call renderable directly to 64 bit machine code
    num64bit = 3

# NB: Not a Python enum...
# A base usable on it's own
# until inherited into an Architecture context and so extended?
#? not convinced here, by implementation and contents
class RegisterIndex():

    '''
 A register is a return register---where we need this
 value to arrive. In the case of params,
 the parameter mark appears in the AST tree, but there
 is no need for analysis for machine code. register/stack
 application places the params.
 This mark identifies AST expressions known to have no linearised expression.  
    '''
    UNALLOCATED = -1
    STACK = -2
    ABSTRACT = -3

    UNALLOCATED_STR = 'unallocated'
    STACK_STR = 'stack'
    ABSTRACT_STR = 'abstract'


    #def __init__(self):

    def __str__(self, idx):
        if (idx == self.UNALLOCATED):
          return 'unallocated'
        elif (idx == self.STACK):
          return 'stack'
        elif (idx == self.ABSTRACT):
          return 'abstract'
