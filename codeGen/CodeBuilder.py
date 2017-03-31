#!/usr/bin/python3


#from TreeTraverser import TreeTraverser, PruningTraverser
from trees.Trees import *
from codeGen.Templates import tmpl, stock_tmpl
#from codeGen.MCodeContext import MCodeContext

#class CodeBuilder(TreeTraverser):
class CodeBuilder():
    def __init__(self, tree, reporter, codeGenContext):
        self.reporter = reporter
        self.codeGenContext = codeGenContext
        # The expression stack handles nested expressions
        # in the form +(2 *(14 3)).
        # These cannot be resolved when parsed, as we must
        # have a complete expression, two terms and a
        # mark/function symbol, to write code.
        # The Jack Crenshaw solution is to ask code to push
        # terms which have no complement to the computer stack.
        # But I see no reason why not keep the incomplete
        # AST expressions on an AST stack, then write code
        # by popping them back off, writing as we go.
        self.expressionStack = []

        # Also, the conventional assembly storage model is a stack
        # However, this causes problems with the registers,
        # which are random acess.
        # I'm try the use of an array model, or 'slots'.
        # The problem here is that slots will not model the
        # action of a stack very well. slot(14) means 'make sure 8--13'
        # are popped, then pop'. And throw an error if you do not repush.
        # However, slots will model parameter passing conventions ok,
        # at least when building. And they can handle nested
        # expressions in a way a stack can not. For
        # (2/(3*5))
        # a stack recurses into the internal expression, then must shunt
        # the resulting expression out to get,
        # (2/result)
        # Wheras a slot has an idea of position, so can say,
        # (2: pos 1/ result: pos 2)
        # ?
 
        # builders
        self.architecture = "BITS 64\n\n\nextern printf"
        # read-only data
        self.readOnlyStanzaPrelude = "\n\nSECTION .rodata\n"
        # initialised data
        self.initialisedStanzaPrelude = "\n\nSECTION .data\n"
        self.prelude = self.architecture + self.readOnlyStanzaPrelude + self.initialisedStanzaPrelude

        # uninitialised data
        self.uninitialisedStanzaPrelude = "\n\nSECTION .bss\n"
        self.instructionStanzaPrelude = "\n\nSECTION .text\n\nglobal main\n"
        self.globalStanzaPrelude = self.uninitialisedStanzaPrelude + self.instructionStanzaPrelude

        # TODO: should be '_start'? 'main' is something else?
        self.mainOpen = "\nmain:\n  push rbp\n"
        self.mainClose = "\n  pop rbp\n  mov rax,0\n  ret\n"
        self.constB = []
        self.subprogramB = []
        self.b = []

        # autorun
        # start on slot 0
        #self.dispatch(tree, 0)
        self.writeBodyList(tree.body)

    def _addNewline(self):
        self.b.append('\n')
       
    ## May need to get more sophisticated for 
    # later phases such as inlining?
    def result(self):
        '''
        @return the builder as blocks.
        '''
        r = [self.prelude]
        r.extend(self.constB)
        r.append('\n')
        r.extend(self.globalStanzaPrelude)
        r.append(self.mainOpen)
        r.extend(self.b)
        r.append(self.mainClose)
        return r

    def writeDefinitionMark(self, tree):
        # for now. Needs labels checking, etc.
        self.constB.append(tree.data)

    def writeMark(self, tree):
        # for now. Needs labels checking, etc.
        self.b.append(tree.data)

    def writeDefinitionConstant(self, t):
        '''
        Definition label writer.
        '''
        if (t.tpe == ConstantKind.string):
            self.constB.append('"')
            self.constB.append(t.data)
            self.constB.append('"')
        else:
            self.constB.append(t.data)

    def writeConstantToSlot(self, t, slot):
        '''
        General label writer---intended for non-definition
        constants in expressions.
        '''
        f = stock_tmpl['data_move']
        cnst = ''
        if (t.tpe == ConstantKind.string):
            cnst = '"{0}"'.format(t.data)
        elif (t.tpe == ConstantKind.floatNum):
            #TODO: Move to a template (should react to type, too...?)
            cnst = '__float64__({0})'.format(t.data)
        else:
            cnst = t.data
        self.b.append(f(self.codeGenContext.registerToString(slot), cnst))

    def writeMutableVal(self, tree):
        '''
        Identifier ~ ':' ~  'db' ~ Constant
        (len_str:	equ $-Hello)
        '''
        #label = tree.children[0].data
        #self.constB.append(label)
        self.writeDefinitionMark(tree.defMark)
        self.constB.append(':\tdb  ')
        self.writeDefinitionConstant(tree.children[0])
        self.constB.append('\n')

    def writeImmutableVal(self, tree):
        '''
        Identifier ~ ' equ ' ~ Constant
        '''
        self.writeDefinitionMark(tree.defMark)
        self.constB.append(' equ ')
        self.writeDefinitionConstant(tree.children[0])
        self.constB.append('\n')

    def writeParamDefs(self, tree):
        '''
        Def params never have nesting, only marks.
        e.g. 'defunc(x, y)'
        '''
        for t in self.children:
            self.writeMark(tree)

    '''
    def renderTwig(self, tree):
        r = 'Oops'
        if (isinstance(tree, ExpressionWithBody)):
            return self.renderTwig(tree.actionMark)
        elif (isinstance(tree, Expression)):
            return self.renderTwig(tree.actionMark)
        elif (isinstance(tree, Mark)):
            return tree.data
        elif (isinstance(tree, Constant)):
            if (tree.tpe == ConstantKind.string):
                return '""{0}"'.format(tree.data)
            else:
                return tree.data
        else:
            self.reporter.error("renderTwig: Unrecognised class name: '{0}'".format(type(tree).__name__))
    '''
    '''
    def renderTwigParentExpression(self, tree):
        mrk = tree.actionMark.data
        f = tmpl.get(mrk)
        print('twig parent expression: ' + mrk)
        if f:
            self.writeMark(tree.actionMark)
            print('  childCount: ' + str(len(tree.children)))
            paramList = [self.renderTwig(e) for e in tree.children]
            self.b.append(f(paramList))
            self.b.append('\n')
        else:
            # twig expression yet unknown name
            # anything else must be a function call (?)
            # we catch no undeclared functions errors and the like,
            # assume the function is now valid
            # (if a twig, no parameters to handle)
            f = stock_tmpl['function_call']
            self.b.append(f(tree.actionMark.data))
            self.b.append('\n')

        #else:
         #   self.reporter.error("Expression symbol unrecognised in templates '{0}'".format(mrk))
    '''
    def writeBodyList(self, lst):
        '''
        in an expression list, each expression can be written
        immediately, as the only interaction is through labels.
        An expression list would be a block e.g. a function body.
        '''
        for t in lst:
            self.dispatch(t)
            self._addNewline()

    def writeTreeListAndIncrementSlots(self, lst, startSlot):
        '''
        Used for parameters.
        in an expression list, each expression can be written
        immediately, as the only interaction is through labels and constants?
        It may also be a function call list? 
        '''
        i = startSlot
        for t in lst:
            self.dispatch(t, i)
            i += 1
        return i


    '''
    def renderTwigParentExpressionWithBody(self, tree):
        # below is like renderTwigParentExpression but, with body rendering?
        mrk = tree.actionMark.data
        f = tmpl.get(mrk)
        print('twig parent expression with body expression: ' + mrk)
        if f:
            self.writeMark(tree.actionMark)
            print('  childCount: ' + str(len(tree.children)))
            print('  bodyCount: ' + str(len(tree.body)))
            paramList = [self.renderTwig(e) for e in tree.children]
            bodyList = [self.renderTwig(e) for e in tree.body]
            self.b.append(f(paramList, bodyList))
            self.b.append('\n')
        else:
            self.reporter.error("ExpressionWithBody symbol unrecognised in templates '{0}'".format(mrk))
    '''
    def writeCallExpressionWithBody(self, tree):
        '''
        For non-def expressions, with body, comments, etc.
        Not worked out how to do if... jumps. switch... while... etc?
        '''

            # now need to resolve body expressions...
        #self.writeTreeList(tree.body, slot)


    def writeFunctionCall(self, tree, slot):
            f = stock_tmpl['function_call']
            self.b.append(f(tree.actionMark.data))
            # TODO: Now need to move the return into a slot
            # currently assume returns in rax
            if (slot != 0):
                f = stock_tmpl['data_move']
                self.b.append(f(
                    self.codeGenContext.registerToString(slot),
                    self.codeGenContext.registerToString(0)
                    ))

    def writeCallExpression(self, tree, slot):
        '''
        For non-def expressions, not with body, comments, etc.
        '''
        #print('expression: slot:{0} {1}'.format(slot, tree.toString()))
        self.writeTreeListAndIncrementSlots(tree.children, slot)
        self.writeFunctionCall(tree, slot)


    def dispatch(self, tree):
        '''
        Filters definitions
        '''
        if (isinstance(tree, Constant)):
            #self.writeConstantToSlot(tree, slot)
            pass
        # catch body expressions
        if (isinstance(tree, ExpressionWithBody)):
            # if constant func declaration
            if (tree.defMark):
                #print('func def found! :' + tree.defMark.data)
                pass
            else:
               #self.writeCallExpressionWithBody(tree)
               pass
        elif (isinstance(tree, Expression)):
            if(tree.defMark):
            #if(tree.isDefFromConst()):
                # constant value declaration
                #print('const val def found!' + str(tree.mutable))
                #if (tree.mutable):
                #    self.writeMutableVal(tree)
                #else:
                #    self.writeImmutableVal(tree)
                #self.b.append('\n')
                #return False
                pass
            else:
                # all other expressions dispatched via the
                # actionmark?
                # depends on parameter count...
                #(tree.actionMark.data)

                # ok, write
                #for e in tree.children:
            #self.writeTreeListAndIncrementSlots(tree.children)
                #self.writeCallExpression(tree, slot)
                self.codeGenContext.functionCall(self.b, tree)
                pass
        #if (isinstance(tree, Mark)):
         #   self.b.append(tree.data)
            #b.append()
