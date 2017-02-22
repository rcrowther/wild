import unittest

#from genCode import MCodeContext

#import genCode
from codeGen.architectureContext import ArchitectureContext, X64ArchitectureContext
from codeGen.CodeGenContext import X64CodeGenContext
from codeGen import spliceCode, spliceCodeParse, spliceCodeTraverser
from trees import *

from wildio import Source
from wildio import spliceCodeIterator, StringIterator
from reporters import ConsoleStreamReporter

class TestSplicecode(unittest.TestCase):
    '''
    python3 -m unittest wildio.IOTest
    '''
    def setUp(self):
      self.ctx = X64ArchitectureContext()
      self.cgCtx = X64CodeGenContext()
      self.splicecodeArray = [
3, 'dji', 'dead',
3, 'funcWithParams', 'dead',
3, 'funky', 'dead',
3, 'printstr', 'dead',
1, 'zee', '-3.142',
2, 'zii', '4',
10, '0', '76',
30, '0', '9',
12, '0', '83',
100, 'dji', 'dead',
14, '1', 'dead',
10, '0', '2',
32, '0', '3',
12, '2', '0', 
100, 'funcWithParams', 'dead',
13, '[zii]', '6',
100, 'funky', 'dead',
14, '0', 'dead',
100, 'printstr', 'dead'
      ]

    def test_codearray_print(self):
      '''
      python3 -m unittest codeGen.SplicecodeTest.TestSplicecode.test_codearray_print
      '''
      ts = spliceCodeTraverser.ToString(self.splicecodeArray)
      print(ts.toString())

    def test_codearray_to_asm(self):
      '''
      python3 -m unittest codeGen.SplicecodeTest.TestSplicecode.test_codearray_to_asm
      '''
      conv = spliceCodeTraverser.toASMCode(
      X64ArchitectureContext(), 
      self.splicecodeArray
      )
      conv.result()
      print(conv.result())
