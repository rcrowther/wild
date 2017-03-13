import unittest

from tokens import *
from wildio import *
#from Source import Source

import newNames

class TestTools(unittest.TestCase):
    '''
    python3 -m unittest TestTools
    '''
    def setUp(self):
      self.newName = newNames.NewName()
      pass

    def test_newnames(self):
      '''
      python3 -m unittest TestTools.TestTools.test_newnames
      '''
      n = self.newName.get()
      print(n)
      n = self.newName.get()
      print(n)
      n = self.newName.get()
      print(n)
      pn = self.newName.getPrefixed('widget[int]')
      print(pn)
      pn = self.newName.getPrefixed('widget[int]')
      print(pn)
      pn = self.newName.getPrefixed('widget[int]')
      print(pn)
