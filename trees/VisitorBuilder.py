

#from trees.Trees import ExpressionWithBody, Expression, Mark, Constant, Comment
#from Trees import ExpressionWithBody, Expression, Mark, Constant, Comment
#from trees.Trees import *
import trees.Trees
from Kinds import *

## This needs sorting out, a lot
# like, much could be DRY, away from inline/pretty printing. 
class VisitorBuilderBase():
    def __init__(self, tree):
      self.b = []  
      self.dispatch(tree)


    def _newline(self):
      '''
       Used in descendants, if not here.
      '''
      self.b.append('\n')

    def result(self):
      return ''.join(self.b)

    #def _addActionMark(self, tree):
     # self.b.append(tree.actionMark.data)

    def addExpressionWithBody(self, tree):
      pass

    def addExpression(self, tree):
      pass

    def addMark(self, tree):
      pass

    def addConstant(self, tree):
      pass

    def addComment(self, tree):
      pass

    def dispatch(self, tree):
      if (isinstance(tree, trees.ExpressionWithBody)):
        self.addExpressionWithBody(tree)
      elif (isinstance(tree, trees.Expression)):
        self.addExpression(tree)
      elif (isinstance(tree, trees.Mark)):
        self.addMark(tree)
      elif (isinstance(tree, trees.Constant)):
        self.addConstant(tree)
      elif (isinstance(tree, trees.Comment)):
        self.addComment(tree)
      else:
        print('OOPS? ' + tree.toString())


class VisitorBuilderRebuilder(VisitorBuilderBase):
    '''
    Output viable code from a tree.
    Not an exact match for the original, but parsable.
    Has some pretty-printing (and similarities to terse-printing also).
    '''
    def __init__(self, tree, withType = False):
      self.withType = withType
      self.indent = ''
      VisitorBuilderBase.__init__(self, tree)

    def addReturnKind(self, tree):
       #print('rt:' + tree.returnKind.toString())
       if (
         self.withType and
         tree.returnKind != UnknownKind and
         tree.returnKind != Any
         ):
         self.b.append(': ')         
         tree.returnKind.addString(self.b)


    def decIndent(self):
        self.indent = self.indent[0: len(self.indent) - 2]

    def incIndent(self):
        self.indent = self.indent + (2 * ' ')
      
    def  _indent(self, s):
      self.b.append(self.indent)
      self.b.append(s)
      self._newline()

    def addList(self, children):
      # for params
      self.b.append(' (')
      first = True
      for c in children:
          if first:
            first = False
          else:
            self.b.append(' ')
          self.dispatch(c)
      self.b.append(')')

    def addIndentedList(self, children):
      # for bodies
      if (children):
        self._newline()
        self._indent('(')
        for c in children:
            self.b.append(self.indent)
            self.dispatch(c)
            self._newline()
        self._indent(')')

    def addExpressionWithBody(self, tree):
      self.addMark(tree.actionMark)
      if tree.defMark:
          self.addMark(tree.defMark)
      self.addList(tree.children)
      self.addReturnKind(tree)
      self.incIndent()
      self.addIndentedList(tree.body)
      self.decIndent()

    def addExpression(self, tree):
      #self.b.append('Expression(')
      #self.b.extend(self.actionMark.addString(b))
      self.addMark(tree.actionMark)
      if tree.defMark:
          self.addMark(tree.defMark)
      #self.b.append('(')
      self.addList(tree.children)
      #self.b.append(')')

    def addMark(self, tree):
      self.b.append(tree.data)

    def addConstant(self, tree):
      if (tree.tpe == trees.STRING_CONSTANT):
        self.b.append('""')
        self.b.append(tree.data)
        self.b.append('"')
      else:
        self.b.append(tree.data)

    def addComment(self, tree):
      # Always as multiline comment?
      self._newline()
      self.b.append(self.indent)
      self.b.append('## ')
      self.b.append(tree.data)
      self._newline()
      self._indent('#')





class VisitorBuilder(VisitorBuilderBase):
    '''
    Full tree representation output.
    Prints class names, etc.
    '''
    def __init__(self, tree, withType = False):
      self.b = []
      self.withType = withType
      #print('tree!')
      VisitorBuilderBase.__init__(self, tree)




    def addList(self, children):
      self.b.append(' (')
      first = True
      for c in children:
          if first:
            first = False
          else:
            self.b.append(' ')
          self.dispatch(c)
      self.b.append(')')

    def addReturnKind(self, tree):
       #print('rt:' + tree.returnKind.toString())
       if (
         self.withType and
         tree.returnKind != UnknownKind and
         tree.returnKind != Any
         ):
         #print('rt:')
         self.b.append('Kind(""')         
         tree.returnKind.addString(self.b)
         self.b.append('") ')

    def addExpressionWithBody(self, tree):
      self.b.append('ExpressionWithBody(')
          #self.b.extend(self.actionMark.addString(b))
      self.addMark(tree.actionMark)
      self.b.append(' ')
      if tree.defMark:
          self.addMark(tree.defMark)
          self.b.append(' ')
      self.addReturnKind(tree)
      self.addList(tree.children)
      self.addList(tree.body)
      self.b.append(')')

    def addExpression(self, tree):
      self.b.append('Expression(')
      #self.b.extend(self.actionMark.addString(b))
      self.addMark(tree.actionMark)
      self.b.append(' ')
      if tree.defMark:
          self.addMark(tree.defMark)
          self.b.append(' ')
      self.addReturnKind(tree)
      self.addList(tree.children)
      self.b.append(')')

    def addMark(self, tree):
      self.b.append('Mark(""')
      self.b.append(tree.data)
      self.b.append('")')

    def addConstant(self, tree):
      self.b.append('Constant(')
      #self.b.append(tree.data)
      if (tree.tpe == trees.STRING_CONSTANT):
        self.b.append('""')
        self.b.append(tree.data)
        self.b.append('" ')
      else:
        self.b.append(tree.data)
        self.b.append(' ')
      #self.b.append(constantTypeToString[self.tpe])
      print( tree.data + tree.returnKind.toString())
      self.addReturnKind(tree)

      self.b.append(')')

    def addComment(self, tree):
      self.b.append('Comment(""')
      self.b.append(tree.data)
      self.b.append('")')



class PrettyVisitorBuilder(VisitorBuilder):
    '''
    Full Tree representation, pretty-print formatted.
    Adds indented layout.
    '''
    def __init__(self, tree, withType = False):
      self.indent = ''
      self.indentStep = 2
      VisitorBuilder.__init__(self, tree, withType)

    def decIndent(self):
        self.indent = self.indent[0: len(self.indent) - self.indentStep]

    def incIndent(self):
        self.indent = self.indent + (self.indentStep * ' ')
      
    def  _indent(self, s):
      self.b.append(self.indent)
      self.b.append(s)
      self._newline()

    def addList(self, children):
      if (children):
        self._indent('(')
        for c in children:
            self.dispatch(c)
        self._indent(')')

    def addIndentedReturnKind(self, tree):
       #print('rt:' + tree.returnKind.toString())
       if (
         self.withType and
         tree.returnKind != UnknownKind and
         tree.returnKind != Any
         ):
         #print('rt:')
         self.b.append(self.indent)
         self.b.append('Kind(""')         
         tree.returnKind.addString(self.b)
         self.b.append('")\n')

    def addExpressionWithBody(self, tree):
      self._indent('ExpressionWithBody(')
      #print('rt:' + tree.returnKind.toString())
      self.incIndent()
      self.addMark(tree.actionMark)
      if tree.defMark:
          self.addMark(tree.defMark)
          self.b.append(' ')
      self.addIndentedReturnKind(tree)
      self.addList(tree.children)
      self.addList(tree.body)
      self.decIndent()
      self._indent(')')


    def addExpression(self, tree):
      self._indent('Expression(')
      self.incIndent()
      self.addMark(tree.actionMark)
      if tree.defMark:
          self.addMark(tree.defMark)
          self.b.append(' ')
      self.addIndentedReturnKind(tree)
      self.addList(tree.children)
      self.decIndent()
      self._indent(')')


    def addMark(self, tree):
      self.b.append(self.indent)
      VisitorBuilder.addMark(self, tree)
      self._newline()

    def addConstant(self, tree):
      self.b.append(self.indent)
      VisitorBuilder.addConstant(self, tree)
      #self._indent(' ')
      #self._indent(constantTypeToString[self.tpe])
      self._newline()

    def addComment(self, tree):
      self.b.append(self.indent)
      VisitorBuilder.addComment(self, tree)
      self._newline()



class TaggedPrettyVisitorBuilder(VisitorBuilder):
    '''
    Full Tree representation, pretty-print formatted.
    Adds indented layout.
    '''
    def __init__(self, tree, withType = False):
      self.indent = ''
      self.indentStep = 2
      VisitorBuilder.__init__(self, tree, withType)

    def decIndent(self):
        self.indent = self.indent[0: len(self.indent) - self.indentStep]

    def incIndent(self):
        self.indent = self.indent + (self.indentStep * ' ')
      
    def  _indent(self, s):
      self.b.append(self.indent)
      self.b.append(s)
      self._newline()

    def  _indentTag(self, s):
      self.b.append(self.indent)
      self.b.append(s)
      self.b.append(': ')

    def addList(self, children):
      if (children):
        self._indent('(')
        for c in children:
            self.dispatch(c)
        self._indent(')')

    def addIndentedReturnKind(self, tree):
       #print('rt:' + tree.returnKind.toString())
       if (
         self.withType and
         tree.returnKind != UnknownKind and
         tree.returnKind != Any
         ):
         #print('rt:')
         self.b.append(self.indent)
         self.b.append('Kind(""')         
         tree.returnKind.addString(self.b)
         self.b.append('")\n')

    def _addExpressionCommon(self, tree):
      self._indentTag('actionMark')
      VisitorBuilder.addMark(self, tree.actionMark)
      self._newline()
      self._indentTag('defMark')
      if tree.defMark:
          VisitorBuilder.addMark(self, tree.defMark)
      self._newline()
      self._indentTag('returnKind')
      self.addIndentedReturnKind(tree)
      self._newline()
      self._indentTag('children')
      self._newline()
      self.addList(tree.children)


    def addExpressionWithBody(self, tree):
      self._indent('ExpressionWithBody(')
      #print('rt:' + tree.returnKind.toString())
      self.incIndent()
      self._addExpressionCommon(tree)
      self._indentTag('body')
      self._newline()
      self.addList(tree.body)
      self.decIndent()
      self._indent(')')


  
    def addExpression(self, tree):
      self._indent('Expression(')
      self.incIndent()
      self._addExpressionCommon(tree)
      self.decIndent()
      self._indent(')')

    def addMark(self, tree):
      self.b.append(self.indent)
      VisitorBuilder.addMark(self, tree)
      self._newline()

    def addConstant(self, tree):
      self.b.append(self.indent)
      VisitorBuilder.addConstant(self, tree)
      #self._indent(' ')
      #self._indent(constantTypeToString[self.tpe])
      self._newline()

    def addComment(self, tree):
      self.b.append(self.indent)
      VisitorBuilder.addComment(self, tree)
      self._newline()


class TerseVisitorBuilder(VisitorBuilderBase):
    '''
    Pretty-print removing meta data.
    Removes strict list bracketing in expressions.
    Substitutes Expression marks with actionMark.
    Removes Comment/Constant marks.
    No Kinds.
    '''
    def __init__(self, tree):
      VisitorBuilderBase.__init__(self, tree)


    def addList(self, children):
      if (children):
        self.b.append(' (')
        first = True
        for c in children:
            if first:
              first = False
            else:
              self.b.append(' ')
            self.dispatch(c)
        self.b.append(')')


    def addExpressionWithBody(self, tree):
      self.addMark(tree.actionMark)
      self.b.append('(')
      self.addList(tree.children)
      self.addList(tree.body)
      self.b.append(')')

    def addExpression(self, tree):
      self.addMark(tree.actionMark)
      self.addList(tree.children)


    def addMark(self, tree):
      self.b.append(tree.data)

    def addConstant(self, tree):
      if (tree.tpe == trees.STRING_CONSTANT):
        self.b.append('""')
        self.b.append(tree.data)
        self.b.append('"')
      else:
        self.b.append(tree.data)
      #self._indent(' ')
      #self._indent(constantTypeToString[self.tpe])


    def addComment(self, tree):
      self.b.append('# ')
      self.b.append(tree.data)


class TersePrettyVisitorBuilder(VisitorBuilderBase):
    '''
    Pretty-print removing meta data.
    Removes strict list bracketing in expressions.
    Substitutes actionMarks for Expression marks.
    Removes Comment/Constant marks.
    No Kinds.
    '''
    def __init__(self, tree):
      self.indent = ''
      VisitorBuilderBase.__init__(self, tree)

    def decIndent(self):
        self.indent = self.indent[0: len(self.indent) - 2]

    def incIndent(self):
        self.indent = self.indent + (2 * ' ')
      
    def  _indent(self, s):
      self.b.append(self.indent)
      self.b.append(s)
      self._newline()

    def addList(self, children):
      if (children):
        self.b.append(self.indent)
        self.b.append('(\n')
        for c in children:
            self.dispatch(c)
        self.b.append(self.indent)
        self.b.append(')\n')


    def addExpressionWithBody(self, tree):
      self.b.append(self.indent)
      self.b.append(tree.actionMark.data)
      self.b.append('(\n')
      self.incIndent()
      self.addList(tree.children)
      self.addList(tree.body)
      self.decIndent()
      self._indent(')')

    def addExpression(self, tree):
      self.addMark(tree.actionMark)
      self.incIndent()
      self.addList(tree.children)
      self.decIndent()


    def addMark(self, tree):
      self._indent(tree.data)

    def addConstant(self, tree):
      if (tree.tpe == trees.STRING_CONSTANT):
        self.b.append(self.indent)
        self.b.append('""')
        self.b.append(tree.data)
        self.b.append('"\n')
      else:
        self._indent(tree.data)
      #self._indent(' ')
      #self._indent(constantTypeToString[self.tpe])


    def addComment(self, tree):
      self.b.append(self.indent)
      self.b.append('# ')
      self.b.append(tree.data)
      self._newline()
