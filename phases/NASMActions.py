


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
        if (tree.defMark.identifier[0:2] == '$$'):
            #tree.defMark.data = 'X' + tree.defMark.data
            tree.defMark = tree.defMark.replaceIdentifier('X' + tree.defMark.identifier)

    def expression(self, tree):
      #print('expression: ' + tree.actionMark.data)
        if (tree.actionMark.identifier[0:2] == '$$'):
            #tree.actionMark.data = 'X' + tree.actionMark.data
            tree.actionMark = tree.defMark.replaceIdentifier('X' + tree.defMark.actionMark)

    def definingExpressionWithBody(self, tree):
      #print('defining expression with body: ' + tree.defMark.data)
        if (tree.defMark.identifier[0:2] == '$$'):
            #tree.defMark.data = 'X' + tree.defMark.data
            tree.defMark = tree.defMark.replaceIdentifier('X' + tree.defMark.identifier)

    def expressionWithBody(self, tree):
      #print('expression with body: ' + tree.actionMark.data)
        if (tree.actionMark.identifier[0:2] == '$$'):
            #tree.actionMark.data = 'X' + tree.actionMark.data
            tree.actionMark = tree.defMark.replaceIdentifier('X' + tree.defMark.actionMark)


