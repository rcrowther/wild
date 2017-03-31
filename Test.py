import unittest

#from tokens import *
from SymbolTables import kindSymbolTable, expressionActionSymbolTable
#from Kinds import *
import SymbolTables
import wildio.Source
import reporters.ConsoleStreamReporter
import TokenSyntaxer
import ArchitectureRegisterContext


class Test(unittest.TestCase):
    '''
    python3 -m unittest Test
    '''
    def setUp(self):
      srcPath = "/home/rob/Desktop/wild/test/test.wild"
      self.src = wildio.Source.Source(srcPath)
      self.tokenIt = self.src.tokenIterator()
      self.reporter = reporters.ConsoleStreamReporter.ConsoleStreamReporter()

    def test_syntax(self):
      '''
      python3 -m unittest Test.Test.test_syntax
      '''
      p = TokenSyntaxer.TokenSyntaxer(self.tokenIt, self.reporter)
      print('tree:')
      #print(p.ast().toFrameString())
      print(p.ast().toPrettyString())


    def test_symbol_tables(self):
      '''
      python3 -m unittest Test.Test.test_symbol_tables
      '''
      print(kindSymbolTable.toString())
      #print(expressionActionSymbolTable.toString())
      expressionActionSymbolTable.add('bloom')
      expressionActionSymbolTable.define('bloom')
      self.assertIs(expressionActionSymbolTable.exists('bloom'), True)
      print(expressionActionSymbolTable.toString())
      #expressionActionSymbolTable.define('bloom')
      self.assertRaises(
        SymbolTables.DuplicateDefinitionException,
        expressionActionSymbolTable.define, 
        'bloom'
        )
     #     print('Duplicate define() raises error')

   #def test_phaselist(self):
      #pl = PhaseList()
      #assert(pl.size() == 3)
      #pl1 = pl.take('intern')
      #assert(pl1.size() == 2)
      #print(pl.phaseDataToString())

    def test_arch(self):
      '''
      python3 -m unittest Test.Test.test_arch
      '''
      ac = ArchitectureRegisterContext.X64ArchitectureRegisterContext()

      print(str(ac))
      print('getGeneralRegister:')
      for i in range(ac.generalIdxsSize + 3):
          #idx = ac.getGeneralRegister(i)
          print(ac.generalRegisterToString(i))

      print('getCallRegister:')
      for i in range(ac.callConventionIdxsSize + 3):
          #idx = ac.getGeneralRegister(i)
          print(ac.callRegisterToString(i))

      print('call register take:')
      registers = ac.callRegisterTake(ac.callConventionIdxsSize + 3)
      for i in registers:
          print(ac.registerToString(i))

      print('single locations:')
      print('  abstract:' + ac.registerToString(ac.ABSTRACT))
      print('  return:' + ac.registerToString(ac.RETURN))
      print('  float return:' + ac.registerToString(ac.FLOAT_RETURN))
      print('  stack pointer:' + ac.registerToString(ac.STACK_POINTER))
      #print(p.ast().toPrettyString())
