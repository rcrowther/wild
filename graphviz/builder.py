from collections import namedtuple

# Of course, several python/graphviz builders exist. But we need our own, for future conversion.

#a http://graphviz.readthedocs.io/en/latest/manual.html
#a http://www.graphviz.org/doc/info/shapes.html#html
#a http://www.graphviz.org/content/attrs
#a https://web.njit.edu/~kevin/rgb.txt.html
#! neato for undirected graphs?
# use xdot for quick viewing

EdgeData = namedtuple('EdgeData', 'nodeList attrs')
NodeClusterData = namedtuple('NodeClusterData', 'nameList attrs')

#! autoquote fontname, label, other attributes?
class GraphBuilder():
    def __init__(self, name, nodeAttrs= {}, edgeAttrs= {}, codeComment = ''):
        self.name = name
        self.nodeAttrs = nodeAttrs
        self.edgeAttrs = edgeAttrs
        self.codeComment = codeComment

        # node, optional attribute list
        self.nodes = {}
        self.nodeClusters = []
        self.edges = []

    def node(self, name, attrs = {}):
        self.nodes[name] = attrs
 
    def nodeCluster(self, *nameList, attrs = {}):
        self.nodeClusters.append(NodeClusterData(nameList, attrs))

    def edge(self, *nodeList, attrs = {}):
        self.edges.append(EdgeData(nodeList, attrs))

    def _edgeMark(self):
        return ' -- '

    def _renderPrefix(self):
        return 'graph'

    def renderAttrs(self, b, attrs):
        if (attrs):
            b.append('[')
            for k, v in attrs.items():
                b.append(k)
                b.append(' = ')
                b.append(v)
                b.append(' ')
            b.append(']')

    def render(self, b):
        b.append(self._renderPrefix())
        b.append(' ')
        b.append(self.name)
        b.append(' {\n')

        if (self.nodeAttrs):
            b.append(' node ')  
            self.renderAttrs(b, self.nodeAttrs)
            b.append('\n')

        if (self.edgeAttrs):
            b.append(' edge ')  
            self.renderAttrs(b, self.edgeAttrs)
            b.append('\n')

        #? clusters in graphviz are recursive notation
        #a http://www.graphviz.org/content/dot-language
        # but I can't be othered implementing R.C.
        for c in self.nodeClusters:
            b.append(' subgraph {\n')
            b.append(' node ')  
            self.renderAttrs(b, c.attrs)
            b.append(';\n')
            for name in c.nameList:
              b.append(name)
              b.append(';\n')
            b.append('}\n')
            #b.append('\n')

        for name, attrs in self.nodes.items():
            b.append(' ')
            b.append(name)
            b.append(' ')
            self.renderAttrs(b, attrs)
            b.append('\n')

        for e in self.edges:
            first = True

            b.append(' ')
            for n in e.nodeList:
                if (first): 
                    first = False
                else:         
                    b.append(self._edgeMark())
                b.append(n)
            self.renderAttrs(b, e.attrs)
            b.append('\n')
        b.append('}\n')
        return b

    def result(self):
       return ''.join(self.render([]))

class DigraphBuilder(GraphBuilder):
    def _edgeMark(self):
        return ' -> '

    def _renderPrefix(self):
        return 'digraph'





import os
def ensureDirs(p):
    d = os.path.dirname(p)
    os.makedirs(d, exist_ok=True)

#!  generic and temporary writer, for now
def write(dataStr, buildDir, filename):
    dstPath = os.path.join(
        buildDir,
        filename + '.dot'
        )
    ensureDirs(dstPath)
    #print(compilationUnit.source.pathStub())
    #print('AssemblyCode path: ' + assemblyCodePath)
    #print('Source filename: ' + compilationUnit.source.fileName())

    # write machine code as file
    with open(dstPath, 'w') as f:
        f.write(dataStr)

import subprocess

'''
code -> GZ code
'''
#' Debian: canon cmap cmapx cmapx_np dot eps fig gd gd2 gif gv imap imap_np ismap jpe jpeg jpg pdf pic plain plain-ext png pov ps ps2 svg svgz tk vml vmlz vrml wbmp x11 xdot xdot1.2 xdot1.4 xlib

formats = {
    'ps' : 'ps',
    'svg' : 'svg',
    'png' : 'png',
    'jpg' : 'jpg'
    #'html' : 'cmapx',
    #'htm' : 'cmapx'
    }

formatList = formats.keys()

def toFormat(buildDir, filename, frmt = 'png'):
    if (not(frmt in formatList)):
        print("Error: graph conversion: format not recognised: format:'{0}' allowable:{1}".format(frmt, ', '.join(formatList)))
    else:
        srcPath = os.path.join(
                buildDir,
                filename + '.dot'
                )
        dstPath = os.path.join(
                buildDir,
                filename + '.' + frmt
                )
    
        cmd = ['dot', srcPath, '-T' + formats[frmt], '-o', dstPath]
        
        try:
          # Python 3.5
          #subprocess.run(cmd, check=True)
          r = subprocess.call(cmd)
          if (r != 0):
            raise CalledProcessError
          else:
            return True
        except Exception:
          #self.reporter.error("running NASM path:{0}".format(p))
          print("Error: graph conversion: on invokation to:{0} path:{1}".format(frmt, p))
          #CalledProcessError as e:
          #print(e.stderr)
          #self.reporter.error("cmd:{0}".format(' '.join(cmd)))
          return False
    
