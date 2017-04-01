#!/usr/bin/python3

import sys
from Position import Position
from reporters import Reporter
from tokens import *
from trees import *
import trees.Trees
from Kinds import *
from wildio import *
from enumerations import RenderKind

##!
# Position/reporter
# Continue the block() build
# Make all rules return results?
# But 'and' can fail in a rule?
# There is a difference between 'didn't start with this' and 'started ok but failed'?
# Have a body vs. child issue, which means passing back lists, not passing trees in?
# Lets boost the booleans
# Decide type annotation positions
#! How to do parameter definitions? Can be Mark direct? Seems
# too difficult to make func-only definitions, use a cleanup/rationalise
# phase to 'find simple expressions inside func def/calls then
# replace with Mark?'
#! Some roots can be rationalized, see expressionCall and 'block',
# for example, and other multiple tests against 'identifier'
#! some error reporting is deprecated
#
class TokenSyntaxer:
    '''
    '''
    def __init__(self, tokenIt, reporter):
        self.it = tokenIt
        self.reporter = reporter
        self.tok = tokens['empty']
        self._next()
        # Token offset must be where it started,
        # Not where it is...
        self.prevLine = 1
        self.prevOffset = 1
        self.treeRoot = ExpressionWithBody(trees.Trees.noPathIdentifierValue('TREE_ROOT'))
        # let's go
        self.root()

    def ast(self):
        return self.treeRoot

    def textOf(self):
        return self.it.textOf()

    def _next(self):
        self.prevLine = self.it.lineCount()
        self.prevOffset = self.it.lineOffset()
        self.tok = self.it.__next__()

    def position(self):
        return Position(self.it.source(), self.prevLine, self.prevOffset)

    def error(self, m):
        txt = self.it.textOf()
        if (txt):
            txtO = "\n                token text : '{0}'".format(txt)
        else:
            txtO = ''

        #pos = Position(self.it.source(), self.prevLine, self.prevOffset)
        self.reporter.error(m + txtO, self.position())

        sys.exit("Error message")

    def expectedError(self, tok):
         self.error("Expected one of '{0}' but found '{1}'".format(
             tokenToString[tok],
             tokenToString[self.tok]
             ))



    def expectedRulesError(self, ruleNames):
         self.error("Expected one rule of '{0}' but found '{1}'".format(
             '/'.join(ruleNames),
             tokenToString[self.tok]
             ))

    def expectedRuleTokenError(self, ruleName, tok):
         self.error("In rule '{0}' expected '{1}' but found '{2}'".format(
             ruleName,
             tokenToString[tok],
             tokenToString[self.tok]
             ))

    def expectedRuleTokensError(self, ruleName, tokenNames):
         self.error("In rule '{0}' expected one of '{1}' but found '{2}'".format(
             ruleName,
             '/'.join(tokenNames),
             tokenToString[self.tok]
             ))

    ## Parse utilities ##


    # ok
    def ruleTokenSkip(self, ruleName, tok):
       if (tok == self.tok):
         self._next()
       else:
         self.expectedRuleTokenError(
             ruleName,
             tok
             )

    def ruleTokenMatch(self, ruleName, tok):
       if (tok != self.tok):
         self.expectedRuleTokenError(
             ruleName,
             tok
             )

    def isToken(self, tokenName):
       return (tokens[tokenName] == self.tok)
    


    ## Rules ##






    ## Kind
    def optionalGenericParam(self, kind):
      commit = self.isToken('identifier')
      if(commit):
          retKindText = self.textOf()
          self._next()
          retKindNum = ''
          if (self.isToken('intNum')):
              retKindNum = self.textOf()
              self._next()
          text = retKindText + retKindNum
          k = kind.appendContentKind(text)
          self.optionalGenericParams(k)          
      return commit

    def optionalGenericParams(self, kind):
       if (self.isToken('lsquare')):
           self._next()
           self.optionalGenericParamList(kind)
           self.ruleTokenSkip('Generic Parameters', tokens['rsquare'])

    def optionalGenericParamList(self, kind):
        while (self.optionalGenericParam(kind)):
            pass

    def optionalKindAnnotation(self, tree):
        if (self.isToken('colon')):
           self._next()
           if(not self.isToken('identifier')):
              self.expectedRuleTokenError('Kind Annotation', tokens['identifier'])
           k = tree.setReturnKind(self.textOf())
           self._next()
           # add contents
           self.optionalGenericParams(k)
           #tree Expression('type-annotation')


#////////////////////////////////////////////////////////



   ## literals
    def constantExpression(self, lst, optional):
        '''
        (IntNum | FloatNum | String) ~ option(KindAnnotation)
        '''
        #print('const')
        commit = self.isToken('intNum') or self.isToken('floatNum') or self.isToken('string')
        if (not optional and not commit):
            self.expectedRuleTokensError('Constant Expression', ['intNum', 'floatNum', 'string']) 
        if (commit):
            cst = None
            if (self.isToken('intNum')):
                cst = IntegerConstant(self.textOf(), self.position())       
            if (self.isToken('floatNum')):
                cst = FloatConstant(self.textOf(), self.position())
            if (self.isToken('string')):
                cst = StringConstant(self.textOf(), self.position())
            lst.append(cst)
            self._next()
            self.optionalKindAnnotation(cst)
        return commit

    def identifierPath(self, isFunc):
        '''
        Must start on an identifier
        '''
        #self.ruleTokenMatch('Identifier Path', tokens['identifier'])
        #pathedId = [(self.textOf(), self.position())]
        pathedId = [self.textOf()]
        self._next()
        while(self.isToken('period')):
            self._next()
            self.ruleTokenMatch('Identifier Path', tokens['identifier'])
            #pathedId.append((self.textOf(), self.position()))
            pathedId.append(self.textOf())
            self._next()
        return trees.Trees.PathedIdentifier(pathedId[0:-1], pathedId[-1], False, isFunc)
        #return pathedId


    def pathedIdentifier(self, isFunc):
        self.ruleTokenMatch('Pathed Identifier', tokens['identifier'])
        xPath = self.identifierPath(isFunc)
        return xPath
    '''
    def valueCallExpression(self, lst):
        commit = self.isToken('identifier')
        if (commit):
            #print('VALEXP' + self.textOf())
            t = Expression(self.identifierPath(False), self.position())
            lst.append(t)
        return commit
    '''

    def callExpression(self, lst):
        '''
        id ~ ('(' ~ zeroOrMore(Expression) ~')' | constantExpression)
        Used for all func calls, Will nest down to . 
        Constant allowable as param without brackets (?)
        '''
        commit = self.isToken('identifier')
        if (commit):
            #print('call expression ' + self.textOf())
            #! Need to match at least one expression for further processing
            # Though there is the possibility of *one* parameter, which would
            # be ambiguous with a path?
            # initially assume a data call expression
            t = Expression(self.identifierPath(False), self.position())
            #t = Expression(self.textOf(), self.position())
            t.renderKind = RenderKind.data
            lst.append(t)
            #self._next()
            commitParams = self.isToken('lbracket')
            if (commitParams):
                # ok, brackets makes it a func call expression
                t.actionMark = t.actionMark.toFunc()
                t.renderKind = RenderKind.function
                self._next()
                self.zeroOrMore(self.expression, t.children)
                self.ruleTokenSkip('Identifier Expression', tokens['rbracket'])
            self.optionalKindAnnotation(t)
        return commit

    def expression(self, lst, optional):
        '''
        constantExpression | callExpression
        '''
        #print('expression')
        commit = (
            self.constantExpression(lst, True) 
            or self.callExpression(lst)
            )  
        if (not optional and not commit):
            self.expectedRulesError(['IdentifierExpression', 'Constant'])
        #if (commit):
         #   self.optionalKindAnnotation()
        return commit

    def zeroOrMore(self, rule, lst):
       while(rule(lst, True)):
           pass   

    # problematic error messages?
    '''
    def oneOrMore(self, rule, lst):
       matched = rule(lst)
       if (not matched):
           self.error("Expected one of '{0}' but found '{1}'".format(
             tokensToString(tokens, '/'),
             tokenToString[self.tok]
             )) 
       while(rule(lst)):
           pass 
    '''
    def expressionList(self, lst):
       '''
       zeroOrMore(Expression)
       '''
       self.zeroOrMore(self.expression, lst)


    ## Comment
    def comment(self, lst):
        commit = self.isToken('comment')
        if (commit):
            lst.append(Comment(self.textOf().strip(), self.position()))
            self._next()
        return commit

    def multilineComment(self, lst):
        commit = self.isToken('multilineComment')
        if (commit):
            lst.append(Comment(self.textOf().strip(), self.position()))
            self._next()
        return commit

    ## declarations
    def parametersforDefine(self, lst):
        self.ruleTokenSkip('Definition Parameters', tokens['lbracket'])
        while(self.isToken('identifier')):
            t = Mark(self.textOf())
            lst.append(t)
            self._next()
            # optional type...  
            self.optionalKindAnnotation(t)
        self.ruleTokenSkip('Definition Parameters', tokens['rbracket'])

    def defineVal(self, lst):
        '''
        'val' ~ Identifier ~ Expression
        Definitions of singular data
        '''
        #print('defval ' + self.textOf())
        commit = (self.isToken('identifier') and self.textOf() == 'val')
        #print(commit)
        if(commit):
            t = Expression(trees.Trees.noPathIdentifierValue('val'), self.position())
            lst.append(t)
            self._next()
            if(not self.isToken('identifier')):
              self.expectedRuleTokenError('Define Value', tokens['identifier'])
            #mark = self.textOf()
            #t.setDefMark(mark)
            #t.defMark = mark
            t.defMark = self.pathedIdentifier(False)
            t.mutable = t.defMark.identifier.endswith('!') 
            t.isDef = True
            #self._next()
            # this is expression..
            self.expression(t.children, False)
        return commit

    def defineFunction(self, lst):
        '''
        'fnc' ~ Identifier ~ DefineParameters ~ ExplicitSeq
        Definitions attached to code blocks
        '''
        commit = (self.isToken('identifier') and self.textOf() == 'fnc')
        if(commit):
             t = ExpressionWithBody(trees.Trees.noPathIdentifierFunc('fnc'), self.position())
             lst.append(t)
             self._next()
             if(not self.isToken('identifier')):
                 self.expectedRuleTokenError('Define Function', tokens['identifier'])
             #! pathedIdentifier
             #t.setDefMark(self.textOf())
             #self._next()
             #t.setDefMark(self.pathedIdentifier())
             t.defMark = self.pathedIdentifier(True)
             t.isDef = True
             # generic params?
             self.parametersforDefine(t.children)
             self.explicitSeq(t.body)
        return commit 


    def definePackage(self, lst):
        '''
        'package' ~ PathedIdentifier ~ ExplicitSeq
        '''
        commit = (self.isToken('identifier') and self.textOf() == 'package')
        if(commit):
             t = ExpressionWithBody(trees.Trees.noPathIdentifierValue('package'), self.position())
             lst.append(t)
             self._next()
             #t.setDefMark(self.pathedIdentifier())
             t.defMark = self.pathedIdentifier(False)
             # no params, goto a body
             self.explicitSeq(t.body)
        return commit 

    def defineImport(self, lst):
        '''
        'import' ~ PathedIdentifier
        '''
        #! no, needs to be pathed
        commit = (self.isToken('identifier') and self.textOf() == 'import')
        if(commit):
             t = Expression(trees.Trees.noPathIdentifierFunc('import'), self.position())
             lst.append(t)
             self._next()
             t.defMark = self.pathedIdentifier(True)
        return commit 

    def seqContents(self, lst):
        '''
        Used for body contents
        '''
        while(
            self.comment(lst)
            or self.multilineComment(lst)
            or self.defineVal(lst)
            or self.defineFunction(lst)
            or self.definePackage(lst)
            or self.defineImport(lst)
            or self.expression(lst, True)
            #or self.newline(t)
            ):
            #print('loo')
            pass


    def explicitSeq(self, lst):
        #print('explicitSeq')
        self.ruleTokenSkip('Explicit Expression Seq', tokens['lbracket'])
        self.seqContents(lst)
        self.ruleTokenSkip('Explicit Expression Seq', tokens['rbracket'])

    def root(self):
        try:
            #self.block(self.treeRoot)
            self.seqContents(self.treeRoot.body)
            # if we don't except on StopIteration...
            self.error('Parsing did not complete')
        except StopIteration:
            # All ok
            pass

