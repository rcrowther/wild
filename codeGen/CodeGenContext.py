from codeGen.Templates import tmpl, stock_tmpl, word_tmpl
#import codeGen.architectureContext # import STACK, X64ArchitectureContext
from codeGen.architectureContext import STACK, X64ArchitectureContext
from trees import *


# Include, as other phase
# code could use the data?

class CodeGenContext():
    '''
    Link architecture data to templates.
    '''
    def __init__(self, architectureContext):
      self.architectureContext = architectureContext
      #self.mCodeFunctions = []


    def functionCall(self, b, tree):
      pass




class X64CodeGenContext(CodeGenContext):
    '''
    Link architecture data to templates.
    '''
    def __init__(self):
      CodeGenContext.__init__(self, X64ArchitectureContext())
      self.currentParamSlot = 0
      self.currentRegisterSlot = 0
      self.mCodeFunctions = [
        '$$plus$',
        '$$minus$',
        '$$mult$',
        '$$divide$'
        ]


    def resetParamSlots(self):
      self.currentParamSlot = 0

    def resetRegisterSlots(self):
      self.currentRegisterSlot = 0

    def allocateToParam(self, b, tree):
      r = self.architectureContext.getCallRegister(self.currentParamSlot)
      self.currentParamSlot += 1
      if (r == STACK):
        b.append(word_tmpl['stack_push'])
        b.append(' ')
      else:
        b.append(word_tmpl['data_move'])
        b.append(' ')
        b.append(r)
        b.append(',')
      self.renderParam(b, tree) 
      b.append('\n')

    def allocateSlot(self, b, fromData):
      r = self.architectureContext.getRegister(self.currentRegisterSlot)
      self.currentRegisterSlot += 1
      if (r == STACK):
        b.append(stock_tmpl['stack_push'](fromData))
      else:
        b.append(stock_tmpl['data_move'](r, fromData))

    def deallocateSlot(self, b, toRegister):
      self.currentRegisterSlot -= 1
      r = self.architectureContext.getRegister(self.currentRegisterSlot)
      if (r == STACK):
        b.append(stock_tmpl['stack_pop'](toData))
      else:
        b.append(stock_tmpl['data_move'](toRegister, r))

    def renderParam(self, b, tree):
       '''
       Params can be either Constants, Marks (references),
       or Expressions (returned to slots)
       '''
       if (isinstance(tree, Expression)):
         # Expression. 
         # Can only be a mCode call, not custom.
         #self.allocateToParam(b)
         #deallocateSlot(b)
         # This is a nested expression. The handling trick
         # is to bounce the param count back after using the
         # following two param slots
         self.mCodeFunctionCall(b, tree.actionMark.data, tree)
         #self.currentRegisterSlot -= 2
         #return '???'
       if (isinstance(tree, Mark)):
         # Mark (label)
         b.append(tree.data)
       elif (isinstance(tree, Constant)):
         if (tree.tpe == STRING_CONSTANT):
           b.append('"')
           b.append(tree.data)
           b.append('"')
         else:
           b.append(tree.data)

    # will have protection and a returnSlot?
    def customFunctionCall(self, b, mark):
      f = stock_tmpl['function_call']
      b.append(f(mark))

    # Do we return functions, or render here?
    # probably need to do here, and render?
    # will have protection and a returnSlot?
    # need to handle smaller registers?
    def mCodeFunctionCall(self, b, mark, tree):
        #param1 = self.renderParam(tree.children[0])
        #param2 = self.renderParam(tree.children[1])
        #b.append(f([param1, param2]))
        b.append(word_tmpl[mark])
        b.append(' ')
        self.renderParam(b, tree.children[0])
        b.append(',')
        self.renderParam(b, tree.children[1])
        b.append('\n')

    def functionCall(self, b, tree):
      # TODO: Should test type too.
      # and ensure no nested functions?
      mark = tree.actionMark.data
      #kind = tree.returnKind
      if (
      #(mark in self.mCodeFunctions)
      tree.isMachine
      and len(tree.children) == 2
      ): 
        self.mCodeFunctionCall(b, mark, tree)
      else:
        # set params
        for c in tree.children:
          self.allocateToParam(b, c)
        self.customFunctionCall(b, mark)
        self.resetParamSlots()
