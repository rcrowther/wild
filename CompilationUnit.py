#!/usr/bin/python3


from trees.Trees import *

# as Global

class CompilationUnit:
    '''
    Would usually represent one source file, or similar.
    Wraps the source file with the resulting tree. As the tree is transformed, maintains the connection with source data and error reporting.
    '''
    def __init__(self, source):
      self.source = source
      #self.reporter = reporter
      self.tree = NoTree

      # the builder as blocks.
      self.mCode = None
      # status report calls?
      # final code (icode)?
      # namegenerators?
      #dependencies?
