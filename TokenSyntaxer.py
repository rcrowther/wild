#!/usr/bin/python3

import sys
#import io
#from io import *
from Position import Position
#from Reporter import Reporter
from reporters import Reporter
from tokens import *
from trees import *
from Kinds import *
from wildio import *



##
# Position/reporter
# Continue the block() build
# Make all rules return results?
# But 'and' can fail in a rule?
# There is a difference between 'didn't start with this' and 'started ok but failed'?
# Have a body vs. child issue, which means passing back lists, not passing trees in?
# Lets boost the booleans
# Decide type annotation positions
# How to do parameter definitions? Can be Mark direct?
class TokenSyntaxer:
    '''
    '''
    def __init__(self, tokenIt, reporter):
        self.it = tokenIt
        self.tok = tokens['empty']
        self._next()
        # Token offset must be where it started,
        # Not where it is...
        self.prevLine = 1
        self.prevOffset = 1
        self.treeRoot = ExpressionWithBody('TREE_ROOT')
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
        reporter.error(m + txtO, self.position())

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
    def ruleTokenMatch(self, ruleName, tok):
       if (tok == self.tok):
         self._next()
       else:
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
           self.ruleTokenMatch('Generic Parameters', tokens['rsquare'])

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
    def constantExpression2(self, lst, optional):
        '''
        (IntNum | FloatNum | String) ~ option(KindAnnotation)
        '''
        commit = self.isToken('intNum') or self.isToken('floatNum') or self.isToken('string')
        if (not optional and not commit):
            self.expectedRuleTokensError('Constant', ['intNum', 'floatNum', 'string']) 
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

    def identifierExpression2(self, lst):
        '''
        id ~ ('(' ~ zeroOrMore(Expression) ~')' | Constant)
        Used for all embedded expressions? 
        Constant allowable as param without brackets (?)
        '''
        commit = self.isToken('identifier')
        if (commit):
            t = Expression(self.textOf(), self.position())
            lst.append(t)
            self._next()
            commitParams = self.isToken('lbracket')
            if (commitParams):
                self._next()
                self.zeroOrMore(self.expression2, t.children)
                self.ruleTokenMatch('Identifier Expression', tokens['rbracket'])
            else:
                self.constantExpression2(t.children, False)
            self.optionalKindAnnotation(t)
        return commit

    def expression2(self, lst, optional):
        commit = (
            self.constantExpression2(lst, True) 
            or self.identifierExpression2(lst)
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
       self.zeroOrMore(self.expression2, lst)


    ## Comment
    def comment2(self, l):
        commit = self.isToken('comment')
        if (commit):
            l.append(Comment(self.textOf().strip(), self.position()))
            self._next()
        return commit

    def multilineComment2(self, l):
        commit = self.isToken('multilineComment')
        if (commit):
            l.append(Comment(self.textOf().strip(), self.position()))
            self._next()
        return commit

    ## declarations
    def parametersforDefine(self, lst):
        self.ruleTokenMatch('Definition Parameters', tokens['lbracket'])
        while(self.isToken('identifier')):
            t = Mark(self.textOf())
            lst.append(t)
            self._next()
            # optional type...  
            self.optionalKindAnnotation(t)
        self.ruleTokenMatch('Definition Parameters', tokens['rbracket'])

    def defineVal2(self, lst):
        '''
        'val' ~ Identifier ~ Expression
        Definitions of singular data
        '''
        #print('defval ' + self.textOf())
        commit = (self.isToken('identifier') and self.textOf() == 'val')
        #print(commit)
        if(commit):
            t = Expression('val', self.position())
            lst.append(t)
            self._next()
            if(not self.isToken('identifier')):
              self.expectedRuleTokenError('Define Value', tokens['identifier'])
            mark = self.textOf()
            t.setDefMark(mark)
            t.mutable = mark.endswith('!') 
            self._next()
            # this is expression..
            self.expression2(t.children, False)
        return commit

    def defineFunction2(self, lst):
        '''
        'fnc' ~ Identifier ~ DefineParameters ~ ExplicitSeq
        Definitions attached to code blocks
        '''
        commit = (self.isToken('identifier') and self.textOf() == 'fnc')
        if(commit):
             t = ExpressionWithBody('fnc', self.position())
             lst.append(t)
             self._next()
             if(not self.isToken('identifier')):
                 self.expectedRuleTokenError('Define Function', tokens['identifier'])
             t.setDefMark(self.textOf())
             self._next()
             # generic params?
             self.parametersforDefine(t.children)
             self.explicitSeq(t.body)
        return commit 


    def seqContents(self, lst):
        '''
        Used for body contents
        '''
        while(
            self.comment2(lst)
            or self.multilineComment2(lst)
            or self.defineVal2(lst)
            or self.defineFunction2(lst)
            or self.expression2(lst, True)
            #or self.newline(t)
            ):
            #print('loo')
            pass


    def explicitSeq(self, lst):
        self.ruleTokenMatch('Explicit Expression Seq', tokens['lbracket'])
        self.seqContents(lst)
        self.ruleTokenMatch('Explicit Expression Seq', tokens['rbracket'])

    def root(self):
        try:
            #self.block(self.treeRoot)
            self.seqContents(self.treeRoot.body)
            # if we don't except on StopIteration...
            self.error('Parsing did not complete')
        except StopIteration:
            # All ok
            pass

       

#test

#from StringIterator import StringIterator
#from TokenIterator import TokenIterator
#from Source import Source
'''
from reporters.ConsoleStreamReporter import ConsoleStreamReporter

srcPath = "/home/rob/Desktop/wild/test/test.wild"

s = Source(srcPath)
it = StringIterator(s, s.get())

tokenIt = TokenIterator(it)
reporter = ConsoleStreamReporter()
p = TokenSyntaxer(tokenIt, reporter)

print('tree:')
#print(p.ast().toFrameString())
print(p.ast().toPrettyString())

#print(src)
print("done syntax")
'''
