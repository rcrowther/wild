

from trees.Trees import *
from trees.TreeTraverser import CallbackTraverser, CallbackUpdater
import SymbolTables

from enumerations import FuncRenderType


#def intern(tree, reporter):

    #reporter.error("renderTwig: Unrecognised class name: '{0}'".format(type(tree).__name__))

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
        self.expSymbolTable.define(tree.defMark.data)
      except SymbolTables.DuplicateDefinitionException:
        self.reporter.error('duplicate expression definition in scope of symbol mark: {0}'.format(tree.defMark.data), tree.position)

    def expression(self, tree):
      #print('expression: ' + tree.actionMark.data)
      self.expSymbolTable.add(tree.actionMark.data)

    def definingExpressionWithBody(self, tree):
      #print('defining expression with body: ' + tree.defMark.data)
      try:
        self.expSymbolTable.define(tree.defMark.data)
      except SymbolTables.DuplicateDefinitionException:
        self.reporter.error('duplicate expression with body definition in scope of symbol mark: {0}'.format(tree.defMark.data), tree.position)

    def expressionWithBody(self, tree):
      #print('expression with body: ' + tree.actionMark.data)
      self.expSymbolTable.add(tree.actionMark.data)



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


class MarkNormalize(CallbackTraverser):
    def __init__(self, tree, reporter):
      self.reporter = reporter
      #print('intern tree' +  tree.toString())
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
        tree.defMark.data = self._normalizeMark(tree, tree.defMark.data)


    def expression(self, tree):
      #print('expression: ' + tree.actionMark.data)
        tree.actionMark.data = self._normalizeMark(tree, tree.actionMark.data)

    def definingExpressionWithBody(self, tree):
      #print('defining expression with body: ' + tree.defMark.data)
        tree.defMark.data = self._normalizeMark(tree, tree.defMark.data)

    def expressionWithBody(self, tree):
        #print('expression with body: ' + tree.actionMark.data)
        tree.actionMark.data = self._normalizeMark(tree, tree.actionMark.data)



# TODO: A class is surely way too heavy.
# A global func could do this...
# unless we get to multithreading?
# TODO: is triple '$' a good idea?
class UnparsedNameGenerator():
    def __init__(self):
      self._unparsedNameCounter = 0

    def reset(self):
      self._unparsedNameCounter = 0

    def unparsedName(self):
      self._unparsedNameCounter += 1
      return '$tmp' + str(self._unparsedNameCounter)

class FuncUnnest(CallbackTraverser):
    '''
    From
    { func1(fun2())}
    {tmp = func2() func1(tmp)}
    {} = a body (otherwise this extraction creates another parameter!)
    '''
    def __init__(self, tree):
      #print('intern tree' +  tree.toString())
      self.nameGenerator = UnparsedNameGenerator()
      CallbackTraverser.__init__(self, tree)

    def _unNest(self, tree):
       # walk this body
       #print('unest ' + tree.toString())
       elems = tree.body
       for e in elems:
         self.nameGenerator.reset()
         if (e.isNonAtomicExpression):
           # look at children (parameters), for expressions in this expression
           for subchild in e.children:
             if (
               subchild.isNonAtomicExpression
               and subchild.renderCategory == FuncRenderType.CALL
             ):
               # TODO: Not elegant here
               #print('nested func: ' + subchild.actionMark.data)
               newName = self.nameGenerator.unparsedName()
               # replace the expression with a mark
               e.updateChild(subchild, Mark(newName))
               # create a definition for the mark
               newMarkDef = ExpressionWithBody('val') 
               newMarkDef.setDefMark(newName)
               newMarkDef.appendBody(subchild)
               # Insert the new definition,
               # placed before the original function
               tree.insertBodyChildBefore(e, newMarkDef)

    #def definingExpression(self, tree):
    #  self._unNest(tree)

    #def expression(self, tree):
    #  print('expression: ' + tree.actionMark.data)
    #  self._unNest(tree)

    def definingExpressionWithBody(self, tree):
      self._unNest(tree)

    def expressionWithBody(self, tree):
      self._unNest(tree)
