import unittest

import RunnerContext
from codeGen.CodeGenContext import X64CodeGenContext

from wildio.Source import Source
from CompilationUnit import *
from reporters.ConsoleStreamReporter import ConsoleStreamReporter
from Settings import Settings

class TestRun(unittest.TestCase):
    '''
    python3 -m unittest TestRun
    '''
    def setUp(self):
      srcPath = "/home/rob/Desktop/wild/test/test.wild"

      self.src = Source(srcPath)
      self.cu = CompilationUnit(self.src)



    def test_run(self):
      '''
      python3 -m unittest TestRun.TestRun.test_run
      '''
      rpt = ConsoleStreamReporter()
      ctx = RunnerContext.RunnerContext(rpt, X64CodeGenContext())
      ctx.run(self.cu)

    def test_tokens(self):
      '''
      python3 -m unittest TestRun.TestRun.test_tokens
      '''
      print(self.src.tokenIterator().toString())

    def test_tree(self):
      '''
      python3 -m unittest TestRun.TestRun.test_run
      '''
      settings = Settings()
      settings.setValue('XOtree', True)
      rpt = ConsoleStreamReporter()
      ctx = RunnerContext.RunnerContext(rpt, X64CodeGenContext(), settings)
      ctx.run(self.cu)

    def test_phases(self):
      '''
      python3 -m unittest TestRun.TestRun.test_phases
      '''
      settings = Settings()
      settings.setValue('XOphases', True)
      rpt = ConsoleStreamReporter()
      ctx = RunnerContext.RunnerContext(rpt, X64CodeGenContext(), settings)
      ctx.run(self.cu)

