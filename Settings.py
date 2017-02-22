#!/usr/bin/python3

import os
from collections import namedtuple


SettingsData = namedtuple('SettingsData', 'description value')


class Settings():
    '''
    Used to carry notions from the commandline, config files, build tools, etc.
    '''
    # Yes, yes mutale. look up records or whatever it is?
    def __init__(self):
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
       'XCphases': SettingsData('output phase data while compiling', True)
       }

    def compilerSettings(self):
       return {
       'XCphaseStop': SettingsData('stop at named phase', None),
       #'XCphaseStop': SettingsData('stop at named phase', 'parser'),
       'XCparametersStacking': SettingsData('warn that parameters must be stacked (when applicable)', True)
       }

    # some are mutually exclusive?
    # tree/symtable/phases can be done anyhow
    # or all can be done anyhow?
    def alternateOutputSettings(self):
       return {
       'XOphases': SettingsData('report phase data', False),
       'XOsettings': SettingsData('report settings data', False),
       'XOtree': SettingsData('report the tree', True),
       #'XOtree': SettingsData('report the tree', False),
       'XOtokens': SettingsData('report the initial tokens', False),
       'XOexpressionSymbolTable': SettingsData('report the expression symbol table', False),
       'XOkindSymbolTable': SettingsData('report the kind symbol table', False)
       }

    def stockSettings(self):
       return {
       'verbose': SettingsData('output messages', False)
       }

    def ensuredSettings(self):
        return {
        'buildDir': SettingsData(
           "directory to build output",
           os.path.join(os.getcwd(), 'build') 
           )
        }


    def append(self, k, v):
        self.settings[k] = v

    def getDescription(self, k):
        return self.settings[k].description

    def getValue(self, k):
        return self.settings[k].value

    def addStringSettingsData(self, b, data):
       b.append('"')
       b.append(data.description)
       b.append('", ')
       b.append(str(data.value))
       return b

    def toString(self):
       b = []
       first = True
       b.append('Settings(')
       for k, v in self.settings.items():
          if (first):
            first = False
          else:
            b.append(', ')
          b.append(str(k))
          b.append(' -> (')
          self.addStringSettingsData(b, v)
          b.append(')')
       b.append(')')
       return ''.join(b)

