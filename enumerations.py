
from enum import Enum

class FuncRenderType(Enum):
    NOT_FUNC = 0
    # is a call. This may be adapted by a phase if the
    # func code is capable of being rendered directly to
    # machine code 
    CALL = 1
    # a call renderable directly to 32 bit machine code
    MCODE32 = 2
    # a call renderable directly to 64 bit machine code
    MCODE64 = 3
