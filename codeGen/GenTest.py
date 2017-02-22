import unittest

#from genCode import MCodeContext

#import genCode
from codeGen.architectureContext import ArchitectureContext, X64ArchitectureContext
from codeGen.CodeGenContext import X64CodeGenContext
from codeGen import spliceCode, spliceCodeParse
from trees import *

from wildio import Source
from wildio import spliceCodeIterator, StringIterator
from reporters import ConsoleStreamReporter

class TestGen(unittest.TestCase):
    '''
    python3 -m unittest wildio.IOTest
    '''
    def setUp(self):
      self.ctx = X64ArchitectureContext()
      self.cgCtx = X64CodeGenContext()
      te = Expression('$$divide$')
      t3 = FloatConstant('3.14')
      t4 = IntegerConstant('9')
      te.appendChild(t3)
      te.appendChild(t4)

      self.testTree = te

      te = Expression('+')
      t3 = FloatConstant('3.14')
      t4 = IntegerConstant('9')
      te.appendChild(t3)
      te.appendChild(t4)

      self.testTree2 = te

    def test_context(self):
      '''
      python3 -m unittest codeGen.GenTest.TestGen.test_context
      '''
      print(self.ctx.registerNames)
      print(self.ctx.registerToString(0))
      print(self.ctx.registerToString(3))

    def test_codegen_context_slots(self):
      '''
      python3 -m unittest codeGen.GenTest.TestGen.test_codegen_context_slots
      '''
      b = []
      print('\nallocateToParam:')
      for i in range(10):
        self.cgCtx.allocateToParam(b, IntegerConstant('5'))
      print(''.join(b))

      b = []
      self.cgCtx.resetParamSlots()
      for i in range(10):
        self.cgCtx.allocateToParam(b, Mark('5'))
      print(''.join(b))

      b = []
      print('\nallocateSlot:')
      for i in range(10):
        self.cgCtx.allocateSlot(b, '3')
      print(''.join(b))


      b = []
      print('\ndeallocateSlot:')
      for i in range(10):
        self.cgCtx.deallocateSlot(b, 'rax')
      print(''.join(b))

    def test_codegen_context_functions(self):
      '''
      python3 -m unittest codeGen.GenTest.TestGen.test_codegen_context_functions
      '''
      b = []
      print('\nmcode func:')
      self.cgCtx.functionCall(b, self.testTree)
      print(''.join(b))

      b = []
      print('\ncustom func:')
      self.cgCtx.functionCall(b, self.testTree2)
      print(''.join(b))

    def test_splicecode_tokens(self):
      '''
      python3 -m unittest codeGen.GenTest.TestGen.test_splicecode_tokens
      '''
      assert(spliceCode.codeToName[spliceCode.nameToCode['add']] == 'add')
      spliceCodeTest =[10, 4.3, 6, 50, 'print']
      print(spliceCode.toString(spliceCodeTest))

    def test_splicecode_itr(self):
      '''
      python3 -m unittest codeGen.GenTest.TestGen.test_splicecode_parse
      '''
      src = Source('/home/rob/Desktop/wild/test/splicecode.wild')
      it = StringIterator(src, src.get())
      tokenItr = spliceCodeIterator.SpliceLexIterator(it)
      print(tokenItr.toString())

    def test_splicecode_parse(self):
      '''
      python3 -m unittest codeGen.GenTest.TestGen.test_splicecode_parse
      '''
      src = Source('/home/rob/Desktop/wild/test/splicecode.wild')
      it = StringIterator(src, src.get())
      tokenItr = spliceCodeIterator.SpliceLexIterator(it)
      reporter = ConsoleStreamReporter.ConsoleStreamReporter()
      spliceCodeParse.SpliceCodeParse(tokenItr, reporter)
      #o = spliceCodeParse.parse(src)
      #print(o)

    def test_splicecode_tostring(self):
      '''
      python3 -m unittest codeGen.GenTest.TestGen.test_splicecode_tostring
      '''
      ct = spliceCodeTraverser.ToString(testSC)
      print(ct.toString())
