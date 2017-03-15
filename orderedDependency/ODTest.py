import unittest

from orderedDependency.GraphOrderable import *


class TestOD(unittest.TestCase):
    '''
    python3 -m unittest orderedDependency.ODTest.TestOD.test
    '''
    def setUp(self):
      self.ogs = [
      GraphOrderable('first', None, [], []),
      GraphOrderable('one', 'first', ['twoA'], ['four']),
      GraphOrderable('twoA', None, ['one'], []),
      GraphOrderable('twoB', 'twoA', [], []),
      GraphOrderable('three', None, ['twoA'], []),
      GraphOrderable('four', 'three', [], ['oddity']),
      GraphOrderable('five', 'four', ['three'], [])
      ]

    def test(self):
      '''
      python3 -m unittest orderedDependency.ODTest.TestOD.test
      '''
      #dg = graphOrderableToGraph(self.ogs)
      order(self.ogs, 'first')

    def test_orderable(self):
      '''
      python3 -m unittest orderedDependency.ODTest.TestOD.test_orderable
      '''
      print(str(self.ogs[2]))

    def test_methods(self):
      '''
      python3 -m unittest orderedDependency.ODTest.TestOD.test_methods
      '''
      dg = DependencyGraph()
      dg.getUpdateNode('liar')
      print(''.join(dg.compilerPhaseList()))
      #print(self.ctx.registerNames)

