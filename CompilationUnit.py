#!/usr/bin/python3


from trees.Trees import *

import newNames

# as in Global

class CompilationUnit:
    '''
    Would usually represent one source file, or similar.
    Wraps the source file with the resulting tree. As the tree is transformed, maintains the connection with source data and error reporting.
    '''
    def __init__(self, source):
      self.source = source
      #self.reporter = reporter
      self.tree = NoTree

      # May seem an odd addittion,
      # But the temp names are associated 
      # with a compilation unit
      self.newNames = newNames.NewName()

      self.liveRanges = None
      # the builder as blocks.
      self.mCode = None
      # status report calls?
      # final code (icode)?
      # namegenerators?
      #dependencies?
