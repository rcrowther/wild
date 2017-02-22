#!/usr/bin/python3




from tokens import *


class StringIterator:
    '''
     Raises error on end of iteration
    '''
    def __init__(self, source, srcText):
        self.source = source
        self.src = srcText
        self.i = 0
        self.len = len(srcText)
        self.lineOffset = 1
        self.lineCount = 1


    def __iter__(self):
        return self


    def __next__(self): # Python 3: def __next__(self)
        if (self.i < self.len):
            c = self.src[self.i]
            self.i += 1
            r = ord(c)
            self.lineOffset += 1
            if (r == LINE_FEED):
                self.lineOffset = 1
                self.lineCount += 1
            return r
        else:
            raise StopIteration

    def error(m):
       print('[lexicalError] ' + m)

