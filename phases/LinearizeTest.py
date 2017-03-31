import unittest


from reporters import ConsoleStreamReporter
import phases.LinearizeActions

class LinearizeTest(unittest.TestCase):
    '''
    python3 -m unittest phases.LinearizeTest
    '''
    def setUp(self):
      self.reporter = ConsoleStreamReporter.ConsoleStreamReporter()
      self.testRangesOrig = {"$2$":[27, 31], "zii":[17, None], "$1$":[7, 11], "zmap":[19, None], "zstr":[21, None], "zee":[15, 29]}

      self.noninterfereRanges = { "$1$":[7, 8], "$2$":[9, 21], "$3$":[32, 34]}
      self.overlapRanges = { "$1$":[7, 11], "$2$":[8, 13], "$3$":[9, 21]}

      #self.overlapRanges = { "$1$":[7, 11], "$2$":[12, 21], "$3$":[14, 19]}

      self.spillRanges = {"$1$":[7, 27], "$2$":[8, 28], "$3$":[9, 28], "$4$":[10, 30], "$5$":[11, 31], "$6$":[12, 32], "$7$":[13, 33]}

    def test_ranges(self):
      '''
      python3 -m unittest phases.LinearizeTest.LinearizeTest.test_ranges
      '''
      #p = phases.TreeActions.ParseLiveRanges(tree, self.reporter)
      #print(p.toString())
      pass

      #ranges = p.result()

    def test_reg_realloc(self):
      '''
      python3 -m unittest phases.LinearizeTest.LinearizeTest.test_reg_overlap
      '''
      alloc = phases.LinearizeActions.ChooseRegisters(self.noninterfereRanges)
      print(str(alloc))

    def test_reg_overlap(self):
      '''
      python3 -m unittest phases.LinearizeTest.LinearizeTest.test_reg_overlap
      '''
      alloc = phases.LinearizeActions.ChooseRegisters(self.overlapRanges, registers)
      print(str(alloc))

    def test_reg_spill(self):
      '''
      python3 -m unittest phases.LinearizeTest.LinearizeTest.test_reg_spill
      '''
      alloc = phases.LinearizeActions.ChooseRegisters(self.spillRanges)
      print(str(alloc))
