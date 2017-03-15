


from Kinds import UnknownKind, Any, Kind, IntegerKind, FloatKind, StringKind
from trees.VisitorBuilder import VisitorBuilder, PrettyVisitorBuilder, TaggedPrettyVisitorBuilder, TersePrettyVisitorBuilder

import trees.Flags
import Position

from enumerations import FuncRenderType

from collections import namedtuple

from util.codeUtils import StdPrint, StdSeqPrint

#PathedIdentifier = namedtuple('SymbolData', 'path identifier')

class PathedIdentifier(namedtuple('SymbolData', 'path identifier')):
        '''
        path string
        identifier string
        '''
       #? could be (mark != NoPathedIdentifier)?
        def isEmpty(self):
            return self.identifier == ''

       #? could be (mark != NoPathedIdentifier)?
        def isNotEmpty(self):
            return self.identifier != ''

        #? Provide in  tree. Used a lot.
        def replaceIdentifier(self, newIdentifier):
            '''
            Must be used immutable, as an assignment
            tree.defMark = tree.defMark.replaceIdentifier(xxx)
            '''
            return self._replace(identifier = newIdentifier)

        def addPrettyString(self, b):
           for e in self.path:
             b.append(e)
             b.append('.')
           b.append(self.identifier)
           return b

        def addString(self, b):
            if (self.path):
                b.append(str(self.path))
                b.append(', ')
            b.append(self.identifier)
            return b

        def toPrettyString(self):
            b = []
            self.addPrettyString(b)
            return ''.join(b)

        '''
        path list of identifiers
        '''
        def __str__(self):
            b = ['PathedIdentifier(']
            self.addString(b)
            b.append(')')
            return ''.join(b)

NoPathedIdentifier = PathedIdentifier([], '')




## 
# Tidy up _toFrameString
# We do need to keep positions in the tree, because of compiler phases,
# Which otherwise do not know position of error.
class Tree(StdSeqPrint):
    '''
    Base tree. 
    Tree enables constant iteration, so includes every syntax rule.
    The base class does very little and is never instatiated.
    '''
    def __init__(self, position = Position.NoPosition):
        StdSeqPrint.__init__(self, 'Tree')
        # if constant
        # if expression
        # if data
        # if kind...


        self.position = position
        # For expressions, a fast call
        # to test if a tree may contain children
        # deprecated?
        self.hasParams = False
        self.hasBody = False
        '''
        Several manipulations work only on expressions
        '''
        self.isNonAtomicExpression = False

        '''
        An abstract expression may be rendered in several ways.
        e.g. assembler calls, macros, values, assembler instructions etc.
        This field allows analysis tools to note decisions.
        The field defaults to saying this expression is rendered as a call.
        '''
        self.renderCategory = FuncRenderType.NOT_FUNC
        #? The below is not necessary, may become supplemental nodes?
        # ok as a default from here down the ancestory. See renderCategory also
        #? not needed for comments and Marks, but yes for Expressions and Constants? 
        self.register = None

   
    #def isTwig(self):
    #    '''
    #    Identifies Tree leaf nodes
    #    A leaf node contains no further evaluable Expressions.
    #    This is, of course, the self-evaluating Constant.
    #    However, it also includes a function call. Which is a 
    #    a Mark as a  an expression. So the Expression
    #    -? must not be a definition,
    #    - have no, or empty, brackets.
    #    The same applies to an ExpressionWithBody, if meeting
    #    the Expression terms and also has an empty body.

    #    leaves:
    #    Constant(0.4 Kind(""float") )
    #    empty Expression(actionMark: Mark(""zee!"))

    #    An Expression function call will not be a leaf if the
    #    function contains inlines because, in that case, further processiong
    #    can be done. (what if it is an inline? probably ok).
    #    '''
    #   return False

    #def isTwigParent(self):
    #   '''
    #   Identifies Tree leaf nodes, or immediate ancestors.

    #   A Tree isTwig if it contains only a leaf, or is an
    #   ancestor of a leaf. Generally, this can be seen
    #   as having no dependancy on other trees. 

    #   A Tree is also LeafOrleafParent if it is an Expression containing
    #   a Mark only (a function call). 
    #   # ? This expression must not be a
    #   definition, 
    #   and have no, or empty brackets. 

    #   An Expression function call will not be LeafOrleafParent if the
    #   function is inlined because, in that case, further processiong
    #    can be done. 

    #  A Tree is also LeafOrleafParent if all immediate children are
    #   LeafOrleafParent.
    #   '''
    #return False

    def _addIndentedValue(self, b, indent, v):
       b.append(indent)
       b.append(v)
 
    def addPrettyString(self, b, indent):
       self._addIndentedValue(b, indent, str(self.renderCategory))
       b.append('\n')
       self._addIndentedValue(b, indent, str(self.register))
       return b
    '''
    def toPrettyString(self):
      b = TaggedPrettyVisitorBuilder(self, True)
      #b = TersePrettyVisitorBuilder(self)
      return "".join(b.result())
    '''
    def addPrettyStringWrap(self, b, indent):
      self._addIndentedValue(b, indent, self.entitySuffix)
      b.append('(\n')
      self.addPrettyString(b, indent + '  ')
      b.append('\n')
      self._addIndentedValue(b, indent, ')')
      return b
    
    def toPrettyString(self):
      b = []
      self.addPrettyStringWrap(b, '')
      return "".join(b)
    
    def addStringWithSeparator(self, b, sep):
       #b.append('renderCategory: ')
       b.append(str(self.renderCategory))
       b.append(sep)
       #b.append('register: ')
       b.append(str(self.register))
       return b





NoTree = Tree(Position.NoPosition)

class Comment(Tree):
    '''
    Mostly, a literal (also comments).
    Has no children, returnKind, parameters, genericParameters...
    '''
    def __init__(self, data, position = Position.NoPosition):
        Tree.__init__(self, position)
        StdSeqPrint.__init__(self, 'Comment')
        self.data = data


    def _truncString(self):
        return self.data[0:8] + '...' if (len(self.data) > 8) else self.data



    def addPrettyString(self, b, indent):
       self._addIndentedValue(b, indent, self._truncString())
       return b

    def addStringWithSeparator(self, b, sep):
       if (len(self.data) > 8):
         b.append(self.data[0:8])
         b.append('...')
       else:
         b.append(self.data)
       return b



# messy, refactor

class ExpressionBase(Tree):
    '''
    Base for expressions 
    i.e. all active code. Has a return Kind, but little else.
    Never activated.
    '''
    def __init__(self, position = Position.NoPosition):
        Tree.__init__(self, position)
        StdSeqPrint.__init__(self, 'ExpressionBase')
        self.returnKind = UnknownKind
        # Big question over how to handle defines
        # Several models possible e.g. LISP,
        # (defun symbol (lambda (args*) (body*)))
        # For now, using this define attribute.
        # A value definition is much the same as an expression
        # but defined
        # val x = 42
        # consistent, difficult to handle with the split parameters
        # Expression(actionMark: val, ('x, 42))
        # but using,
        # Expression(actionMark: 'val,  defMark: 'x, (42))
        # fnc x(a b)()
        # ExpressionWithBody(actionMark: 'fnc,  defMark: 'x, (a b) ())
        #self.defMark = None
        self.defMark = NoPathedIdentifier
        #? The below is not necessary, may become supplemental nodes?
        '''
        Tests if this definition was inserted by the compiler
        '''
        self.isDefinitionFromCompiler = False

    # Needs testing for compatibility if called more than once?
    # What if we know a kind name but not type?
    def setReturnKind(self, name):
        k = Kind(name)
        self.returnKind = k
        return k

    def addPrettyString(self, b, indent):
       if (self.defMark.isNotEmpty()):
           self._addIndentedValue(b, indent, self.defMark.toPrettyString())
           #self._addIndentedValue(b, indent, str(self.defMark))
           b.append('\n')
       self._addIndentedValue(b, indent, self.returnKind.toString())
       b.append('\n')
       Tree.addPrettyString(self, b, indent)
       return b

    def addStringWithSeparator(self, b, sep):
    #def addString(self, b):
       #if (self.defMark !=  No  ):
       #b.append('defmark: ')
       b.append(str(self.defMark))
       b.append(sep)
       #b.append('returnKind: ')
       self.returnKind.addString(b)
       b.append(sep)
       Tree.addStringWithSeparator(self, b, sep)
       return b

#class ExpressionBase(Tree):
    #def __init__(self, name):
        #Tree.__init__(self, name)
        #self.returnKind = UnknownKind 
        #self.params = []

    ## Needs testing for compatibility if called more than once?
    #def setReturnKind(self, name):
        #k = Kind(name)
        #self.returnKind = k
        #return k

    #def appendParam(self, name):
        #'''
        #@return the expression, so it can have a Kind attached.
        #'''
        ## isn't this just a symbol with kind?
        ## how do lisp compilers handle?
        #p = Expression(name)
        #self.params.append(p)
        #return p

INTEGER_CONSTANT = 1
FLOAT_CONSTANT = 2
# No!
#CODEPOINT_CONSTANT = 3
STRING_CONSTANT = 3

# Maintain some basic category of constant kinds using
# this enum
# Reason this is useful, when we carry returnKinds, is where we need the basic category,
# For example, print strings with quote marks round them.
constantTypeToString = {
1: 'INTEGER_CONSTANT',
2 : 'FLOAT_CONSTANT',
3: 'STRING_CONSTANT'
}

# besides convenience, what for?
# How do lisp compilers handle?
## Should differentiate between strings/numbers...
# and default numbers...
# Would be smaller if store numbers as numbers, not strings?
#! constant is not an expression? end of story? but returns a kind?
class Constant(Tree):
#class Constant(ExpressionBase):
    '''
    Literals.
    Strings, numbers. Also symbols?
    Has no children, parameters, generic parameters...
    Has data, and rough type. Inherits returnKind
    @data text gathered from parse
    @tpe general type of Constant i.e. Enum
    '''
    def __init__(self, position, data, tpe):
        ExpressionBase.__init__(self, position)
        StdSeqPrint.__init__(self, 'Constant')
        self.data = data
        self.tpe = tpe
        self.returnKind = Any

    # Needs testing for compatibility if called more than once?
    # What if we know a kind name but not type?
    def setReturnKind(self, name):
        k = Kind(name)
        self.returnKind = k
        return k

    def addPrettyString(self, b, indent):
       #Tree.addPrettyString(self, b, indent)
       #b.append('\n')
       #b.append('returnKind: ')
       self._addIndentedValue(b, indent, constantTypeToString[self.tpe])
       b.append('\n')
       self._addIndentedValue(b, indent, self.data)
       return b

    def addStringWithSeparator(self, b, sep):
    #def addString(self, b):
       ExpressionBase.addStringWithSeparator(self, b, sep)
       b.append(sep)
       #b.append('tpe: ')
       b.append(constantTypeToString[self.tpe])
       b.append(sep)
       #b.append('data: ')
       b.append(self.data)
       return b

def IntegerConstant(data, position = Position.NoPosition):
  t = Constant(position, data, INTEGER_CONSTANT)
  #print('add int' + IntegerKind.toString())
  t.returnKind = IntegerKind
  return t

def FloatConstant(data, position = Position.NoPosition):
  t = Constant(position, data, FLOAT_CONSTANT)
  t.returnKind = FloatKind
  return t

def StringConstant(data, position = Position.NoPosition):
  t = Constant(position, data, STRING_CONSTANT)
  t.returnKind = StringKind
  return t


class Mark(ExpressionBase):
    '''
    Currently unused, but may be shortcut to no-param calls.
    Not evaluated or compiled, a pointer to some place.
    Has no children, parameters, generic parameters...
    Has data/name. Inherits returnKind
    '''
    def __init__(self, data):
        ExpressionBase.__init__(self, Position.NoPosition)
        #StdPrint.__init__(self, 'Mark')
        StdSeqPrint.__init__(self, 'Mark')
        self.data = data
        self.returnKind = Any

    def addStringWithSeparator(self, b, sep):
    #def addString(self, b):
       ExpressionBase.addStringWithSeparator(self, b, sep)
       b.append(sep)
       #b.append('data: ')
       b.append(self.data)
       return b


class Expression(ExpressionBase):
    '''
    Adds an actionmark, seperately (can be anonymous 'lambda'). Note this this could be builtin '+(33 2)' or a definition 'slant(55)'
    Has an actionmark, built as an instance of Mark.
    Has children params. These can be for calls (list of any expression tree) or for a definition (Mark only, see ExpressionWithBody)
    Inherits returnKind. 
    actionMark a pathedIdentifier
    '''
    def __init__(self, actionMark, position = Position.NoPosition):
        ExpressionBase.__init__(self, position)
        #StdPrint.__init__(self, 'Expression')
        StdSeqPrint.__init__(self, 'Expression')
        # if constant
        # if expression
        # if data
        # if kind...
        #self.actionMark = Mark(actionMark)
        self.actionMark = actionMark
        self.children = []
        # Used in defs
        #? May be extended to a series of flags?
        self.isMutable = False
        self.hasParams = True
        self.isNonAtomicExpression = True
        #? The below is not necessary, may become supplemental nodes?
        # ok as a default from here down the ancestory. See register also
        self.renderCategory = FuncRenderType.CALL
        self.register = None

    def isDefFromConst(self):
        '''
        Used in code generation to test for static allocations. 
        '''
        return (
          self.defMark 
          and len(self.children) == 1 
          and isinstance(self.children[0], Constant)
          )

    def appendChild(self, tree):
        self.children.append(tree)
        return tree

    def addExpression(self, actionMark):
        t = Expression(actionMark)
        self.children.append(t)
        return t

    def addExpressionWithBody(self, actionMark):
        t = ExpressionWithBody(actionMark)
        self.children.append(t)
        return t

    def addConstant(self, text, tpe):
        t = Constant(text, tpe)
        self.children.append(t)
        return t
        
    def addMark(self, text):
        t = Mark(text)
        self.children.append(t)
        return t

    def removeChild(self, obj):
        self.children.remove(obj)


    #   self.children = [to if e==fromObj else e for e in self.children]

    def updateChild(self, fromObj, newObj):
        self.children = [newObj if e==fromObj else e for e in self.children]

    def addPrettyString(self, b, indent):
       #print(str(self.actionMark))
       self._addIndentedValue(b, indent, self.actionMark.toPrettyString())
       #self._addIndentedValue(b, indent, str(self.actionMark))
       b.append('\n')
       #b.append('returnKind: ')
       ExpressionBase.addPrettyString(self, b, indent)
       b.append('\n')
       self._addIndentedValue(b, indent, 'children:\n')
       newIndent = indent + '  '
       first = True
       for c in self.children:
         if (first):
             first = False
         else:
             b.append('\n')
         c.addPrettyStringWrap(b, newIndent)
       return b

    def addStringWithSeparator(self, b, sep):
    #def addString(self, b):
       #b.append(', actionMark: ')
       #b.append(self.actionMark.data)
       b.append(str(self.actionMark))
       #b.append(', childCount: ')
       #b.append(str(len(self.children)))
       b.append(sep)
       ExpressionBase.addStringWithSeparator(self, b, sep)
       b.append(sep)
       b.append('children: ')
       first = True
       for c in self.children:
         if (first):
             first = False
         else:
             b.append(sep)
         b.append(str(c))
       return b



class ExpressionWithBody(Expression):
    '''
    Used for defining values and functions 
    Also used for main block.
    
    defMark a pathedIdentifier
    '''
    def __init__(self, actionMark, position = Position.NoPosition):
        Expression.__init__(self, actionMark, position)
        #StdPrint.__init__(self, 'ExpressionWithBody')
        StdSeqPrint.__init__(self, 'ExpressionWithBody')
        self.body = []
        self.hasBody = True



    def setBody(self, actionMark):
        t = Expression(actionMark)
        self.body = t
        return t

    def appendBody(self, tree):
        self.body.append(tree)
        return tree

    # override
    def updateChild(self, fromObj, to):
        self.children = [to if e==fromObj else e for e in self.children]
        self.body = [to if e==fromObj else e for e in self.body]
    #def isTwigParent(self):
    #    r = True
    #    for c in self.children:
    #      r = r and c.isTwig()
    #    for e in self.body:
    #      r = r and e.isTwig()
    #    return r 

    def insertBodyChildBefore(self, seekObj, newObj):
        idx = self.body.index(seekObj)
        self.body.insert(idx, newObj)

    def addPrettyString(self, b, indent):
       Expression.addPrettyString(self, b, indent)
       b.append('\n')
       self._addIndentedValue(b, indent, 'body:\n')
       newIndent = indent + '  '
       first = True
       for c in self.body:
         if (first):
             first = False
         else:
             b.append('\n')
         c.addPrettyStringWrap(b, newIndent)
       return b

    def addStringWithSeparator(self, b, sep):
    #def addString(self, b):
       #b.append(sep)
       #b.append('bodyCount: ')
       #b.append(str(len(self.body)))
       Expression.addStringWithSeparator(self, b, sep)
       b.append(sep)
       b.append('body: ')
       first = True
       for c in self.body:
         if (first):
             first = False
         else:
             b.append(sep)
         #c.addStringWithSeparator(b, sep)
         b.append(str(c))
       return b

