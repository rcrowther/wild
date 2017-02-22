

from wildio.StringIterator import StringIterator
from tokens import *

from wildio.Source import Source

## TODO:
# Test for end
# Need to test for '$' initially, as used to mark 
# internal-generated names and marked-up operator to alphanumeric transforms.
# Not reporting errors?
class TokenIterator:
    '''
    Iterate comments, identifiers, numerics, etc.
    Very simple, compared to other efforts, but it works.
    zeroOrMore(zeroOrMore(Space) ~ (
    Comment
    | Number
    | String
    | Punctuation
    | Identifier
    | OperatorIdentifier
    ))
    A few notes:
    Comment can be single or muti-line
    Numbers can include the dot
    Punctuation is always single chars
    Identifier starts with an alphabetic, can be followed by not (whitespace or number).
    OperatorIdentifier starts with any non-whitespace, and is followed by not(whitespace or punctuation or number)

    Stalling on punctuation allows identifiers to push against punctuation. Operator identifiers also stall on numbers, to allow '-20' etc.
    '''
    def __init__(self, srcItr):
        self.it = srcItr
        self.b = []
        self.tok = 99
        self.c = self.it.__next__()

    def source(self):
        return self.it.source

    def lineOffset(self):
        return self.it.lineOffset

    def lineCount(self):
        return self.it.lineCount

    def _next(self):
        #print('_nxt')
        self.c = self.it.__next__()

    def textOf(self):
        return ''.join(map(chr, self.b))

    def _clear(self):
        self.b = []

    def _loadUntil(self, c):
        while(self.c != c):
            #print('cmmnt ' + str(self.c) + str(chr(self.c)))
            self.b.append(self.c)
            self._next()
        self._next()
#??
    #def _loadUntilWhitespace(self, c):
    #    while(self.c != c or self.isWhitespace(self.c)):
    #        self.b.append(c)
    #        self._next()

    def isWhitespace(self, c):
        #print('wt: ' + chr(self.c))
        return (c <= 32)

    def isAlphabetic(self, c):
        return ((c >= 65 and c <= 90) or (c >= 97 and c <= 122) or c == UNDERSCORE)

    def isOperator(self, c):
        ''' + - * %'''
        return (c == 43 or c==45 or c==42 or c==37)

    #def isIdentifier(self, c):
    #    ''' + - * %'''
    #    return (c == 43 or c==45 or c==42 or c==37)

    def isPunctuation(self, c):
        return (
            c == LEFT_BRACKET
            or c == RIGHT_BRACKET
            or c == LEFT_CURLY
            or c == RIGHT_CURLY
            or c == LEFT_SQR
            or c == RIGHT_SQR
            or c == COLON
            or c == SOLIDUS
            or c == PERIOD
            or c == LINE_FEED
            )

    def isNumeric(self, c):
        return (c >= 48 and c <= 57)
# comment
#number

# Duaql test not robust code?
    def scanPunctuation(self):
       if (self.isPunctuation(self.c)):
           if (self.c == COLON):
               self.tok = tokens['colon']
           if (self.c == SOLIDUS):
               self.tok = tokens['solidus']
           if (self.c == PERIOD):
               self.tok = tokens['period']
           if (self.c == LEFT_BRACKET):
               self.tok = tokens['lbracket']
           if (self.c == RIGHT_BRACKET):
               self.tok = tokens['rbracket']
           if (self.c == LEFT_SQR):
               self.tok = tokens['lsquare']
           if (self.c == RIGHT_SQR):
               self.tok = tokens['rsquare']
           if (self.c == LEFT_CURLY):
               self.tok = tokens['lcurly']
           if (self.c == RIGHT_CURLY):
               self.tok = tokens['rcurly']
           if (self.c == LINE_FEED):
               self.tok = tokens['linefeed']

           self._next()
           return True
       else:
           return False

    def scanComment(self):
       if (self.c == HASH):
           self._next()
           if (self.c == HASH):
               self._next()
               self._loadUntil(HASH)
               self.tok = tokens['multilineComment']
           else:
               self._loadUntil(LINE_FEED)
               self.tok = tokens['comment']               
           return True
       else:
            return False

    def scanString(self):
       if (self.c == ICOMMAS):
           self._next()
           if (self.c == ICOMMAS):
               self._next()
               self._loadUntil(ICOMMAS)
               self.tok = tokens['string']
               return True
           else:
               self.error('string balancing')               
           return False
       else:
            return False

    def scanNumber(self):
       if (self.isNumeric(self.c) 
            #or self.c == PLUS 
            #or self.c == HYPHEN_MINUS
            ):
            #while(self.isNumeric(self.c)):
            while(True):
                self.b.append(self.c)
                self._next()
                if(not self.isNumeric(self.c)):
                    break

            #print('?: ' + chr(self.c))
            if (self.c != PERIOD):
                self.tok = tokens['intNum']
            else:
                self.b.append(self.c)
                self._next()
                while(self.isNumeric(self.c)):
                    self.b.append(self.c)
                    self._next()
                self.tok = tokens['floatNum']                 
            return True
       else:
            return False

    def scanIdentifier(self):
        '''
        [a-z, A-Z] ~ zeroOrMore(not(Whitespace) | not(Punctuation))
        '''
        if(self.isAlphabetic(self.c)):
        #if (not self.isWhitespace(self.c)):
          while (
             (not self.isWhitespace(self.c))
              # brackets only?
              and (not self.isPunctuation(self.c))
              ):
            self.b.append(self.c)
            self._next()
          self.tok = tokens['identifier'] 
          return True
        else:
          return False

    def scanOperatorIdentifier(self):
        '''
        [a-z, A-Z] ~  zeroOrMore(not(Whitespace) | not(Numeric) | not(Punctuation))
        '''
        if (not self.isWhitespace(self.c)):
          while (
             (not self.isWhitespace(self.c)) 
              and (not self.isNumeric(self.c))
              # brackets only?
              and (not self.isPunctuation(self.c))
              ):
            self.b.append(self.c)
            self._next()
          self.tok = tokens['identifier'] 
          return True
        else:
          return False


    def skipWhitespace(self):
          while (self.isWhitespace(self.c)):
             self._next()

    def getNext(self):
        self.skipWhitespace()
        self._clear()
        if (self.scanComment()):
            pass
        elif (self.scanNumber()):
            pass
        elif (self.scanString()):
            pass
        elif (self.scanPunctuation()):
            pass
        elif (self.scanIdentifier()):
            pass
        elif (self.scanOperatorIdentifier()):
            pass
        else:
            # Unscanable. Should never be reached.
            self.tok = tokens['empty']

    def __iter__(self):
        return self

    def __next__(self):
        #print ('nxt')
        #print(str(self.c))
        self.getNext()
        return self.tok

    def addString(self, b):
        first = True
        for e in self:
           if first:
             first = False
           else:
             b.append(', ')
           b.append(tokenToString[e])
           if (
             e == tokens['intNum']
             or e == tokens['floatNum']
             or e == tokens['identifier']
           ):
             b.append(':')
             b.append(self.textOf())
           elif (e == tokens['intNum']
             or e == tokens['string']
           ):
             b.append(':""')
             b.append(self.textOf())
             b.append('"')
            
    def toString(self):
        b = []
        b.append('TokenIterator(')
        self.addString(b)
        b.append(')')
        return ''.join(b)
