

from trees.Trees import *
from trees.TreeTraverser import CallbackTraverser, CallbackUpdater
import SymbolTables

from enumerations import FuncRenderType


#def intern(tree, reporter):

    #reporter.error("renderTwig: Unrecognised class name: '{0}'".format(type(tree).__name__))

#? need to intern paths
class Intern(CallbackTraverser):
    def __init__(self, tree, expSymbolTable, reporter):
      self.expSymbolTable = expSymbolTable
      self.reporter = reporter
      #print('intern tree' +  tree.toString())
      CallbackTraverser.__init__(self, tree)

    def comment(self, tree):
      #print('comment found!')
      pass

    def constant(self, tree):
      #print('constant: ' + tree.data)
      pass

    def mark(self, tree):
      #print('mark: ' + tree.data)
      pass

    def definingExpression(self, tree):
      #print('defining expression: ' + tree.defMark.data)
      try:
        #! need to do path too
        mark = tree.defMark
        if (mark.isNotEmpty()):
            self.expSymbolTable.define(tree.defMark.identifier)
      except SymbolTables.DuplicateDefinitionException:
        self.reporter.error('duplicate expression definition in scope of symbol mark: {0}'.format(tree.defMark.identifier), tree.position)

    def expression(self, tree):
      #print('expression: ' + tree.actionMark.data)
      self.expSymbolTable.add(tree.actionMark.identifier)

    def definingExpressionWithBody(self, tree):
      #print('defining expression with body: ' + tree.defMark.data)
      try:
        self.expSymbolTable.define(tree.defMark.identifier)
      except SymbolTables.DuplicateDefinitionException:
        self.reporter.error('duplicate expression with body definition in scope of symbol mark: {0}'.format(tree.defMark.identifier), tree.position)

    def expressionWithBody(self, tree):
      #print('expression with body: ' + tree.actionMark.data)
      self.expSymbolTable.add(tree.actionMark.identifier)



normalizedSymbols = {
'+' : '$$plus$',
'-' : '$$minus$',
'*' : '$$mult$',
'%' : '$$divide$',
# TODO: Allow underscore, but what about initial underscore?
# use '$$$' in place?
'_' : '_',
# NB: allow dot 
'.' : '.'
}

#! messy
class MarkNormalize(CallbackTraverser):
    def __init__(self, tree, reporter):
      self.reporter = reporter
      CallbackTraverser.__init__(self, tree)

    def _isAlphaNumeric(self, c):
        return (
          # alphabetic
          (c >= 65 and c <= 90) 
          or (c >= 97 and c <= 122) 
          # numeric
          or (c >= 48 and c <= 57)
          #? or c == UNDERSCORE
          )

    def _normalizeMarkText(self, mark):
      nMark = ''
      failed = False
      for cp in mark:
        if (self._isAlphaNumeric(ord(cp))):
          nMark += cp
        else:
          try:
            nMark += normalizedSymbols[cp]
          except Exception:
            self.reporter.error('Unable to normalize mark: {0}: unrecognised symbol: {1}'.format(mark, cp))
            failed = True
            break
      return mark if failed else nMark
      
    def _normalizeMark(self, tree, mark):
       strippedMark = mark
       lastChar = mark[-1:]
       if (lastChar == '!' or lastChar == '?'):
         tree.isMutable = lastChar == '!'
         strippedMark = mark[0:-1]
       return self._normalizeMarkText(strippedMark)

    def comment(self, tree):
      #print('comment found!')
      pass

    def constant(self, tree):
      #print('constant: ' + tree.data)
      pass

    def mark(self, tree):
      #print('mark: ' + tree.data)
      pass

    def definingExpression(self, tree):
      #print('defining expression: ' + tree.defMark.data)
        #tree.defMark.data = self._normalizeMark(tree, tree.defMark.identifier)
        normalizedMark = self._normalizeMark(tree, tree.defMark.identifier)
        tree.defMark = tree.defMark.replaceIdentifier(normalizedMark)


    def expression(self, tree):
      #print('expression: ' + tree.actionMark.data)
        #tree.actionMark.data = self._normalizeMark(tree, tree.actionMark.identifier)
        normalizedMark = self._normalizeMark(tree, tree.actionMark.identifier)
        tree.actionMark = tree.actionMark.replaceIdentifier(normalizedMark)


    def definingExpressionWithBody(self, tree):
      #print('defining expression with body: ' + tree.defMark.data)
        #tree.defMark.data = self._normalizeMark(tree, tree.defMark.identifier)
        normalizedMark = self._normalizeMark(tree, tree.defMark.identifier)
        tree.defMark = tree.defMark.replaceIdentifier(normalizedMark)


    def expressionWithBody(self, tree):
        #print('expression with body: ' + tree.actionMark.data)
        #tree.actionMark.data = self._normalizeMark(tree, tree.actionMark.identifier)
        normalizedMark = self._normalizeMark(tree, tree.actionMark.identifier)
        tree.actionMark = tree.actionMark.replaceIdentifier(normalizedMark)




from trees.Trees import Constant, Mark


class UnaryMinus(CallbackUpdater):
    '''
    Crush plus/minus sign expression-wrapped Constant 
    to Constant with signed numeric content 
    '''
    def __init__(self, tree, reporter):
      self.reporter = reporter
      #print('intern tree' +  tree.toString())
      CallbackUpdater.__init__(self, tree)

    '''
    def definingExpression(self, parent, tree):
      #print('defining expression: ' + tree.defMark.data)
      if (
      tree.defMark.data == '$$minus$'
      tree.defMark.data == '$$plus$' 
      and len(tree.children) == 1
      and isinstance(tree.children[0], Constant)
      ):
        sign = '-' if (tree.actionMark.data == '$$minus$') else ''
        tree.children[0].data = sign + tree.children[0].data
        print('found unary minus def!')
        parent.update(tree, tree.children[0])
    '''
    def expression(self, parent, tree):
      #print('expression: ' + tree.actionMark.data)
      if (
      (tree.actionMark.identifier == '$$minus$' or tree.actionMark.identifier == '$$plus$')
      and len(tree.children) == 1
      and isinstance(tree.children[0], Constant)
      ):
        sign = '-' if (tree.actionMark.identifier == '$$minus$') else ''
        tree.children[0].data = sign + tree.children[0].data  
        #print('found unary minus!')
        #print(parent.toString())
        #print(tree.children[0].toString())
        parent.updateChild(tree, tree.children[0])

mCodeFunctions = [
    '$$plus$',
    '$$minus$',
    '$$mult$',
    '$$divide$'
    ]


class FunctionCategorize(CallbackTraverser):
    '''
    '''
    def __init__(self, mCodeContext, tree, reporter):
      self.reporter = reporter
      self.mCodeContext = mCodeContext
      #print('intern tree' +  tree.toString())
      CallbackTraverser.__init__(self, tree)
      
    '''
    def definingExpression(self, parent, tree):
      #print('defining expression: ' + tree.defMark.data)
      if (
      tree.defMark.data == '$$minus$'
      tree.defMark.data == '$$plus$' 
      and len(tree.children) == 1
      and isinstance(tree.children[0], Constant)
      ):
        sign = '-' if (tree.actionMark.data == '$$minus$') else ''
        tree.children[0].data = sign + tree.children[0].data
        print('found unary minus def!')
        parent.update(tree, tree.children[0])
    '''
    def expression(self, tree):
      #print('expression: ' + tree.actionMark.data)
      #! should test type too, with 32/64bit...
      if (
      (tree.actionMark.identifier in mCodeFunctions)
      and len(tree.children) == 2
      ):
        tree.renderCategory = FuncRenderType.MCODE64
      #else:
       # tree.renderCategory = FuncRenderType.CALL



from collections import namedtuple


###############################################
import operator
    # Lord, this is tedious in Python

    # seems useful to do abstract registers
    # but what about param registers? Could they be a category
    # of likely-to-spill, so last?
#? Very untested. Especially spillage and freeArray reallocation
#! Doesn't answer preallocation issues
class RegisterAllocate():
    # for intervals
    NAME = 0
    FROM = 1
    TO = 2

    def __init__(self, intervalList, registers = ['reg1', 'reg2', 'reg3', 'reg4']):
      # [[regName, isAvailable]]
      self.freeRegisters = []
      for reg in registers:
          self.freeRegisters.append([reg, True])
      # [isAvailable]
      self.freeArray = []
      for i in range(64):
          self.freeArray.append(True)
      # always sorted by increasing end point
      # 
      self.active = []

      # create tuples and drop dead ranges
      # from name -> instruction number,  start, end
      # to [(name, from, to)]
      filteredIntervals = []
      for k, v in intervalList.items():
           if (v[0] and v[1]):
               filteredIntervals.append([k, v[0], v[1]])

      # sort by increasing start point
      self.sortedIntervals = sorted(filteredIntervals, key=lambda iv : iv[RegisterAllocate.FROM]) 
      # the result
      # ivName -> regName
      self.allocated = {}

      self.registerAllocation(len(registers))

    ## Helper ##

    #!
    def getFreeArray(self):
         freeIdx = self.freeArray.index(True)
         # mark idx as in use
         self.freeArray[freeIdx] = False 
         return 'freeArray' + str(freeIdx)

    def getFreeRegister(self):
         reg = ''
         for e in self.freeRegisters:
             if (e[1]):
                 e[1] = False
                 reg = e[0]
                 break
         #freeReg = next(e for e in self.freeRegisters if e[1])
         # mark register as in use
         # set tuple list to False...
         #self.freeRegisters[freeReg[0]] = False 
         #return freeReg[0]
         return reg

    def freeRegisterOrArray(self, ivName):
         regName = self.allocated[ivName]
         if (regName[0:8] != 'freeArray'):
             # register
             for e in self.freeRegisters:
                 if (e[0] == regName):
                     e[1] = True
                     break
         else:
            # freeArray
            idx = int(regName[8:-1])
            self.freeRegisters[idx] = True
              
                 
    def addActive(self, iv):
        # add i to active, sorted by increasing end point
        self.active.append(iv)
        self.active = sorted(self.active, key = operator.itemgetter(RegisterAllocate.TO))


    def isPreAllocatedInterval(self, iv):
        return iv

    ## Main ##
    def result(self):
        return self.allocated

    def registerAllocation(self, regCount):
      for iv in self.sortedIntervals:
          self.expireOldIntervals(iv[RegisterAllocate.FROM])
          if (len(self.active) == regCount):
            self.spillAtInterval(iv)
          else:
            #register[i] ← a register removed from pool of free registers
            self.allocated[iv[RegisterAllocate.NAME]] = self.getFreeRegister()
            # add i to active, sorted by increasing end point
            self.addActive(iv)

    def expireOldIntervals(self, start):
         dead = []
         for iv in self.active:
             if (iv[TO] < start):
                 ivName = iv[RegisterAllocate.NAME]
                 dead.append(ivName)
                 # mark register as free
                 #self.freeRegisters[name] = True
                 self.freeRegisterOrArray(ivName)
         #  from active, remove the intervals
         self.active = [e for e in self.active if (not(e[RegisterAllocate.NAME] in dead))]

    def spillAtInterval(self, iv):
        lastActive = self.active[-1]
        if (lastActive[TO] > iv[TO]):
            #register[i] ← register[lastActive]
            #location[lastActive] ← new stack location
            self.allocated[lastActive[RegisterAllocate.NAME]] = self.getFreeArray()
            #remove spill from active
            self.removeActive(lastActive)
            # allocate
            self.allocated[iv[RegisterAllocate.NAME]] = self.getFreeRegister()
            #add iv to active, sorted by increasing end point
            self.addActive(iv)
        else:
            #location[iv] ← new stack location
            self.allocated[iv[RegisterAllocate.NAME]] = self.getFreeArray()

    def addString(self, b):
        first = True
        for k, v in self.allocated.items():
            if first:
                first = False
            else:
                b.append(', ')                
            b.append(k)
            b.append('->')
            b.append(v)
        return b

    def toString(self):
        b = []
        b.append('RegisterAllocate(')
        self.addString(b)
        b.append(')')
        return ''.join(b) 


