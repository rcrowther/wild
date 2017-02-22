from trees.Trees import *

#! deprecated?
class TreeTraverser:
    def __init__(self, tree, topdown = True):
       #self.tree = tree
       #self.topdown = topdown
       if topdown:
           #print('topdown')
           self._topdown(tree)
       else:
           #print('bottomup')
           self._bottomup(tree)

       
    def call(self, tree):
        pass

    def _topdown(self, t):
        self.call(t)
        if t.hasParams:
          for c in t.children:
            self._topdown(c)
        if t.hasBody:
          for c in t.body:
            self._topdown(c)

    def _bottomup(self, t):
        if t.hasParams:
            for c in t.children:
               self._bottomup(c)
        if t.hasBody:
          for c in t.body:
            self._bottomup(c)
        self.call(t)






class PrintMarks(TreeTraverser):
    def __init__(self, tree, topdown = True):
        TreeTraverser.__init__(self, tree, topdown)

    def call(self, tree):
        if (isinstance(tree, Expression)):
            print(tree.actionMark.data)

class PruningTraverser(TreeTraverser):
    '''
    Traverse top down, halting traversal on request.
    See the 'call' method.
    '''
    def __init__(self, tree):
       #self.tree = tree
       #self.topdown = topdown
       self._topdown(tree)


       
    def call(self, tree):
        '''
        @return True if traversal downwards should continue, else false.
        '''
        return True

    def _topdown(self, t):
        r = self.call(t)
        if r and t.hasParams:
          for c in t.children:
            self._topdown(c)
        if r and t.hasBody:
          self._topdown(t.body)

#TODO: Callack traverser for marks only
# MAYBE: make tree double-linked 
class CallbackTraverser:
    def __init__(self, tree):
      self._dispatch(tree) 

    def comment(self, tree):
      pass

    def constant(self, tree):
      pass

    def mark(self, tree):
      pass

    def definingExpression(self, tree):
      pass

    def expression(self, tree):
      pass

    def definingExpressionWithBody(self, tree):
      pass

    def expressionWithBody(self, tree):
      pass

    def _dispatch(self, tree):
        '''
        Filters definitions
        '''
        #print('dispatching callback traverser')
        if (isinstance(tree, Comment)):
            self.comment(tree)
        elif (isinstance(tree, Constant)):
            self.constant(tree)
        elif (isinstance(tree, Mark)):
            self.mark(tree)
        elif (isinstance(tree, ExpressionWithBody)):
            if (tree.defMark):
               #print('CT func def found! :' + tree.defMark.data)
               self.definingExpressionWithBody(tree)
            else:
               #print('CT ExpBody! :' + tree.actionMark.data)
               self.expressionWithBody(tree)
            for c in tree.children:
              self._dispatch(c)
            for c in tree.body:
              self._dispatch(c)
        elif (isinstance(tree, Expression)):
            if(tree.defMark):
                #print('val def found!' + str(tree.mutable))
                self.definingExpression(tree)
            else:
                self.expression(tree)
            for c in tree.children:
              self._dispatch(c)

class CallbackUpdater:
    def __init__(self, tree):
      self._dispatch(NoTree, tree) 

    def comment(self, parent, tree):
      pass

    def constant(self, parent, tree):
      pass

    def mark(self, parent, tree):
      pass

    def definingExpression(self, parent, tree):
      pass

    def expression(self, parent, tree):
      pass

    def definingExpressionWithBody(self, parent, tree):
      pass

    def expressionWithBody(self, parent, tree):
      pass



        
    def _dispatch(self, parent, tree):
        '''
        Filters definitions
        '''
        #print('dispatching callback traverser')
        if (isinstance(tree, Comment)):
            self.comment(parent, tree)
        elif (isinstance(tree, Constant)):
            self.constant(parent, tree)
        elif (isinstance(tree, Mark)):
            self.mark(parent, tree)
        elif (isinstance(tree, ExpressionWithBody)):
            if (tree.defMark):
               #print('CT func def found! :' + tree.defMark.data)
               self.definingExpressionWithBody(parent, tree)
            else:
               #print('CT ExpBody! :' + tree.actionMark.data)
               self.expressionWithBody(parent, tree)
            for c in tree.children:
              self._dispatch(tree, c)
            for c in tree.body:
              self._dispatch(tree, c)
        elif (isinstance(tree, Expression)):
            if(tree.defMark):
                #print('val def found!' + str(tree.mutable))
                self.definingExpression(parent, tree)
            else:
                self.expression(parent, tree)
            for c in tree.children:
              self._dispatch(tree, c)
