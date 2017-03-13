#!/usr/bin/python3

import os
import wildio.StringIterator
import wildio.TokenIterator


class SourceBase:
    def pathAsString(self):
      pass
    def fileName(self):
      pass
    def tokenIterator(self):
      pass

#! there may be several sources, not necessarily disk-based files. See above.
class Source:
    '''
    Includes a token iterator, as main interface to
    parsable naterial
    '''
    def __init__(self, srcPath):
        self.srcPath = srcPath

    def pathAsString(self):
         '''
         full path as string
         '''
         return self.srcPath

    def pathStub(self):
         '''
         filename
         '''
         #! not good enough. Should be against preset dir origin...
         return os.path.basename(self.srcPath)

    def fileName(self):
         '''
         Filename of this source
         If none, ???        
         '''
         stub = os.path.basename(self.srcPath)
         i = stub.rfind('.')
         if (i != 1):
           return stub[0:i]
         else:
           return stub

    def get(self):
         '''
         return the contents as a string
         If none ???
         '''
         srcAsLines = None
         with open(self.srcPath, 'r') as f:
             srcAsLines = "".join(f.readlines())
         return srcAsLines

    def tokenIterator(self):
         '''
         returns a token iterator of the file
         '''
         it = wildio.StringIterator(self, self.get())
         return wildio.TokenIterator(it)
