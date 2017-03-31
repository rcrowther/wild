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

#? used where?
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

#? Callack traverser for marks only
#? make tree double-linked 
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
            if (tree.isDef):
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
            if(tree.isDef):
                #print('val def found!' + str(tree.mutable))
                self.definingExpression(tree)
            else:
                self.expression(tree)
            for c in tree.children:
              self._dispatch(c)


#? used? Enable!
#! difficult to use
class CallbackBodyBuilder:
    def __init__(self, tree):
      #assert(isinstance(ExpressionWithBody, tree))
      self._dispatch(tree) 

    def child(self, b, tree):
        pass

    def _dispatch(self, tree):
        '''
        Filters definitions
        '''
        assert(isinstance(tree, ExpressionWithBody))
        b = [] 
        for c in tree.body:
            self.child(b, c)
            if (isinstance(c, ExpressionWithBody)):
                self._dispatch(c)
        tree.body = b


class CallbackUpdater2:
    def __init__(self, tree):
        if (isinstance(tree, ExpressionWithBody)):
            for c in tree.children:
              self._dispatch(tree, c)
            for c in tree.body:
              self._dispatch(tree, c)
        elif (isinstance(tree, Expression)):
            for c in tree.children:
              self._dispatch(tree, c)

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
            if (tree.isDef):
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
            if(tree.isDef):
                #print('val def found!' + str(tree.mutable))
                self.definingExpression(parent, tree)
            else:
                self.expression(parent, tree)
            for c in tree.children:
              self._dispatch(tree, c)


class CallbackBodyUpdater:
    '''
    Onky dispatches when parent has a body
    Initial tree must have body to do anything
    '''
    def __init__(self, tree):
        if (isinstance(tree, ExpressionWithBody)):
            for e in tree.body:
              self._dispatch(tree, e)

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
            if (tree.isDef):
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
            if(tree.isDef):
                #print('val def found!' + str(tree.mutable))
                self.definingExpression(parent, tree)
            else:
                self.expression(parent, tree)
