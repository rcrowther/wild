import unittest

from orderedDependency.orderedDependency import *


class TestOD(unittest.TestCase):
    '''
    python3 -m unittest orderedDependency.ODTest.TestOD.test
    '''
    def setUp(self):
      self.ogs = [
      BasicGraphOrderable('first', None, [], []),
      BasicGraphOrderable('one', 'first', ['twoA'], ['four']),
      BasicGraphOrderable('twoA', None, ['one'], []),
      BasicGraphOrderable('twoB', 'twoA', [], []),
      BasicGraphOrderable('three', None, ['twoA'], []),
      BasicGraphOrderable('four', 'three', [], ['oddity']),
      BasicGraphOrderable('five', 'four', ['three'], [])
      ]

    def test(self):
      '''
      python3 -m unittest orderedDependency.ODTest.TestOD.test
      '''
      #dg = graphOrderableToGraph(self.ogs)
      order(self.ogs, 'first')

    def test_methods(self):
      '''
      python3 -m unittest orderedDependency.ODTest.TestOD.test_methods
      '''
      dg = DependencyGraph()
      dg.getUpdateNode('liar')
      print(''.join(dg.compilerPhaseList()))
      #print(self.ctx.registerNames)

