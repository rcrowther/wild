#!/usr/bin/python3



from enumerations import RegisterIndex

#! better handling of mmx and sse
#? inheriting Register index is rubbissh, is a classwide var/namespace,
# but not fighting with Python, possibly specialist, inheritance
#? isn't this architecture *register* data? Architecture
# may contain data about available methods, about cache, about other
# things? 
class ArchitectureRegisterContext(RegisterIndex):
    '''
    @param callNoSaveRequiredRegisterNames registers usable outside subprograms which a call must by convention restore, so no save required.
    '''
    #! do we  need a list for general registers, and a backing list?
    def __init__(
      self,
      registerNames,
      generalIdxs,
      callConventionIdxs,
      callNoSaveRequiredIdxs,
      returnRegisterIdx,
      floatReturnIdx,
      stackPointerIdx,
      hasMMX = False
      ):
      self.registerNames = registerNames
      self.registerNamesSize = len(registerNames)
      self.generalIdxs = generalIdxs
      self.generalIdxsSize = len(generalIdxs)
      self.callConventionIdxs = callConventionIdxs
      self.callConventionIdxsSize = len(callConventionIdxs)
      # preserved accross function call: RBX RBP ESP R12 R13 R14 R15
      self.callNoSaveRequiredIdxs = callNoSaveRequiredIdxs
      self.callNoSaveRequiredSize = len(callNoSaveRequiredIdxs)
      self.RETURN = returnRegisterIdx
      self.FLOAT_RETURN = floatReturnIdx
      self.STACK_POINTER = stackPointerIdx
      # return register: rax, rdx
      self.hasMMX = hasMMX
      self.hasSSE = False


    def callRegisterTake(self, until):
      '''
      idx until convention register location from 0 until this value 
      return list of register or stack idx
      '''
      return [self.callConventionIdxs[i]  if (i < self.callConventionIdxsSize) else self.STACK for i in range(until)]

    #def _getRegister(self, idx):
    #    return idx if (idx < self.registerNamesSize) else self.STACK

    def getGeneralRegister(self, idx):
      '''
      idx general register location idx
      return register or stack idx
      '''
      return self.generalIdxs[idx] if (idx < self.generalIdxsSize) else self.STACK

    def getCallRegister(self, idx):
      '''
      idx call convention register location idx
      return register or stack idx
      '''
      return self.callConventionIdxs[idx] if (idx < self.callConventionIdxsSize) else self.STACK


   #? Unused, but should be used.
    def isSaveRequired(self, idx):
      if (idx == STACK):
          return False
      else:
          return (not (idx in self.callNoSaveRequiredIdxs))

    def registerToString(self, idx):
      '''
      Will not return stack - asserted
      idx register or other RegisterIndex idx
      return register string
      '''
      assert (idx < self.registerNamesSize)
      if (idx < 0):
          return RegisterIndex.__str__(self, idx)
      else:
          return self.registerNames[idx]

    def generalRegisterToString(self, idx):
      '''
      idx general register location idx
      return register or stack string
      '''
      if (idx < self.generalIdxsSize):
          return self.registerNames[self.generalIdxs[idx]]
      else:
          return self.STACK_STR

    def callRegisterToString(self, idx):
      '''
      idx call register location idx
      return register or stack string
      '''
      if (idx < self.callConventionIdxsSize):
          return self.registerNames[self.callConventionIdxs[idx]]
      else:
          return self.STACK_STR

    def __str__(self):
      b = []

      b.append('general registers:')
      first = True
      for i in range(self.generalIdxsSize):
         if first:
           first = False
         else:
           b.append(',')
         b.append(self.generalRegisterToString(i))

      b.append(', call-convention registers:')
      first = True
      for i in range(self.callConventionIdxsSize):
         if first:
           first = False
         else:
           b.append(',')
         b.append(self.callRegisterToString(i))

      b.append(', no-save-required registers:')
      first = True
      for i in self.callNoSaveRequiredIdxs:
         if first:
           first = False
         else:
           b.append(',')
         b.append(self.registerNames[i])
      b.append(', return register:')
      b.append(self.registerToString(self.RETURN))
      b.append(', float return register:')
      b.append(self.registerToString(self.FLOAT_RETURN))
      b.append(', stack pointer register:')
      b.append(self.registerToString(self.STACK_POINTER))
      # return register: rax, rdx

      b.append(', hasMMX:')
      b.append(str(self.hasMMX))
      b.append(', hasSSE:')
      b.append(str(self.hasSSE))
      return ''.join(b)

class EmptyArchitecture(ArchitectureRegisterContext):
    def __init__(self):
        ArchitectureRegisterContext.__init__(self, 
            # registerNames
            [],
            # generalRegisterNames 
            [],
            # callConventionRegisterNames
            [],
            # callNoSaveRequiredRegisterNames
            [],
            # return register
            -1,
            # return float register
            -1,
            # stack pointer register
            -1,
            # hasMMX
            False
            )

EmptyArchitecture = EmptyArchitecture()

class X64ArchitectureRegisterContext(ArchitectureRegisterContext):
    def __init__(self):
        ArchitectureRegisterContext.__init__(self, 
            # registerNames
            ['rax', 'rbx', 'rcx', 'rdx', 'rdi', 'rsi', 'rcx', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'r10', 'r11', 'r12', 'r13', 'r15', 'rbp', 'XMM0'],
            # generalRegisterNames
            #['rax', 'rbx', 'rcx', 'rdx', 'rdi', 'rsi', 'rcx', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'r10', 'r11', 'r12', 'r13', 'r15', 'rbp'],
            [0, 1, 2, 3, 4, 5, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            # callConventionRegisterNames
            #['rax', 'rdi', 'rsi', 'rdx', 'rcx', 'r8', 'r9'],
            [0, 4, 5, 3, 2, 14, 15],
            # callNoSaveRequiredRegisterNames
            # *is* preserved across function call
            # RBX RBP ESP R12 R13 R14 R15?
            # Can be used in general, as well as calls?
            #['rax', 'rdi', 'rsi', 'rdx', 'rcx', 'r8', 'r9', 'r10', 'r11'],
            [0, 4, 5, 3, 2, 14, 15, 16, 17],
            # return register: rax, rdx
            0,
            #'XMM0',
            22,
            # stackPointerIdx
            # rbp?
            21,
            # hasMMX
            True
            )


#ctx = X64Context
#print(ctx.registerToString(0))
#print(ctx.registerToString(3))
