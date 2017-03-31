

from collections import namedtuple

from trees.TreeTraverser import CallbackTraverser, CallbackBodyBuilder
from trees.Trees import Constant, Mark, Expression, ExpressionWithBody, PathedIdentifier

#from enumerations import FuncRenderType, MachineRenderKind
from enumerations import MachineRenderKind
from codeGen.architectureContext import ABSTRACT
from util.codeUtils import StdPrint


################################################################
mCodeNumericFunctions = [
    '$$plus$',
    '$$minus$',
    '$$mult$',
    '$$divide$'
    #'$$assign$'
    ]


#? surely this needs some architecture data, for the methods and categories? 
class FunctionCategorize(CallbackTraverser):
    '''
    Categorises expressions to machine code if they are method calls
    (functions, not value calls) and contain two children.
    As an additional check, the method call identifier must match a
    list of known translatable method calls (simple translatable calls
    such as shift or divide).
    Note that the phase expresses no opinion on if the expression
    is in a state or positioned where it may be translated into
    a machine code method. For example, the expression may contain
    subexpressions. The classification says only that the data in the
    expression is suitable. 
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
    #! must cover assign children too... or is that all children?
    #? but I think it do?
    def constant(self, tree):
      # (tree.tpe == ConstantKind.integerNum and tree.data < machinemax and tree.data > machinemin
      tree.isMachine = True
      #if (tree.tpe == ConstantKind.string and ???)


    def expression(self, tree):
      #print('expression: ' + tree.actionMark.data)
      #! should test type too, with 32/64bit...
      # should be set by now?
      #tree.isFunc = tree.actionMark.isFunc
      if (
      tree.isFunc
      and (tree.actionMark.identifier in mCodeNumericFunctions)
      #and kind.bounds < platform.maxNum
      ):
        tree.isMachine = True
        tree.machineKind = MachineRenderKind.num64bit

      if (
      tree.isData
      #and kind.bounds < platform.maxNum
      ):
        tree.isMachine = True

#####################################################
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
    Unnest parameters recursively.
    This also allocates registers where they are known i.e. for
    code function calls.
    Parameter unnesting is not the full job of translating a tree to
    node -> machine code correspondence. For example, the returns from function calls must be allocated to variables. This may need an allocation inserting.
    However, this is a big step forward.
    '''
    '''
    def __init__(self, tree, newNames, architectureContext):
      print('unnest!!!')
      assert(isinstance(tree, ExpressionWithBody))              
      assert(tree.actionMark.identifier == 'TREE_ROOT')
      #self.nameGenerator = UnparsedNameGenerator()
      self.newNames = newNames
      self.architectureContext = architectureContext
      #CallbackTraverser.__init__(self, tree)
      #self._dispatch(tree)
      for t in tree.body:
         self._unNestBody(t)

    def newVal(self, name, register, value):
        syntheticSupply = ExpressionWithBody(noPathIdentifierFunc('val'))
        syntheticSupply.defMark = noPathIdentifierValue(name)
        syntheticSupply.isDef = True
        syntheticSupply.appendBody(value)
        syntheticSupply.register = register
        
        syntheticSupply.isDefinitionFromCompiler = True
        return syntheticSupply

    def  _unnestSupply(self, targetName, register, tree):
       supply = []
       #! are all calls nonAtomic?
       if(tree.renderCategory == FuncRenderType.CALL):
         print('la: ' + tree.actionMark.identifier)
       if (
         tree.isNonAtomicExpression
         #and tree.renderCategory == FuncRenderType.CALL
         and tree.isFunc
         #? a defense, for now
         and (not tree.isDefinitionFromCompiler)
       ):
         tree.isDefinitionFromCompiler = True 
         for idx, child in enumerate(tree.children):
           newName = self.newNames.get()
           # replace the expression with a synthetic expression
           syntheticDelivery = Expression(noPathIdentifierValue(newName))
           syntheticDelivery.isDefinitionFromCompiler = True
           syntheticDelivery.register = ABSTRACT
           tree.children[idx] = syntheticDelivery
           supplyRegister = self.architectureContext.getCallRegister(idx)
           supply.extend(self._unnestSupply(newName, supplyRegister, child))

       supply.append(self.newVal(targetName, register, tree))
       return supply

    def _unNestBody(self, tree):
       ##
       Must be provided with an expression
       tree a tree with a body
       #
       assert(
       isinstance(tree, Expression)
       or isinstance(tree, ExpressionWithBody)
       )
       # walk this body
       # builder for new parent body
       b = []
       #print('unest !!!')
       for e in tree.body:
         #self.newNames.reset()
         #? this needs building, so def are not revisited recursively, and funcs can be raised before vals for X64.
         # is it an Expression/ExpressionWithBody?
         #! Comment is classified as CALL?
         # unnest for all calls (non-def).
         # - if not machine call, unnest everything (inc. constants)
         # they need to be in set registers, maybe, or stacked.
         # - if machine call, unnest everything except constants
         # Constants can be written directly. How about machine variables?
         #! below is a bodge, as 'assign' should be a machine call 
         #print('look at:' + str(e.isNonAtomicExpression))
         if (
         e.isNonAtomicExpression
         and e.renderCategory == FuncRenderType.CALL
         #and (not e.isDefinitionFromCompiler)
         #? Defence for constants not to be unnested. I present, a mess. 
         and not (e.actionMark.identifier == '$$assign$' and isinstance(e.children[0], Constant))
         ):
           #print('look at children:' + str(e.actionMark.identifier))
           # look at children (parameters),
           # for expressions in this expression
           # no target name for the starting expression,
           # so this is a primer for the recursion
           for idx, child in enumerate(e.children):
             newName = self.newNames.get()
             # replace the expression with a synthetic expression
             syntheticDelivery = Expression(noPathIdentifierValue(newName))
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
    '''
###########################################################

#CallbackBodyBuilder
class FuncUnnest2(CallbackBodyBuilder):
    '''
    From
    { func1(func2())}
    ==
    {tmp = func2() func1(tmp)}
    {} = a body (otherwise this extraction creates another parameter!)
    '''
    def __init__(self, tree, newNames, architectureContext):
      print('unnest2!!!')
      assert(isinstance(tree, ExpressionWithBody))              
      assert(tree.actionMark.identifier == 'TREE_ROOT')
      #self.nameGenerator = UnparsedNameGenerator()
      self.newNames = newNames
      self.architectureContext = architectureContext
      #CallbackTraverser.__init__(self, tree)
      #self._dispatch(tree)
      CallbackBodyBuilder.__init__(self, tree)
    '''
    def addValCall(self, b, name, register=None):
        exp = Expression(noPathIdentifierValue(name))
        exp.isDefinitionFromCompiler = True
        b.append(exp)

    #? used elsewhere?
    def addValAndDef(self, b, name, register, value):
        defExp = Expression(noPathIdentifierFunc('val'))
        defExp.defMark = noPathIdentifierValue(name)
        defExp.isDef = True
        defExp.isDefinitionFromCompiler = True
        b.append(defExp)

        #syntheticSupply.appendBody(value)
        assignExp = Expression(noPathIdentifierFunc('$$assign$'))
        assignExp.defMark = noPathIdentifierValue(name)
        assignExp.children.append(value)
        assignExp.register = register
        assignExp.isDefinitionFromCompiler = True
        b.append(assignExp)
    '''
    def addExpressionAssign(self, b, toName, fromExp, register = None):
        '''
        register if unknown, can be empty
        '''
        e = Expression(noPathIdentifierFunc('$$assign$'))
        e.defMark = noPathIdentifierFunc(toName)
        e.children.append(fromExp)
        e.register = register
        e.isDefinitionFromCompiler = True
        b.append(e)
    '''
    def addDataCallAssign(self, b, toName, fromName, register = None):
        ##
        register if unknown, can be empty
        #
        e = Expression(noPathIdentifierFunc('$$assign$'))
        e.defMark = noPathIdentifierFunc(toName)
        e.children.append(Mark(fromName))
        e.register = register
        e.isDefinitionFromCompiler = True
        b.append(e)
    '''
    '''
    def addCodeFuncCallAssign(self, b, toName, funcCallTree, register):
        ##
        Writes a dual action, call and assign
        
        zee(15)
        becomes
        zee
        $x$ = funcReturnRegister
        parameters should have been unnested before this function

        register if unknown, can be empty
        #
        assert(funcCallTree.identifier.isFunc)
        assert(funcCallTree.renderCategory == FuncRenderType.CALL)
        funcCallTree.isDefinitionFromCompiler = True
        b.append(funcCallTree)
        # Now handle the return, moving the data to the given name/register
        # if the given register eq self.architectureContext.returnRegister,
        # don't assign, it is placed
        if (register != self.architectureContext.returnRegister):
            self.addExpressionAssign(b, toName, self.architectureContext.returnRegister, register)
    '''
    '''
    def addMachineFuncCallAssign(self, b, toName, machineCallTree, register):
        ##
        A machine call is still assigned, so the registers can be simply tracked. But it will render as one instruction, so the tree can be nested, not split then assigned. Also, the register is unassigned, so can be set to whatever is given.

        These would be untouched,
        plus(1 3)
        plus(zee 9)

        This,
        plus(zee(), 18)
        should, before this call, have become
        plus($x$, 18)
        
        register if unknown, can be empty
        #
        assert(machineCallTree.actionMark.isFunc)
        assert(machineCallTree.renderCategory == FuncRenderType.MCODE64 
        or machineCallTree.renderCategory == FuncRenderType.MCODE32)
        self.addExpressionAssign(b, toName, machineCallTree, register)
    '''

    def assignTree(self, b, tree, toName, register=None):
        if (isinstance(tree, Constant)):
          self.addExpressionAssign(b, toName, tree, register)
        elif (not tree.actionMark.isFunc):
          #self.addDataCallAssign(b, toName, tree.actionMark, register = None)
          self.addExpressionAssign(b, toName, tree, register)
          pass
        else:
          self.addExpressionAssign(b, toName, tree, register)
    

    def _unnestCodeCallParams(self, b, exp):
      '''
      Code call parameters 
         - everything is unnested
         - are replaced with Marks
      '''
      for idx, child in enumerate(exp.children):
          #!
          newName = self.newNames.get()
          supplyRegister = self.architectureContext.getCallRegister(idx)
          #! unnest the exp
          #! this puts the child back on the tree?
          #! the assign should do that....
          self._dispatchUnnest(b, child)
          # insert an assignment for the new name
          self.assignTree(b, child, newName, supplyRegister)
          # replace each parameter with a mark
          exp.children[idx] = Mark(newName)
          exp.children[idx].isDefinitionFromCompiler = True

    def _unnestMachineCallParam(self, b, exp, childIdx):
      newName = self.newNames.get()
      child = exp.children[childIdx]
      #! unnest the exp
      #! this puts the child back on the tree?
      self._dispatchUnnest(b, child)
      # insert an assignment for the new name
      self.assignTree(b, child, newName)
      # replace chosen parameters with an expression
      exp.children[childIdx] = Expression(noPathIdentifierFunc(newName)) 
      exp.children[childIdx].isDefinitionFromCompiler = True

    def _unnestMachineCallParams(self, b, exp):
      '''
      Machine call parameters
         - The first must be unnested. Following (could only be one) is unnested if not machine-rendered const, or data. 
         - first is replaced with a Mark (it is not rendered, but split). Othersm if replacwsm are replaced with expressions
      '''
      child = exp.children[0]
      newName = self.newNames.get()
      # recursively unnest the exp
      self._dispatchUnnest(b, child)
      # insert an assignment for the new name
      self.assignTree(b, child, newName)
      # replace this param with a Mark
      exp.children[0] = Mark(newName)
      if (len(exp.children) > 1):
        child = exp.children[1]
        #! if child is not machine
        if(
          #child.renderCategory == FuncRenderType.CALL
          #and child.actionMark.isFunc 
          child.isFunc 
        ):
          newName = self.newNames.get()
          child = exp.children[1]
          # unnest the exp 
          self._dispatchUnnest(b, child)
          # insert an assignment for the new name
          self.assignTree(b, child, newName)
          # replace chosen parameters with an expression
          exp.children[1] = Expression(noPathIdentifierFunc(newName)) 
          exp.children[1].isDefinitionFromCompiler = True

    def _dispatchUnnest(self, b, exp):
      #! assert(exp.isCall)
      #assert(exp.isData)
      #assert(exp.isConstant)
      #assert(exp.isMachine)

      if (
        exp.isNonAtomicExpression 
        and not exp.isDef
      ):
        print('dispatch: ' + exp.actionMark.identifier)
        if (
        #exp.renderCategory == FuncRenderType.CALL
        exp.isFunc
        ):
          if(not exp.isMachine):
            self._unnestCodeCallParams(b, exp)
          else:
            self._unnestMachineCallParams(b, exp)



    def child(self, b, tree):
        '''
      Just params. Don't deal in detail. 
      - Don't try to rewrite function calls so the return is allocated to
      a register
      However, 
      Code call parameters 
         - everything is unnested
         - are replaced with Marks
      Machine call parameters
         - first parameter always unnested 
         - following machine rendering constants and code calls (non-func - labels), are ignored. These do not need register assignment.
         - are replaced with Expressions

        '''
        #! no recursion
        #! what about data and constants?
        #! data now split into def and assignments?
        #! assignment generators not covered?

        self._dispatchUnnest(b, tree)
        # modified or not, put the tree back  
        b.append(tree)


###########################################################
#? should be from..to (but they are Python keywords)
class LiveRange(namedtuple('LiveRange', 'start end')):
        def __str__(self):
           return '[{0}{1}]'.format(self.start, self.end)

INSTRUCTION_NUMBER = 0
FROM = 1
TO = 2

#? Problem:
#? The difference between expressions for calling functions (unwanted)
#? and expressions for calling vars (wanted)
#? Also:
#? need to mark vars used to supply functions---these may be
#? pre-allocated (x64) registers
class ParseLiveRanges(CallbackTraverser, StdPrint):
    def __init__(self, tree, reporter):
      StdPrint.__init__(self, 'LiveRanges')
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
      #self.b[name] = [None, self.expressionCount, None]
      self.b[name] = LiveRange(self.expressionCount, None)

    def _update(self, nane):
      '''
      For appearances/usages to read. 
      '''
      #self.b [nane][TO] = self.expressionCount
      self.b[nane] = self.b[nane]._replace(end = self.expressionCount)

    #def _merge(self, name, instructionNumber, idx):
    #  if (name in self.b):
    #    self.b[name][TO] = idx
    #  else:
    #    self.b[name] = ['???', idx, 0]


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

    def addStringWithSeparator(self, b, sep):
        first = True
        for k, v in self.b.items():
            b.append("'")                
            if first:
                first = False
            else:
                b.append(', ')                
            b.append(k)
            b.append('"->[')
            b.append(str(v))
            b.append(']')
        return b




###############################################
import operator
    # Lord, this is tedious in Python

    # seems useful to do abstract registers
    # but what about param registers? Could they be a category
    # of likely-to-spill, so last?
#? Very untested. Especially spillage and freeArray reallocation
#! Doesn't answer preallocation issues
class ChooseRegisters():
    # for NameToIntervalTuples
    NAME = 0
    FROM = 1
    TO = 2

    def __init__(self, intervalList, architectureRegisters = ['reg1', 'reg2', 'reg3', 'reg4']):
      '''
      '''
      # [[regName, isAvailable], ...]
      self.freeRegisters = []
      for reg in architectureRegisters:
          self.freeRegisters.append([reg, True])
      # [isAvailable]
      self.freeArray = []
      for i in range(64):
          self.freeArray.append(True)
      # intervals, always sorted by increasing end point
      self.active = []

      # create tuples and drop dead ranges
      # from {name -> (start, end), ...}
      # to [(name, from, to), ...]
      filteredIntervals = []
      for k, v in intervalList.items():
           if (v[0] and v[1]):
               filteredIntervals.append([k, v[0], v[1]])
      #print(str(filteredIntervals))
      # sort by increasing start point
      self.sortedIntervals = sorted(filteredIntervals, key=lambda iv : iv[ChooseRegisters.FROM]) 
      # the result
      # ivName -> regName
      self.allocated = {}

      self.registerAllocation(len(architectureRegisters))

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
        # add interval to active, sorted by increasing end point
        self.active.append(iv)
        self.active = sorted(self.active, key = operator.itemgetter(ChooseRegisters.TO))

    def isPreAllocatedInterval(self, iv):
        return iv

    ## Main ##
    def result(self):
        '''
        '''
        return self.allocated

    def registerAllocation(self, regCount):
      for iv in self.sortedIntervals:
          self.expireOldIntervals(iv[ChooseRegisters.FROM])
          if (len(self.active) == regCount):
            self.spillAtInterval(iv)
          else:
            #register[i] ← a register removed from pool of free registers
            self.allocated[iv[ChooseRegisters.NAME]] = self.getFreeRegister()
            # add interval to active, sorted by increasing end point
            self.addActive(iv)

    def expireOldIntervals(self, start):
         dead = []
         for iv in self.active:
             if (iv[TO] < start):
                 ivName = iv[ChooseRegisters.NAME]
                 dead.append(ivName)
                 # mark register as free
                 #self.freeRegisters[name] = True
                 self.freeRegisterOrArray(ivName)
         #  from active, remove the intervals
         self.active = [e for e in self.active if (not(e[ChooseRegisters.NAME] in dead))]

    def spillAtInterval(self, iv):
        lastActive = self.active[-1]
        if (lastActive[TO] > iv[TO]):
            #register[i] ← register[lastActive]
            #location[lastActive] ← new stack location
            self.allocated[lastActive[ChooseRegisters.NAME]] = self.getFreeArray()
            #remove spill from active
            self.removeActive(lastActive)
            # allocate
            self.allocated[iv[ChooseRegisters.NAME]] = self.getFreeRegister()
            #add iv to active, sorted by increasing end point
            self.addActive(iv)
        else:
            #location[iv] ← new stack location
            self.allocated[iv[ChooseRegisters.NAME]] = self.getFreeArray()

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

    def __str__(self):
        b = []
        b.append('ChooseRegisters(')
        self.addString(b)
        b.append(')')
        return ''.join(b) 



###########################################
class ApplyRegistersToTree(CallbackTraverser):
    '''
    
    '''
    def __init__(self, tree, registerMap, reporter):
      # {varname -> regname}
      self.registerMap = registerMap
      self.reporter = reporter
      #print('intern tree' +  tree.toString())
      CallbackTraverser.__init__(self, tree)


    def definingExpression(self, tree):
      #print('defining expression: ' + tree.defMark.data)
      id = tree.defMark.identifier
      reg = self.registerMap.get(id)
      if (reg):
         tree.register = reg

    def expression(self, tree):
      #print('expression: ' + tree.actionMark.data)
      id = tree.actionMark.identifier
      reg = self.registerMap.get(id)
      if (reg):
         tree.register = reg

    def definingExpressionWithBody(self, tree):
      '''
      val/var, func definitions
      '''
      #print('defining expression with body: ' + tree.defMark.data)
      id = tree.defMark.identifier
      reg = self.registerMap.get(id)
      if (reg):
         tree.register = reg         
            

    def expressionWithBody(self, tree):
      #print('expression with body: ' + tree.actionMark.data)
      id = tree.actionMark.identifier
      reg = self.registerMap.get(id)
      if (reg):
         tree.register = reg


############################################

#? pre-allocated (x64) registers
class PrecleanForSplicecode(CallbackTraverser):
    def __init__(self, tree, reporter):
      self.reporter = reporter
      CallbackTraverser.__init__(self, tree)


    def _removeComments(self, tree):
      newBody = [t for t in tree.body if (not isinstance(t, Comment))]
      tree.body = newBody


    def comment(self, tree):
       pass
        
    def constant(self, tree):
       pass

    def definingExpression(self, tree):
      #print('defining expression: ' + tree.defMark.data)
      # some vals/vars?
      pass


    def expression(self, tree):
      #print('expression: ' + tree.actionMark.data)
      # func calls and some var/vals
      pass



    def definingExpressionWithBody(self, tree):
      '''
      '''
      #print('defining expression with body: ' + tree.defMark.data)
      #FuncRenderType.CALL
      # funcs/dynamic allocated var/val
      pass


    def expressionWithBody(self, tree):
      #print('expression with body: ' + tree.actionMark.data)
      # expressionWithBody is definitions 
      #' but will in future be branch calls like case/if
      pass

############################################
from codeGen.Templates import tmpl, stock_tmpl
from trees.Trees import *

#! do deal with redundancy in the tree, this needs to be a homemade parser.
#! list: call parameter marks, constant usage, comments?
#! homemade because newlines not clear also?
#? or should we run a tree cleanup phase?
#!
#! clean tree phase
#! no handling of package or scope
#! make this phase self recursing, check aginst ???
#! sort out constants
#! consider the ways of expressing vals/vars
#! add NASM conversion and wrap
class TreeToSplicecode():
    '''
    
    '''
    machineOps = {
'$$plus$' : 'add',
'$$minus$' :'sub',
'$$mult$' :'mult',
'$$divide$' :'div',
'$$inc$' :'inc',
'$$dec$' :'dec'
#'shift left'
#'$$assign$' : ''
# etc.
    }

    def __init__(self, tree, reporter):
      # {varname -> regname}
      self.reporter = reporter
      self.b = []
      #print('to soliceCode' +  str(tree))
      self._dispatch(tree) 


    def result(self):
      return ''.join(self.b)

    def _newLine(self):
       self.b.append('\n')

    def _space(self):
        self.b.append(' ')

    # partial constant application
    def _constant(self, tree):
      #print('constant: ' + tree.data)
        if (tree.tpe == ConstantKind.string):
            self.b.append('"')
            self.b.append(tree.data)
            self.b.append('"')
        else:
            self.b.append(tree.data)


    def newLineConstant(self, tree):
         self._constant(tree)
         self._newLine()

    def definingExpression(self, tree):
        #print('defining expression: ' + tree.defMark.identifier)
        # defining static vals/vars?
        if(
          tree.actionMark.identifier != 'val'
          and tree.actionMark.identifier != 'import'
        ):
              self.b.append('definingExpression: not a val or import? label:')
              self.b.append(tree.defMark.identifier)
              self._newLine()
        #if(tree.actionMark.identifier == 'import'):
        #      self.b.append('declExtenalFunc ')
              #self.b.append('..some target')
        #      self.b.append(tree.defMark.identifier)
        #      self._newLine()
        if(tree.actionMark.identifier == 'val'):
              #if(tree.isDefinitionFromCompiler):
               #   self.b.append('toReg ')
               #   self.b.append(str(tree.register))
               #   self._space()
                  #self.b.append(tree.defMark.identifier)
               #   self.b.append('..some contents')
               #   self._newLine()
              #else:
                  #self.b.append(tree.actionMark.identifier)
                  self.b.append('allocSpace ')
                  #! should never be empty, so need str()?
                  self.b.append(tree.defMark.identifier)
                  self.b.append(',')
                  self.b.append('<size>')
                  self._newLine()
                  #self.b.append('toSpace ')
                  #self.b.append(tree.defMark.identifier)
                  #self.b.append(',')
                  #! afer unnesting, could only be this or a function
                  #self._noNewlineDispatch(tree.children[0])
                  #self._newLine()

    def _params(self, tree):
        #print(tree)
        assert len(tree.children) > 1
        self._noNewlineDispatch(tree.children[0])
        self.b.append(',')
        self._noNewlineDispatch(tree.children[1])
        #pass


    def expression(self, tree):
      #print('expression: ' + tree.actionMark.data)
      # calls...
      if (tree.actionMark.identifier == '$$assign$'):
                  self.b.append('toSpace ')
                  self.b.append(tree.defMark.identifier)
                  self.b.append(',')
                  #! afer unnesting, could only be this or a function
                  self._noNewlineDispatch(tree.children[0])
                  self._newLine()
      elif(tree.actionMark.identifier == 'import'):
              self.b.append('declExtenalFunc ')
              #self.b.append('..some target')
              self.b.append(tree.defMark.identifier)
              self._newLine()
      #elif(tree.renderCategory != FuncRenderType.CALL):
      elif(tree.isData and tree.isMachine):
          # machine data call
          opId = tree.actionMark.identifier
          machineOp = self.machineOps.get(opId)
          if (not machineOp):
              self.reporter.error('Expression marked as machine code, but has no registered operation: expression: {0}'.format(opId))
              #sys.exit(0)
          self.b.append(machineOp)
          self.b.append(' ')
          # now call params
          # guarenteed two params if classified as machine? 
          #! No, shift, assign
          #self.b.append(')')
          self._params(tree)
          self._newLine()
      else:
        if(tree.actionMark.isFunc):
            # code func call
            #! do better with identifier paths (depends on them validating?)
            self.b.append('call ')
            self.b.append(tree.actionMark.identifier)
            #self._params(tree) 
        else:
            # code data call
            self.b.append(tree.actionMark.identifier)
        self._newLine()    


    def definingExpressionWithBody(self, tree):
      '''
      '''
      #print('defining expression with body: ' + tree.defMark.identifier)
      #FuncRenderType.CALL
      # func defs, dynamic allocated var/val def
      if(tree.actionMark.identifier == 'fnc'):
          # func
          self.b.append('fnc ')
          self.b.append(tree.defMark.identifier)
          self._newLine()
          self.b.append('{')
          self._newLine()
          #self.b.append('various internal allocations')
          #self._newLine()
          #for c in tree.children:
              #self.b.append('allocSpace ')
              #self.b.append(c.defMark)
              #self._newLine()
          self.b.append('...and actions...')
          self._newLine()
          for c in tree.body:
              self._dispatch(c)
          self.b.append('return')
          self._newLine()
          self.b.append('}')
          self._newLine()
      elif(tree.actionMark.identifier == 'package'):
          self.b.append('namespace ')
          self.b.append(tree.defMark.identifier)
          #? re-enable
          self.b.append('{')
          self._newLine()    
          for c in tree.body:
              self._dispatch(c) 
          self.b.append('}')
      else:      
          # val/var
          #if(tree.actionMark.identifier != 'val'):
          #    self.b.append('definingExpressionWithBody: not a val? label:')
          #    self.b.append(tree.defMark.identifier)
          #    self._newLine()
          assert(tree.actionMark.identifier == 'val')
          if(tree.isDefinitionFromCompiler):
              self.b.append('toReg ')
              self.b.append(str(tree.register))
              self._space()
              #self.b.append(tree.defMark.identifier)
              #self.b.append('..some contents')
              self._noNewlineDispatch(tree.body[0])
              self._newLine()
          else:
              #self.b.append(tree.actionMark.identifier)
              self.b.append('toSpace ')
              #! should never be empty, so need str()?
              self.b.append(tree.defMark.identifier)
              self._space()
              self.b.append('..some contents')
              for c in tree.body:
                  self._dispatch(c) 
              self._newLine()


    def expressionWithBody(self, tree):
        #print('expression with body: ' + tree.actionMark.identifier)
        # expressionWithBody is definitions of ???, and treeROOT
        #' but will in future be branch calls like case/if
        for c in tree.body:
            self._dispatch(c) 
        self._newLine()

    def _noNewlineDispatch(self, tree):
        if (isinstance(tree, Expression)):
            #self._expression(tree)
            pass
        if (isinstance(tree, Constant)):
            self._constant(tree)
        else:
            self.reporter.error('No newline dispatch is not Expression or Constant: type: {0}'.format(type(tree).__name__))

    def _dispatch(self, tree):
        if (isinstance(tree, ExpressionWithBody)):
            if (tree.isDef):
               #print('CT func def found! :' + tree.defMark.data)
               self.definingExpressionWithBody(tree)
            else:
               #print('CT ExpBody! :' + tree.actionMark.data)
               self.expressionWithBody(tree)
            #for c in tree.body:
            #  self._dispatch(c)
        elif (isinstance(tree, Expression)):
            if(tree.isDef):
                #print('val def found!' + str(tree.mutable))
                self.definingExpression(tree)
            else:
                self.expression(tree)
        if (isinstance(tree, Constant)):
            self.newLineConstant(tree)
