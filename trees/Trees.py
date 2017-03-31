


from Kinds import UnknownKind, Any, Kind, IntegerKind, FloatKind, StringKind
#from trees.VisitorBuilder import VisitorBuilder, PrettyVisitorBuilder, TaggedPrettyVisitorBuilder, TersePrettyVisitorBuilder

import trees.Flags
import Position

from enumerations import FuncRenderType, MachineRenderKind
from collections import namedtuple
from util.codeUtils import StdPrint, StdSeqPrint


# need to know if val or func or ambiguity in calls 
class PathedIdentifier(namedtuple('SymbolData', 'path identifier isMutable isFunc')):
        '''
        path string
        identifier string
        '''
       #? could be (mark != EmptyPathedIdentifier)?
        def isEmpty(self):
            return self.identifier == ''

       #? could be (mark != EmptyPathedIdentifier)?
        def isNotEmpty(self):
            return self.identifier != ''

        def toFunc(self):
            return self._replace(isFunc = True)

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
           b.append(', ')
           b.append(str(self.isFunc))
           return b

        def toPrettyString(self):
            b = []
            self.addPrettyString(b)
            return ''.join(b)

        def addString(self, b):
            if (self.path):
                b.append(str(self.path))
                b.append(', ')
            b.append(self.identifier)
            b.append(', ')
            b.append(str(self.isMutable))
            b.append(', ')
            b.append(str(self.isFunc))
            return b

        '''
        path list of identifiers
        '''
        def __str__(self):
            b = ['PathedIdentifier(']
            self.addString(b)
            b.append(')')
            return ''.join(b)

def noPathIdentifierValue(identifier):
   return PathedIdentifier([], identifier, False, False)

def noPathIdentifierFunc(identifier):
   return PathedIdentifier([], identifier, False, True)

class _EmptyPathedIdentifierClass(PathedIdentifier):
        def toPrettyString(self):
            return '<no path>'

        '''
        path list of identifiers
        '''
        def __str__(self):
            return '<no path>'

EmptyPathedIdentifier = _EmptyPathedIdentifierClass([], '', False, False)




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

        # the below are not necessary for an AST
        # and not necessary in some nodes
        # but, aside from some weight, are easier here?
        '''
        An abstract expression may be rendered in several ways.
        e.g. assembler calls, macros, values, assembler instructions etc.
        This field allows analysis tools to note decisions.
        The field defaults to saying this expression is not a function.
        '''
        self.renderCategory = FuncRenderType.NOT_FUNC
        # Next few are used for rendering.
        # They make an interface to information scattered
        # between architecture, type, and initial parsing 
        #? these are abstract categories, not machine code?
        self.isConstant = False
        self.isData = False
        self.isFunc = False
        #used
        self.isMachine = False
        # Used to hold an enumeration of machinecode kinds
        #? Currently 8/32/64 num, but could be string types too?
        self.machineKind = MachineRenderKind.not_machine
        # used to hold the used (result) register when tree nodes
        # are shaped to machine code 
        self.register = None
        self.returnKind = UnknownKind

    def _addIndentedValue(self, b, indent, v):
       b.append(indent)
       b.append(v)
 
    def addPrettyString(self, b, indent):
       self._addIndentedValue(b, indent, str(self.renderCategory))
       b.append('\n')
       self._addIndentedValue(b, indent, 'machine' if self.isMachine else '!Machine')
       b.append('\n')
       self._addIndentedValue(b, indent, str(self.machineKind))
       b.append('\n')
       self._addIndentedValue(b, indent,  str(self.register) if self.register else '!Register')
       return b

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
       b.append(str(self.renderCategory))
       b.append(sep)
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



#! messy, refactor as Enum

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
    Only thin shared with Expressions is the returntype. 
    Othewrwise, it's a basic tree.
    @data text gathered from parse
    @tpe general type of Constant i.e. Enum
    '''
    def __init__(self, position, data, tpe):
        ExpressionBase.__init__(self, position)
        StdSeqPrint.__init__(self, 'Constant')
        # it is, of some kind, be that isMachine or not, etc.
        self.isConstant = True
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
        ##? Uncertain about if the actionMark/defMark
        # would be better stored as idMark/defMark e.g. not,
        # actionMark=val defmark=zee
        # but,
        # idMark=zee defMark=val
        # - the first is better at finding ids of definitions, 
        # - the second is better at finding all idMarks, regardless
        self.defMark = EmptyPathedIdentifier
        # Now we are moving to using defmark as firstMarkAsSymbol
        # need to track defs
        # (an assign is also a firstMarkAsSymbol expression)
        #? will be used for source code defs, or machine code defs?
        #? are constants 'defs'? (probably no, but then, what is this?)
        self.isDef = False
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
       self._addIndentedValue(b, indent, self.defMark.toPrettyString())
       b.append('\n')
       self._addIndentedValue(b, indent, self.returnKind.toString())
       b.append('\n')
       self._addIndentedValue(b, indent, 'isDef' if self.isDef else '!Def')
       b.append('\n')
       Tree.addPrettyString(self, b, indent)
       return b

    def addStringWithSeparator(self, b, sep):
       b.append(str(self.defMark))
       b.append(sep)
       self.returnKind.addString(b)
       b.append(sep)
       Tree.addStringWithSeparator(self, b, sep)
       return b


class Mark(ExpressionBase):
    '''
    We need a Tree element to wrap an abstract name.
    Not needed for action or definition marks, where
    there are dedicated fields, but good for parameters.
    '''
    def __init__(self, defMark):
        ExpressionBase.__init__(self, Position.NoPosition)
        StdSeqPrint.__init__(self, 'Mark')
        self.returnKind = Any
        self.defMark = defMark
        #? The below is not necessary, may become supplemental nodes?
        '''
        Tests if this definition was inserted by the compiler
        '''
        self.isDefinitionFromCompiler = False

    def addPrettyString(self, b, indent):
       self._addIndentedValue(b, indent, self.defMark)
       b.append('\n')
       self._addIndentedValue(b, indent, self.returnKind.toString())
       return b

    def addStringWithSeparator(self, b, sep):
       b.append(self.defMark)
       b.append(sep)
       self.returnKind.addString(b)
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
        StdSeqPrint.__init__(self, 'Expression')
        self.actionMark = actionMark
        '''
        Children means parameter marks, for definitions, 
        or parameter Expressions, for calls, 
        '''
        self.children = []
        # Used in defs
        #? May be extended to a series of flags?
        self.isMutable = False
        self.hasParams = True
        self.isNonAtomicExpression = True
        # ok as a default from here down the ancestory. See register also
        self.renderCategory = FuncRenderType.CALL
        self.register = None
        

   #? deprecate
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

    #? does this work?
    def removeChild(self, obj):
        self.children.remove(obj)


    #   self.children = [to if e==fromObj else e for e in self.children]

    def updateChild(self, fromObj, newObj):
        self.children = [newObj if e==fromObj else e for e in self.children]

    def addPrettyString(self, b, indent):
       self._addIndentedValue(b, indent, self.actionMark.toPrettyString())
       b.append('\n')
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
       b.append(str(self.actionMark))
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
        StdSeqPrint.__init__(self, 'ExpressionWithBody')
        self.body = []
        self.hasBody = True
        self.renderCategory = FuncRenderType.DEF



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

    def insertBodyChildBefore(self, seekObj, newObj):
        idx = self.body.index(seekObj)
        self.body.insert(idx, newObj)

    #! should note success?
    #! doubt if this works?
    def removeBodyChild(self, obj):
        self.body.remove(obj)

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
       Expression.addStringWithSeparator(self, b, sep)
       b.append(sep)
       b.append('body: ')
       first = True
       for c in self.body:
         if (first):
             first = False
         else:
             b.append(sep)
         b.append(str(c))
       return b

