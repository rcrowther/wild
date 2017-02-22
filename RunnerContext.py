#!/usr/bin/python3


from trees import *
from reporters import *
from Settings import Settings
from SyntaxPhase import SyntaxPhase
from codeGen.CodeGenPhase import CodeGenPhase

import phases
from SymbolTables import *
import collections
import sys
import wildio


class PhaseList():
    def __init__(self, args):
        self.phases = args
        self.idx = 0

    def __iter__(self):
      return self
       
    def __next__(self):
        if self.idx > (self.size() - 1):
            raise StopIteration
        else:
            self.idx += 1
            return self.phases[self.idx - 1] 
    '''
    def _createPhaseData(self):
        phaseData = collections.OrderedDict()
        for p in self.phases:
          phaseData[p.name] = p.description
        return phaseData
    '''
    def add(self, phase):
        self.phases.append(phase)

    def size(self):
       return len(self.phases)

    def indexOf(self, phaseName):
        i = 0
        broke = False 
        for p in self.phases:
          if p.name == phaseName:
             broke = True
             break
          else:
             i += 1
        return i if broke else -1

    def take(self, phaseName):
        xl = []
        for p in self.phases:
          xl.append(p)
          if (p.name == phaseName):
            break
        return PhaseList(xl)

    def phaseDataToString(self):
        b = []
        for p in self.phases:
            b.append(p.name)
            b.append(': ')
            b.append(p.description)
            b.append("\n")
        return ''.join(b)

# as Global
class RunnerContext:
    def __init__(self, reporter, codeGenContext, settings = None):
        self.expSymbolTable = expressionActionSymbolTable
        self.expSymbolTable.clear()
        self.kindSymbolTable = kindSymbolTable
        self.kindSymbolTable.clear()
        self.settings = Settings() if not settings else settings
        self.codeGenContext = codeGenContext 
        self.reporter = reporter
        # init
        self.phases = PhaseList(self._internalPhases())

    def _internalPhases(self):
       return [
       SyntaxPhase(self.reporter, self.settings),
       phases.MarkNormalizePhase(self.reporter, self.settings),
       phases.InternPhase(self.expSymbolTable, self.reporter, self.settings),
       phases.UnaryMinusPhase(self.reporter, self.settings),
       #? This can't go here. Point of fact, it must go as
       # processing on the final file, as the CodeGenPhase needs
       # to see operators etc.? (what about FunctionCategorizePhase?)
       #phases.NASMPreprocessPhase(self.reporter, self.settings),
       phases.FunctionCategorizePhase(self.codeGenContext, self.reporter, self.settings),
       phases.FunctionUnnestPhase(),
       CodeGenPhase(self.reporter, self.codeGenContext, self.settings)
       ]


    def _reportPhase(self, item, phaseName):
      if (phaseName):
        self.reporter.info("{0}: phase: '{1}'".format(item, phaseName))
      else:
        self.reporter.info("{0}:".format(item))

    # e.g.?
    def run(self, compilationUnit):
       # If output tokens, print and quit
       if (self.settings.getValue('XOtokens')):
         # TODO: reduce to only the token iterator, remove imports
         s = compilationUnit.source
         it = wildio.StringIterator(s, s.get())
         tokenIt = wildio.TokenIterator(it)
         self.reporter.info(tokenIt.toString())
         sys.exit(0)

       # If setting data output, print and quit
       if (self.settings.getValue('XOsettings')):
         self.reporter.info(self.settings.toString())
         sys.exit(0)

       endPhaseName = self.settings.getValue('XCphaseStop')
       if (endPhaseName):
          # limit phase list
          phaseList = self.phases.take(endPhaseName) 
       else:
          phaseList = self.phases

       # If phase data output, print and quit
       if (self.settings.getValue('XOphases')):
         self.reporter.info(phaseList.phaseDataToString())
         sys.exit(0)

       for p in phaseList:
         if (self.settings.getValue('XCphases')):
            self.reporter.info("phase: '{0}'".format(p.name))
         p.run(compilationUnit)
         if (self.reporter.hasErrors()):
             break 

       # if symbol table output requested
       if (self.settings.getValue('XOexpressionSymbolTable')):
           self._reportPhase('expression symbol table', endPhaseName)
           self.reporter.info(self.expSymbolTable.toString())

       if (self.settings.getValue('XOkindSymbolTable')):
           self._reportPhase('kind symbol table', endPhaseName)
           self.reporter.info(self.kindSymbolTable.toString())

       # if tree output requested
       if (self.settings.getValue('XOtree')):
           self._reportPhase('tree', endPhaseName)
           self.reporter.info(compilationUnit.tree.toPrettyString())

       # otherwise, report errors
       if (self.reporter.hasErrors()):
             print('errors...')
             print(self.reporter.summaryString())
             # print errors/extent of errors?
             #sys.exit("Error message")
       else:
             #print('out:')
             #print("".join(compilationUnit.mCode))

             print('done')
             # How do we write output?




from codeGen.CodeGenContext import X64CodeGenContext

## test
srcPath = "/home/rob/Desktop/wild/test/test.wild"

from wildio.Source import Source
from CompilationUnit import *
from reporters.ConsoleStreamReporter import ConsoleStreamReporter


s = Source(srcPath)
cu = CompilationUnit(s)
rpt = ConsoleStreamReporter()

ctx = RunnerContext(rpt, X64CodeGenContext())
#print('phaseData:')
#print(ctx.phaseDataToString())
ctx.run(cu)
