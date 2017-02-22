
from codeGen import spliceCode

class SpliceCodeTraverser():

    def __init__(self, codeArray):
        self.tokenCallback = {
            0: self.error,
            1: self.defconst,                
            2: self.defspace,
            3: self.declExtenalFunc,
            10: self.toReg,
            11: self.fromReg,
            12: self.toParam,
            13: self.toSpace,
            14: self.fromCallReturn,
            18: self.slotProtect,
            19: self.slotRecover,
            30: self.add,
            31: self.sub,
            32: self.mult,
            33: self.div,
            35: self.remainder,
            36: self.inc,
            37: self.dec,
            40: self.shiftLeft,
            41: self.shiftRight,
            50: self.bOr,
            51: self.bAnd,
            52: self.bNot,
            53: self.bXor,
            70: self.unconditionalJump,
            71: self.unconditionalLongJump,
            72: self.indexedJump,
            73: self.jumpOnComparisonSuccess,
            80: self.cmp,
            100: self.call,
            101: self.callReturn
            }   
        self.dispatch(codeArray)
     
    def error(self, op1, op2):
        pass
        
    def defconst(self, op1, op2):
        pass
        
    def defspace(self, op1, op2):
        pass

    def declExtenalFunc(self, op1, op2):
        pass

    def toReg(self, op1, op2):
        pass

    def fromReg(self, op1, op2):
        pass

    def toParam(self, op1, op2):
        pass

    def toSpace(self, op1, op2):
        pass

    def fromCallReturn(self, op1, op2):
        pass

    def slotProtect(self, op1, op2):
        pass

    def slotRecover(self, op1, op2):
        pass

    def add(self, op1, op2):
        pass

    def sub(self, op1, op2):
        pass

    def mult(self, op1, op2):
        pass

    def div(self, op1, op2):
        pass

    def remainder(self, op1, op2):
        pass

    def inc(self, op1, op2):
        pass

    def dec(self, op1, op2):
        pass

    def shiftLeft(self, op1, op2):
        pass

    def shiftRight(self, op1, op2):
        pass

    def bOr(self, op1, op2):
        pass

    def bAnd(self, op1, op2):
        pass

    def bNot(self, op1, op2):
        pass

    def bXor(self, op1, op2):
        pass

    def unconditionalJump(self, op1, op2):
        pass

    def unconditionalLongJump(self, op1, op2):
        pass

    def indexedJump(self, op1, op2):
        pass

    def jumpOnComparisonSuccess(self, op1, op2):
        pass

    def cmp(self, op1, op2):
        pass

    def call(self, op1, op2):
        pass

    def callReturn(self, op1, op2):
        pass

    def dispatch(self, codeArray):
        i = 0
        limit = len(codeArray)
        
        while i < limit:
            cmd = codeArray[i]
            op1 = codeArray[i + 1]
            op2 = codeArray[i + 2]
            self.tokenCallback[cmd](op1, op2)
            i += 3

class ToString():
    
    def __init__(self, codeArray):
      self.codeArray = codeArray

    def addString(self, b):
        first = True
        i = 0
        limit = len(self.codeArray)
        while i < limit:
            cmd = self.codeArray[i]
            op1 = self.codeArray[i + 1]
            op2 = self.codeArray[i + 2]
            if first:
                first = False
            else:
                b.append(', ')
                
            b.append('(')
            b.append(spliceCode.codeToName[cmd])
            b.append(', ')
            b.append(op1)
            if (op2 != 'dead'):
                b.append(', ')
                b.append(op2)
            b.append(')')
            i += 3
        return b
                
    def toString(self):
        return ''.join(self.addString([]))
    
    
from codeGen import architectureContext

#! need compiler info, like what bytesize used for what word
# 1:'byte' 2:'word' 4:'dword' 8:'qword'
class toASMCode(SpliceCodeTraverser):
    
    def __init__(self, architectureContext, codeArray):
        self.b = []
        self.architectureContext = architectureContext
        SpliceCodeTraverser.__init__(self, codeArray)

    def _printOps(self, op1, op2):
        self.b.append(' ')
        self.b.append(op1)
        if (op2 != 'dead'):
            self.b.append(',')
            self.b.append(op2)
        self.b.append('\n')

    def _operandToRegOrAddress(self, op):
        '''
        op1
        '''
        if (op.isdigit()):
            paramReg = self.architectureContext.getRegister(int(op))
            #if (paramReg == architectureContext.STACK):
                #self.b.append('push ')
                #self.b.append(op2)
            self.b.append(paramReg)
        else:
          self.b.append(op)

    def _operandToAddressOrConstant(self, op):
        '''
        op2
        label or const?
        '''
        if (op.isalpha()):
          self.b.append(op)
        else:
          self.b.append(op)

    def _arithmeticOps(self, op1, op2):
        self.b.append(' ')
        self._operandToRegOrAddress(op1)
        self.b.append(',')
        self._operandToAddressOrConstant(op2)
        self.b.append('\n')

    def result(self):
        print(len(self.b))
        return ''.join(self.b)
        
    def error(self, op1, op2):
        self.b.append('error')
        self._printOps(op1, op2)
        
    #! except floats. Can't be floats?
    def defconst(self, op1, op2):
        self.b.append(op1)
        self.b.append(': equ ')
        self.b.append(op2)
        self.b.append('\n')

    def defspace(self, op1, op2):
        self.b.append(op1)
        self.b.append(': resb ')
        self.b.append(op2)
        self.b.append('\n')

    def declExtenalFunc(self, op1, op2):
        self.b.append('extern')
        self._printOps(op1, op2)

    def toReg(self, op1, op2):
        paramReg = self.architectureContext.getRegister(int(op1))
        if (paramReg == architectureContext.STACK):
            self.b.append('push ')
            self._operandToAddressOrConstant(op2)
        else:
            self.b.append('mov ')
            self.b.append(paramReg)
            self.b.append(',')
            self._operandToAddressOrConstant(op2)          
            #self._printOps(paramReg, src)
        self.b.append('\n')


    def fromReg(self, op1, op2):
        self.b.append('mov')
        self._printOps(op1, op2)

    def toParam(self, op1, op2):
        paramReg = self.architectureContext.getCallRegister(int(op1))
        if (paramReg == architectureContext.STACK):
            self.b.append('push ')
            self.b.append(op2)
        else:
            self.b.append('mov ') 
            self.b.append(paramReg) 
            self.b.append(',') 
            self._operandToAddressOrConstant(op2)        
            #self._printOps(paramReg, op2)
        self.b.append('\n')

    def toSpace(self, op1, op2):
        self.b.append('mov')
        #! how to define the size?
        self.b.append(' word ')
        self.b.append(op1)
        self.b.append(',')
        self._operandToAddressOrConstant(op2)
        self.b.append('\n')

    def fromCallReturn(self, op1, op2):
        self.b.append('mov ')
        self.b.append(self.architectureContext.returnRegister)
        self.b.append(',')
        self._operandToRegOrAddress(op1)
        self.b.append('\n')

    def slotProtect(self, op1, op2):
        self.b.append('slotProtect')
        self._printOps(op1, op2)

    def slotRecover(self, op1, op2):
        self.b.append('slotRecover')
        self._printOps(op1, op2)

    def add(self, op1, op2):
        self.b.append('add')
        self._arithmeticOps(op1, op2)

    def sub(self, op1, op2):
        self.b.append('sub')
        self._arithmeticOps(op1, op2)

    def mult(self, op1, op2):
        #! need to handle floats
        self.b.append('imul')
        self._arithmeticOps(op1, op2)

    def div(self, op1, op2):
        #! need to handle floats
        self.b.append('idiv')
        self._arithmeticOps(op1, op2)

    #!
    def remainder(self, op1, op2):
        self.b.append('rem')
        self._arithmeticOps(op1, op2)

    def inc(self, op1, op2):
        self.b.append('inc')
        self._operandToRegOrAddress(op1)
        self.b.append('\n')

    def dec(self, op1, op2):
        self.b.append('dec')
        self._operandToRegOrAddress(op1)
        self.b.append('\n')


    def shiftLeft(self, op1, op2):
        self.b.append('srl')
        self._printOps(op1, op2)

    def shiftRight(self, op1, op2):
        self.b.append('srr')
        self._printOps(op1, op2)

    def bOr(self, op1, op2):
        self.b.append('or')
        self._printOps(op1, op2)

    def bAnd(self, op1, op2):
        self.b.append('and')
        self._printOps(op1, op2)

    def bNot(self, op1, op2):
        self.b.append('not')
        self._printOps(op1, op2)

    def bXor(self, op1, op2):
        self.b.append('xor')
        self._printOps(op1, op2)

    def unconditionalJump(self, op1, op2):
        self.b.append('unconditionalJump')
        self._printOps(op1, op2)

    def unconditionalLongJump(self, op1, op2):
        self.b.append('unconditionalLongJump')
        self._printOps(op1, op2)

    def indexedJump(self, op1, op2):
        self.b.append('indexedJump')
        self._printOps(op1, op2)

    def jumpOnComparisonSuccess(self, op1, op2):
        self.b.append('jumpOnComparisonSuccess')
        self._printOps(op1, op2)

    def cmp(self, op1, op2):
        self.b.append('cmp')
        self._printOps(op1, op2)

    def call(self, op1, op2):
        self.b.append('call')
        self._printOps(op1, op2)

    def callReturn(self, op1, op2):
        self.b.append('callReturn')
        self._printOps(op1, op2)
