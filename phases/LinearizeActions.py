

from collections import namedtuple

from trees.TreeTraverser import CallbackTraverser
from trees.Trees import Constant, Mark, Expression, ExpressionWithBody, PathedIdentifier

from enumerations import FuncRenderType
from codeGen.architectureContext import ABSTRACT


'''
= Rules of unnesting
1 must consider three nests at once, asthe children of an expression are moved to the parent.

2 The only parent to be considered is a body expression/seq, because only these can contain unnested expressions

The contents of the body are tested one by one. 

1 Some contents can be ignored: these are Comments (if present), and raw Constants. Inclusive statement: to be a candidate for unnesting the content must be a non-atomic expressioon.

2 A non-atomic expression may also not need to be unnested if already classified as a machine-code-ready expression (though these are unlikely to stand alone).

Now an expression is targetted for unnesting. 
1 a new-name delivery node replaces the original node. The expression to unnest is wrapped in a new val node, as supply, and placed in the parent (but see next section). 
1 only the params/children are unested, not body contents
2 all active code params/children are unnested, even Constants, as they will need register/stack placement

The supply nodes are broken up in a similar way, recursively

= Registers
Since these unnests are known full calls, not machine calls or label-constants, the registers allocated to the supply nodes are known (from the calling convention).

Does this account for jiggery pokery with registers e.g. getting an expression result into a specified register? No, but we know the target.

# Recursion
This is a special recursion, through body elements and across their children. So it may as well be custom, especially as parent body elements are heavily modified by adding in lists of supply expressions.
'''
##? is this later, as in register setting,
# or earlier, as in a a source code unnesting?
# because one uses the name generator, one uses the
# the architectureContext---
class FuncUnnest():
    '''
    From
    { func1(func2())}
    ==
    {tmp = func2() func1(tmp)}
    {} = a body (otherwise this extraction creates another parameter!)
    '''
    def __init__(self, tree, newNames, architectureContext):
      #print('intern tree' +  tree.toString())
      #self.nameGenerator = UnparsedNameGenerator()
      self.newNames = newNames
      self.architectureContext = architectureContext
      #CallbackTraverser.__init__(self, tree)
      #self._dispatch(tree)
      if (isinstance(tree, ExpressionWithBody)):
         self._unNestBody(tree)
      else:
         print('Trying to unnest but no body found!')

    def newVal(self, name, register, value):
        syntheticSupply = ExpressionWithBody(PathedIdentifier([], 'val'))
        syntheticSupply.defMark = PathedIdentifier([], name)
        syntheticSupply.appendBody(value)
        syntheticSupply.register = register
        syntheticSupply.isDefinitionFromCompiler = True
        return syntheticSupply

    def  _unnestSupply(self, targetName, register, tree):
       supply = []
       #! are all calls nonAtomic?
       if (
         tree.isNonAtomicExpression
         and tree.renderCategory == FuncRenderType.CALL
         and (not tree.isDefinitionFromCompiler)
       ):
         tree.isDefinitionFromCompiler = True 
         for idx, child in enumerate(tree.children):
           newName = self.newNames.get()
           # replace the expression with a synthetic expression
           syntheticDelivery = Expression(PathedIdentifier([],newName))
           syntheticDelivery.isDefinitionFromCompiler = True
           syntheticDelivery.register = ABSTRACT
           tree.children[idx] = syntheticDelivery
           supplyRegister = self.architectureContext.getCallRegister(idx)
           supply.extend(self._unnestSupply(newName, supplyRegister, child))

       supply.append(self.newVal(targetName, register, tree))
       return supply

    def _unNestBody(self, tree):
       '''
       Must be provided with a body expression
       '''
       # walk this body
       # builder for new parent body
       b = []
       #print('unest ' + tree.toString())
       for e in tree.body:
         #self.newNames.reset()
         #? this needs building, so def are not revisited recursively, and funcs can be raised before vals for X64.
         # is it an Expression/ExpressionWithBody?
         #! Comment is classified as CALL?
         if (
         e.isNonAtomicExpression
         and tree.renderCategory == FuncRenderType.CALL
         and (not e.isDefinitionFromCompiler)
         ):
           # look at children (parameters),
           # for expressions in this expression
           # no target name for the starting expression,
           # so this is a primer for the recursion
           for idx, child in enumerate(e.children):
             newName = self.newNames.get()
             # replace the expression with a synthetic expression
             syntheticDelivery = Expression(PathedIdentifier([],newName))
             syntheticDelivery.isDefinitionFromCompiler = True
             syntheticDelivery.register = ABSTRACT
             e.children[idx] = syntheticDelivery
             # create a definition for the new assignment
             # make this to the known register
             register = self.architectureContext.getCallRegister(idx)
             syntheticSupply = self._unnestSupply(newName, register, child)
             b.extend(syntheticSupply)
           # e overall is now generator modified
           e.isDefinitionFromCompiler = True 
           # Now, if a body expression, recuse in.
           # Won't damage tree as we are reading in front/down
           # from later changes
           if (isinstance(e, ExpressionWithBody)):
               self._unNestBody(e)
         # now any generated assignments in place, 
         # append the (modified) original
         b.append(e)
       # put the new body in place
       tree.body = b




LiveRange = namedtuple('LiveRange', 'frm to')

INSTRUCTION_NUMBER = 0
FROM = 1
TO = 2

#? Problem:
#? The difference between expressions for calling functions (unwanted)
#? and expressions for calling vars (wanted)
#? Also:
#? need to mark vars used to supply functions---these may be
#? pre-allocated (x64) registers
class ParseLiveRanges(CallbackTraverser):
    def __init__(self, tree, reporter):
      self.reporter = reporter
      #print('intern tree' +  tree.toString())
      #? Instruction number is deprecated
      # name -> instructionNumber,  start, end
      self.b = {}
      self.expressionCount = 0
      CallbackTraverser.__init__(self, tree)

    def result(self):
        return self.b

    def _append(self, name):
      '''
      For definitions
      '''
      self.b[name] = [None, self.expressionCount, None]

    def _update(self, nane):
      '''
      For appearances/usages to read. 
      '''
      self.b [nane][TO] = self.expressionCount

    def _merge(self, name, instructionNumber, idx):
      if (name in self.b):
        self.b[name][TO] = idx
      else:
        self.b[name] = ['???', idx, 0]


    #def comment(self, tree):
      #print('comment found!')
      #pass

    #def constant(self, tree):
      #print('constant: ' + tree.data)
      #pass

    #def mark(self, tree):
      #print('mark: ' + tree.data)
      #pass

    def _nonDefiningExpression(self, tree):
      if (tree.actionMark.identifier == 'val' or tree.actionMark.identifier == 'var'):
          self._append(tree.defMark.identifier)
      else:
          # if the expression actionmark already defined,
          # then its a straight val/var
          #! this is a rubbish test?
          if (tree.actionMark.identifier in self.b):
              self._update(tree.actionMark.identifier)

          # function call
          for param in tree.children:
              if isinstance(param, Mark):
                  self._update(param.identifier)
      self.expressionCount += 1

    def _definingExpression(self, tree):
      if (tree.actionMark.identifier == 'val' or tree.actionMark.identifier == 'var'):
          #print('LL?: ' + tree.toString())
          self._append(tree.defMark.identifier)
      elif (tree.actionMark == 'func'):
          # parameter definitions, track them
          for param in tree.children:
              self._append(param.identifier)
      self.expressionCount += 1

    def definingExpression(self, tree):
      #print('defining expression: ' + tree.defMark.data)
      self._definingExpression(tree)
      self.expressionCount += 1

    def expression(self, tree):
      #print('expression: ' + tree.actionMark.data)
      self._nonDefiningExpression(tree)
      self.expressionCount += 1

    def definingExpressionWithBody(self, tree):
      '''
      val/var, func definitions
      '''
      #print('defining expression with body: ' + tree.defMark.data)
      self._definingExpression(tree)
      self.expressionCount += 1           
            

    def expressionWithBody(self, tree):
      #print('expression with body: ' + tree.actionMark.data)
      self._nonDefiningExpression(tree)

    def addString(self, b):
        first = True
        for k, v in self.b.items():
            if first:
                first = False
            else:
                b.append(', "')                
            b.append(k)
            b.append('"->[')
            b.append(str(v[FROM]))
            b.append(', ')
            b.append(str(v[TO]))
            b.append(']')
        return b

    def toString(self):
        b = []
        b.append('LiveRanges(')
        self.addString(b)
        b.append(')')
        return ''.join(b) 
