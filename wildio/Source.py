#!/usr/bin/python3

import os

# TODO: should include token iterator, as main interface to
# parsable naterial?
class Source:
    def __init__(self, srcPath):
        self.srcPath = srcPath

    def pathAsString(self):
        return self.srcPath

    def pathStub(self):
         '''
         basename ~ extension         
         '''
         # not good enough. Should be against preset dir origin...
         return os.path.basename(self.srcPath)

    def fileName(self):
         '''
         basename ~ extension         
         '''
         stub = self.pathStub()
         i = stub.rfind('.')
         if (i != 1):
           return stub[0:i]
         else:
           return stub

    def get(self):
        srcAsLines = None
        with open(self.srcPath, 'r') as f:
            srcAsLines = "".join(f.readlines())
        return srcAsLines

