#!/usr/bin/python3


from wildio.StringIterator import StringIterator
#from codeGen.spliceCode import *

from wildio.Source import Source

## TODO:

HASH = 35
LINE_FEED = 10

#! repeated. see parse
tokens = {
        'error' : 0,
        'newline' : 1,
        'comment' : 2,
        'item' : 3
        }

tokenToString = {v : k for k,v in tokens.items()}

class SpliceLexIterator:
    '''
    '''
    def __init__(self, srcItr):
        self.it = srcItr
        self.b = []
        self.tok = tokens['error']
        self.c = self.it.__next__()


    def source(self):
        return self.it.source

    def lineOffset(self):
        return self.it.lineOffset

    def lineCount(self):
        return self.it.lineCount

    def textOf(self):
        return ''.join(map(chr, self.b))

    def _next(self):
        self.c = self.it.__next__()


    def _clear(self):
        self.b = []


    def _loadUntil(self, c):
        while(self.c != c):
            self.b.append(self.c)
            self._next()
        self._next()

    def isWhitespace(self, c):
        return (c <= 32)

    def isHorizontalWhitespace(self, c):
        return (c <= 32 and c != LINE_FEED)


    def skipHorizontalWhitespace(self):
        while (self.isHorizontalWhitespace(self.c)):
           self._next()

    def scanComment(self):
       if (self.c == HASH):
           self._next()
           if (self.c == HASH):
               self._next()
               self._loadUntil(HASH)
               self.tok = tokens['comment']
           else:
               self._loadUntil(LINE_FEED)
               self.tok = tokens['comment']   
            
           return True
       else:
           return False

    def scanItem(self):
        if (self.c != LINE_FEED): 
          while(not self.isWhitespace(self.c)):
            self.b.append(self.c)
            self._next()
          self.tok = tokens['item']
          #self._next()   
          return True
        else:
          return False


    def scanNewLine(self):
        if (self.c == LINE_FEED):
          self.tok = tokens['newline']   
          self._next()
          return True
        else:
          return False

    def getNext(self):
        self.skipHorizontalWhitespace()
        self._clear()
        if (self.scanComment()):
            pass
        elif (self.scanItem()):
            pass
        elif (self.scanNewLine()):
            pass
        else:
            # Unscanable. Should never be reached.
            print('lex no recognise: ' + chr(self.c))
            self.tok = tokens['error']

    def __iter__(self):
        return self

    def __next__(self):
        #print ('__nxt' + str(self.tok))
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
             e == tokens['item']
           ):
             b.append(':')
             b.append(self.textOf())

    def toString(self):
        b = []
        b.append('SpliceLexIterator(')
        self.addString(b)
        b.append(')')
        return ''.join(b)
