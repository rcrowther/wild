#!/usr/bin/python3

#! move to enumerations?
STACK = 'stack'
'''
 A register is a return register---where we need this
 value to arrive. In the case of params, for example,
 the parameter mark appears in the AST tree, but there
 is no need for analysis for machine code. register/stack
 application places the params.
 This mark identifies AST expressions known to have no linearised expression.  
'''
ABSTRACT = 'abstract'

class ArchitectureContext():
    '''
    @param callNoSaveRequired registers usable within subprograms which the call may destroy, so no save required
    '''
    #! max/min is very crude for advanced numerical computing e.g.
    # - unsigned
    # - can the compiler code handle the numbers themselves
    # - what about endedness?
    # - and other numeric representations
    def __init__(
      self,
      maxInteger,
      minInteger,
      registerNames,
      callConventionRegisterNames,
      #! refactor to callNoSaveRequiredRegisterNames
      callNoSaveRequired,
      returnRegister,
      floatReturnRegister,
      hasMMX = False
      ):
      self.maxInteger = maxInteger
      self.minInteger = minInteger
      self.registerNames = registerNames
      self.registerNamesSize = len(registerNames)
      self.callRegisterNames = callConventionRegisterNames
      self.callRegisterNamesSize = len(callConventionRegisterNames)
      # preserved accross function call: RBX RBP ESP R12 R13 R14 R15
      self.callNoSaveRequired = callNoSaveRequired
      self.callNoSaveRequiredSize = len(callNoSaveRequired)
      self.returnRegister = returnRegister
      self.floatReturnRegister = floatReturnRegister
      # return register: rax, rdx
      self.hasMMX = hasMMX
      self.hasSSE = False

    def registerToString(self, idx):
      return self.registerNames[idx]

    def callRegisterToString(self, idx):
      return self.callRegisterNames[idx]

    def callRegisterTake(self, until):
      return self.callRegisterNames[0:until - 1]

    def getRegister(self, idx):
      if (idx < self.registerNamesSize):
        return self.registerNames[idx]
      else:
        return STACK

    def getCallRegister(self, idx):
      if (idx < self.callRegisterNamesSize):
        return self.callRegisterNames[idx]
      else:
        return STACK

   #? Unused, but should be used.
    def isSaveRequired(self, registerName):
      if (registerName == STACK):
          return False
      else:
          return (not (registerName in self.callNoSaveRequired))

class X64ArchitectureContext(ArchitectureContext):
    def __init__(self):
        ArchitectureContext.__init__(self, 
            # maxInteger
            #9223372036854775807,
            8,
            # minInteger
            #-9223372036854775808,
            -8,
            # registerNames
            ['rax', 'rbx', 'rcx', 'rdx', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'r10', 'r11', 'r12', 'r13', 'r15'],
            # callConventionRegisterNames
            ['rdi', 'rsi', 'rdx', 'rcx', 'r8', 'r9'],
            # callNoSaveRequired
            # *Not* or *is* preserved across function call: RBX RBP ESP R12 R13 R14 R15?
            # Can be used in general, as well as calls?
            ['rax', 'rdi', 'rsi', 'rdx', 'rcx', 'r8', 'r9', 'r10', 'r11'],
            # return register: rax, rdx
            'rax',
            'XMM0',
            # hasMMX
            True
            )


#ctx = X64Context
#print(ctx.registerToString(0))
#print(ctx.registerToString(3))
