


from trees.TreeTraverser import CallbackTraverser, CallbackUpdater

from enumerations import FuncRenderType

class NASMPreprocess(CallbackTraverser):
    '''
    '''
    mCodeFunctions = [
    '$$plus$',
    '$$minus$',
    '$$mult$',
    '$$divide$'
    ]

    def __init__(self, tree, reporter):
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
      if (tree.defMark.data[0:2] == '$$'):
          tree.defMark.data = 'X' + tree.defMark.data

    def expression(self, tree):
      #print('expression: ' + tree.actionMark.data)
      if (tree.actionMark.data[0:2] == '$$'):
          tree.actionMark.data = 'X' + tree.actionMark.data

    def definingExpressionWithBody(self, tree):
      #print('defining expression with body: ' + tree.defMark.data)
      if (tree.defMark.data[0:2] == '$$'):
          tree.defMark.data = 'X' + tree.defMark.data

    def expressionWithBody(self, tree):
      #print('expression with body: ' + tree.actionMark.data)
      if (tree.actionMark.data[0:2] == '$$'):
          tree.actionMark.data = 'X' + tree.actionMark.data


from trees.Trees import Constant, Mark


class UnaryMinus(CallbackUpdater):
    '''
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
      (tree.actionMark.data == '$$minus$' or tree.actionMark.data == '$$plus$')
      and len(tree.children) == 1
      and isinstance(tree.children[0], Constant)
      ):
        sign = '-' if (tree.actionMark.data == '$$minus$') else ''
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
      if (
      (tree.actionMark.data in mCodeFunctions)
      and len(tree.children) == 2
      ):
        # Would handle type too, and 32/64bit...
        tree.renderCategory = FuncRenderType.MCODE64
      #else:
       # tree.renderCategory = FuncRenderType.CALL



