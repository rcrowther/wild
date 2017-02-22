#!/usr/bin/python3

import os
import subprocess
from Phase import Phase
from codeGen.CodeBuilder import CodeBuilder


## 
# Tidy up _toFrameString
# How do we write output?
class CodeGenPhase(Phase):
    '''
    Base tree. 
    Tree enables constant iteration, so includes every syntax rule.
    The base class does very little and is never instatiated.
    '''
    def __init__(self, reporter, codeGenContext, settings):
        self.reporter = reporter
        self.codeGenContext = codeGenContext
        self.settings = settings
        Phase.__init__(self,
            "code generation",
            "read tree, generate code",
            True
            )

    def _resolvePath(self, dstDirPath, srcStub):
        return os.path.join(dstDirPath, srcStub)

    def ensureDirs(self, p):
        d = os.path.dirname(p)
        os.makedirs(d, exist_ok=True)

    def nasmCompile(self, p):

      # nasm -f elf64 -F stabs build/test.wild
      cmd = ['nasm', '-f', 'elf64',  '-F', 'stabs', p]
      try:
          # Python 3.5
          #subprocess.run(cmd, check=True)
          r = subprocess.call(cmd)
          if (r != 0):
            raise CalledProcessError
          else:
            return True
      except Exception:
          self.reporter.error("running NASM path:{0}".format(p))
          #CalledProcessError as e:
          #print(e.stderr)
          self.reporter.error("cmd:{0}".format(' '.join(cmd)))
          return False

    def gccLink(self, fromPath, toPath):
      # gcc -o build/test build/test.wild
      cmd = ['gcc', '-o', toPath,  fromPath]
      try:
          # Python 3.5
          #subprocess.run(cmd, check=True)
          r = subprocess.call(cmd)
          if (r != 0):
            raise CalledProcessError
          else:
            return True
      except Exception:
          self.reporter.error("running GCC linker path:{0}".format(fromPath))
          return False

    def run(self, compilationUnit):
        # generate machine code
        cb = CodeBuilder(
            compilationUnit.tree,  
            self.reporter,
            self.codeGenContext
            )

        # stash in the compilation unit
        compilationUnit.mCode = cb.result()

        # make paths
        buildDir = self.settings.getValue('buildDir')
        assemblyCodePath = self._resolvePath(
            buildDir,
            compilationUnit.source.pathStub()
            )
        objectPath = self._resolvePath(
            buildDir,
            compilationUnit.source.fileName() + '.o'
            )
        executablePath = self._resolvePath(
            buildDir,
            compilationUnit.source.fileName()
            )
        self.ensureDirs(assemblyCodePath)
        #print(compilationUnit.source.pathStub())
        #print('AssemblyCode path: ' + assemblyCodePath)
        #print('Source filename: ' + compilationUnit.source.fileName())

        # write machine code as file
        with open(assemblyCodePath, 'w') as f:
            for t in compilationUnit.mCode:
                f.write(t)

        # compile and link
        (self.nasmCompile(assemblyCodePath) 
        and self.gccLink(objectPath, executablePath))

