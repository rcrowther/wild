import unittest

from tokens import *
from wildio import *
#from Source import Source

from wildio import spliceCodeIterator

class TestIO(unittest.TestCase):
    '''
    python3 -m unittest wildio.IOTest
    '''
    def setUp(self):
      self.srcPath = "/home/rob/Desktop/wild/test/test.wild"

    def test_source(self):
      '''
      python3 -m unittest wildio.IOTest.TestIO.test_source
      '''
      srcPath = "/home/rob/Desktop/wild/test/test.wild"
      src = Source(srcPath)
      print(src.pathAsString() + ':')
      print(src.get())

    def test_string_iter(self):
      s = Source(self.srcPath)
      it = StringIterator(s, s.get())
      print(it.source.pathAsString() + ':')
      for c in it:
        print(chr(c), end='')

    def test_token_iter(self):
      '''
      python3 -m unittest wildio.IOTest.TestIO.test_token_iter
      '''
      s = Source(self.srcPath)
      tokenIt = s.tokenIterator()
      print(tokenIt.source().pathAsString() + ':')
      print(tokenIt.toString())


    def test_splicecode_iter(self):
      '''
      python3 -m unittest wildio.IOTest.TestIO.test_splicecode_iter
      '''
      s = Source('/home/rob/Desktop/wild/test/splicecode.wild')
      it = StringIterator(s, s.get())

      tokenIt = spliceCodeIterator.SpliceLexIterator(it)
      print(tokenIt.source().pathAsString() + ':')
      print(tokenIt.toString())


if __name__ == '__main__':
    unittest.main()
