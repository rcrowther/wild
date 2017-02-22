import unittest

#from tokens import *
from SymbolTables import kindSymbolTable, expressionActionSymbolTable
#from Kinds import *
import SymbolTables

class Test(unittest.TestCase):
    '''
    python3 -m unittest Test
    '''
    def setUp(self):
      pass

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
