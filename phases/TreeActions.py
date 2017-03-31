

from trees.Trees import *
from trees.TreeTraverser import CallbackTraverser
import SymbolTables

#! use CallbackBodyBuilder
class RemoveComments(CallbackTraverser):
    def __init__(self, tree, reporter):
      self.reporter = reporter
      CallbackTraverser.__init__(self, tree)


    def _removeComments(self, tree):
      newBody = [t for t in tree.body if (not isinstance(t, Comment))]
      tree.body = newBody

    def definingExpressionWithBody(self, tree):
      '''
      '''
      #print('defining expression with body: ' + tree.defMark.data)
      # funcs/dynamic allocated var/val
      self._removeComments(tree)


    def expressionWithBody(self, tree):
      #print('expression with body: ' + tree.actionMark.data)
      # expressionWithBody is definitions 
      #' but will in future be branch calls like case/if
      self._removeComments(tree)


#! use CallbackBodyBuilder
class SplitVals(CallbackTraverser):
    '''
    Split the compound val statement into defenitions and assignments.

      Expression(val, zee, kind, funcRender.CALL, None, children: Constant(3.1))
     becomes,
      Expression(val, zee, kind, funcRender.DEF, None, children: ())
      Expression('$equ$', zee, kind, funcRender.CALL, None, children: Constant(3.1))
    '''
    def __init__(self, tree, reporter):
      self.reporter = reporter
      CallbackTraverser.__init__(self, tree)

    def _splitVals(self, bodyList):
        b = []
        for t in bodyList:
          # insert the element back
          b.append(t)
          if (
             t.isNonAtomicExpression
             and t.actionMark.identifier == 'val'
            ):
            # build a new assignment
            syntheticDelivery = Expression(noPathIdentifierFunc('$$assign$'))
            syntheticDelivery.defMark = t.defMark
            syntheticDelivery.children = t.children

            # reduce t to a definition 
            # (asserting, should be true?) 
            t.isDef = True    
            t.children = []

            # insert syntheticDelivery as 
            # initialising assignment after tree
            b.append(syntheticDelivery)
        return b

    def definingExpressionWithBody(self, tree):
        tree.body = self._splitVals(tree.body)

    def expressionWithBody(self, tree):
        tree.body = self._splitVals(tree.body)







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
'=' : '$$assign$',
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




#from trees.Trees import Constant, Mark

#x deprecated due to revision in tokeniser


#from collections import namedtuple



