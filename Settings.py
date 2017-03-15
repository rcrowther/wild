#!/usr/bin/python3

import os
from collections import namedtuple

from util.codeUtils import StdSeqPrint 
import operator

'''
class Setting(namedtuple('Setting', 'description value')):

    def addString(self, b, data):
       b.append('Setting(')
       b.append(data.description)
       b.append('", ')
       b.append(str(data.value))
       b.append(')')
       return b

    def __str__(self):
       return ''.join(self.addString([]))
'''    


Setting = namedtuple('Setting', 'description value')


class Settings(StdSeqPrint):
    '''
    Used to carry notions from the commandline, config files, build tools, etc.
    '''
    # Yes, yes mutable. look up records or whatever it is?
    def __init__(self):
        StdSeqPrint.__init__(self, 'Settings')
        # name -> Setting(description, value)
        self.settings = {}
        self.appendColl(self.stockSettings())
        self.appendColl(self.ensuredSettings())
        self.appendColl(self.compilerDisplaySettings())
        self.appendColl(self.compilerSettings())
        self.appendColl(self.alternateOutputSettings())


    def appendColl(self, dix):
        for k, v in dix.items():
            self.settings[k] = v
       
    def compilerDisplaySettings(self):
       return {
       'XCphases': Setting('output phase data while compiling', True)
       }

    def compilerSettings(self):
       return {
       'XCtoPhase': Setting('stop at (including) named phase', None),
       #'XCtoPhase': Setting('stop at named phase', 'parser'),
       'XCparametersStacking': Setting('warn that parameters will be stacked (if alternatives exist)', True)
       }

    # some are mutually exclusive?
    # tree/symtable/phases can be done anyhow
    # or all can be done anyhow?
    def alternateOutputSettings(self):
       return {
       'XOtokens': Setting('report the initial tokens', False),
       'XOphases': Setting('report phase data', False),
       'XOsettings': Setting('report settings data', False),
       'XOtree': Setting('report the last tree', False),
       #'XOtree': Setting('report the tree', False),

       'XOexpressionSymbolTable': Setting('report the expression symbol table', False),
       'XOkindSymbolTable': Setting('report the kind symbol table', False),
       'XOliveRanges': Setting('report the live range data', False)
       }

    def stockSettings(self):
       return {
       'verbose': Setting('output messages', False)
       }

    def ensuredSettings(self):
        return {
        'buildDir': Setting(
           "directory to build output",
           os.path.join(os.getcwd(), 'build') 
           )
        }


    #def append(self, k, v):
    #    self.settings[k] = v

    def getDescription(self, k):
        return self.settings[k].description

    def getValue(self, k):
        return self.settings[k].value

    def setValue(self, k, v):
        newData = Setting(self.settings[k].description, v)
        self.settings[k] = newData

    def testAndSetValue(self, name, v):
        '''
        name name of setting to change
        v string of value. Boolean strings are converted to boolean values
        '''
        setting = self.settings.get(name)
        if (not setting):
            return False
        else:
            if (v == 'True'):
                self.settings[name] = setting._replace(value = True)
            elif (v == 'False'):
                self.settings[name] = setting._replace(value = False)
            else:
                self.settings[name] = setting._replace(value = v)
            return True

    def toHelpString(self):
       b = []
       first = True
       seq = sorted(self.settings.items(), key=operator.itemgetter(0))
       for e in seq:
          if (first):
            first = False
          else:
            b.append('\n')
          b.append(e[0])
          b.append((24 - len(e[0])) * ' ')
          b.append(str(e[1].description))
       return ''.join(b)

    def toPrettyString(self):
       b = []
       first = True
       for k, v in self.settings.items():
          if (first):
            first = False
          else:
            b.append('\n')
          b.append(k)
          b.append(' -> ')
          b.append(str(v.value))
       return ''.join(b)

    def addStringWithSeparator(self, b, sep):
       first = True
       for k, v in self.settings.items():
          if (first):
            first = False
          else:
            b.append(sep)
          b.append(k)
          b.append(' -> ')
          b.append(str(v))
       return b



