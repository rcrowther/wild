#!/usr/bin/python3


from trees import *
from reporters import *
from Settings import Settings
from SyntaxPhase import SyntaxPhase
from codeGen.CodeGenPhase import CodeGenPhase
import codeGen.architectureContext
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

    def contains(self, phaseName):
        for p in self.phases:
          if (p.name == phaseName):
            return True
        return False

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
        self.architectureContext = codeGenContext.architectureContext
        self.reporter = reporter
        # init
        self.phases = PhaseList(self._internalPhases())

    def _internalPhases(self):
       return [
       SyntaxPhase(self.reporter, self.settings),
       phases.TreePhases.RemoveCommentsPhase(self.reporter),
       phases.TreePhases.MarkNormalizePhase(self.reporter, self.settings),
       phases.TreePhases.SplitValuesPhase(self.reporter),
       phases.InternPhase(self.expSymbolTable, self.reporter, self.settings),
       #phases.TreePhases.UnaryMinusPhase(self.reporter, self.settings),
       #? This can't go here. Point of fact, it must go as
       # processing on the final file, as the CodeGenPhase needs
       # to see operators etc.? (what about FunctionCategorizePhase?)
       #phases.NASMPreprocessPhase(self.reporter, self.settings),
       phases.LinearizePhases.FunctionCategorizePhase(self.codeGenContext, self.reporter, self.settings),
       phases.LinearizePhases.RenderCategorizePropagatePhase(self.codeGenContext, self.reporter, self.settings),
       phases.LinearizePhases.FunctionUnnestPhase(self.architectureContext),
       phases.LinearizePhases.ParseLiveRangesPhase(self.reporter),
       phases.LinearizePhases.ChooseRegistersPhase(self.architectureContext, self.reporter),
       phases.LinearizePhases.ToSplicecode(self.reporter)

       #CodeGenPhase(self.reporter, self.codeGenContext, self.settings)
       ]


    def _reportPhase(self, item, phaseName):
      if (phaseName):
        self.reporter.info("{0}: phase: '{1}'".format(item, phaseName))
      else:
        self.reporter.info("{0}:".format(item))

    #? Better to quit without run, if data requested, in what circumstance?
    # - no path? But not XOtree, tree, ranges, phase marks, tables...
    def run(self, compilationUnit):
       # If output tokens, print and quit
       if (self.settings.getValue('XOtokens')):
         self.reporter.info('Tokens:\n' + compilationUnit.source.tokenIterator().toPrettyString())
         sys.exit(0)

       # If setting data output, print and quit
       if (self.settings.getValue('XOsettings')):
           self.reporter.info('Settings:\n' + self.settings.toPrettyString())
           sys.exit(0)

       # If phase data output, print and quit
       if (self.settings.getValue('XOphases')): 
         self.reporter.info('Phases:\n' + self.phases.phaseDataToString())
         sys.exit(0)

       endPhaseName = self.settings.getValue('XCtoPhase')
       phaseList = self.phases
       if (endPhaseName):
          # limit phase list
          if(not self.phases.contains(endPhaseName)):
              self.reporter.warning("Phase name not in list:phase name: '{0}'\nIgnoring XCtoPhase limit".format(endPhaseName))
          else:
              phaseList = self.phases.take(endPhaseName)

       endPhaseName = endPhaseName if (endPhaseName) else 'all'


       #!
       #if (self.settings.getValue('XOphases')):
       #  self.reporter.info('Phases:\n' + phaseList.phaseDataToString())
       #  sys.exit(0)

       for p in phaseList:
         if (self.settings.getValue('XCphases')):
            self.reporter.info("phase: '{0}'".format(p.name))
         p.run(compilationUnit)
         if (self.reporter.hasErrors()):
             break 

       #? May be better done by sending print signals
       #? to the phase, then halting right there?
       # if symbol table output requested
       if (self.settings.getValue('XOexpressionSymbolTable')):
           self._reportPhase('expression symbol table', endPhaseName)
           self.reporter.info('Table:\n' + self.expSymbolTable.toPrettyString())

       if (self.settings.getValue('XOkindSymbolTable')):
           self._reportPhase('kind symbol table', endPhaseName)
           self.reporter.info('Table:\n' + self.kindSymbolTable.toPrettyString())

       # if tree output requested
       if (self.settings.getValue('XOtree')):
           #print('XOtree' + str(self.settings.getValue('XOtree')))
           self._reportPhase('tree', endPhaseName)
           self.reporter.info('Tree:\n' + compilationUnit.tree.toPrettyString())

       if (self.settings.getValue('XOliveRanges')):
           #print('XOtree' + str(self.settings.getValue('XOtree')))
           self._reportPhase('tree', endPhaseName)
           self.reporter.info('Live Ranges:\n' + str(compilationUnit.liveRanges))

       #! otherwise?
       # report errors
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


