
import graphviz.builder

#? no need for this to be a class at all, it is a template at best
# and needs no more than a namespace and to be passing objects, not 
# 'self'
#? This turned into an ass as Python looses track of references someplace. so I'm not
#? eaten up about it. revisit later.
# See SubComponent
# Transform blends a tree transformer with a subcomponent, as do other
# classes like SyntaxAnalyzer

#! add reporter
#a http://www.scala-lang.org/old/sid/2

from util.codeUtils import StdPrint 
    
class GraphOrderable(StdPrint):
    '''
    @param after place immediately after this element name. Overrides
     other placement info. Can be None.
    @param placeAfterSeq place after element names in this array
    @param placeBeforeSeq place before element names in this array
    '''
    def __init__(self, name, after, placeAfterSeq, placeBeforeSeq):
        StdPrint.__init__(self, 'GraphOrderable')
        self.name = name    
        #runsRightAfter
        self.after = after
        #runsAfter
        self.placeAfter = placeAfterSeq
        #runsBefore
        self.placeBefore = placeBeforeSeq

    def addSeqString(self, b, seq):
       first = True
       for e in seq:
          if (first):
            first = False
          else:
            b.append(', ')
          b.append(e)
       return b

    def addString(self, b):
       b.append('name:')
       b.append(self.name)
       b.append(', after:')
       b.append(str(self.after))
       b.append(', placeAfter:')
       self._addSeqString(b, self.placeAfter)
       b.append(', placeBefore:')
       self._addSeqString(b, self.placeBefore)
       return b




from collections import namedtuple


DependencyGraphEdge = namedtuple('Edge', 'frm to hardCoded')



class DependencyGraphNode():
    def __init__(self, name):
        self.name = name
        # A list because at the hard links crush stage, 
        # forward links are dragged back to here.
        # starts with the element referenced by the name.
        # was phaseObject
        # Elements
        self.objects = []
        # hashed edges connecting to this node
        # Edges
        self.after = set()
        # hashed edges connecting to this node
        # Edges
        self.before = set()
        self.visited = False
        self.level = 0

    def addNames(self, b):
        if(not self.objects):
            b.append(self.name)
        else:
            #lst.map(_.phaseName).reduceLeft(_+","+_)
            first = True
            for obj in self.objects:
                first = False if first else b.append(', ')
                b.append(obj.name)
            

class DependencyGraph():
    def __init__(self):
        # name -> Node. Full collection.
        self.nodes = {}
        # hashed edges. Full collection - nodes also carry 
        # collections of edges referring to themselves.
        self.edges = set()

    def info(self, msg):
        print(msg)

    # getNodeByPhase
    def getUpdateNodeByName(self, name):
      ''' 
      Given the name of a phase object, get the node for that name. If the
      node object does not exist, create it.
      '''
      if name in self.nodes:
          return self.nodes[name]
      else:
          n = DependencyGraphNode(name)
          self.nodes[name] = n
          return n



    # getNodeByPhase
    def getUpdateNodeByObj(self, obj):
        '''
        Given a phase object, get the node for this phase object. If the
        node object does not exist, then create it.
        '''
        node = self.getUpdateNodeByName(obj.name)
        if(not node.objects):
            node.objects = [obj]
        return node 


    def softConnectNodes(self, frm, to):
        '''
        Connect the frm and to nodes with an edge and make it soft.
        Also add the edge object to the set of edges, and to the dependency
        list of the nodes
        Node
        Node
        '''
        e = DependencyGraphEdge(frm, to, False)
        self.edges.add(e)
        frm.after.add(e)
        to.before.add(e)

    def hardConnectNodes(self, frm, to):
        '''
        Connect the frm and to nodes with an edge and make it hard.
        Also add the edge object to the set of edges, and to the dependency
        list of the nodes
        Node
        Node
        '''
        e = DependencyGraphEdge(frm, to, True)
        self.edges.add(e)
        frm.after.add(e)
        to.before.add(e)


    def compilerPhaseList(self):
        '''
        Given the entire graph, collect the phase objects at each level, where the phase
        names are sorted alphabetical at each level, into the compiler phase list
        '''
        b = []
        for v in self.nodes.values():
           if v.level > 0:
             b.append(v)
        
        b.sort(key= lambda n: n.level)
        
        b2 = []
        for n in b:
           b2.extend(n.objects)
           #.toList filter (_.level > 0) sortBy (x => (x.level, x.phasename)) flatMap (_.phaseobj) flatten
        return b2
    
    #?
    def collapseHardLinksAndLevels(self, node, lvl):
        '''
        Test if there are cycles in the graph, assign levels to the nodes
        and collapse hard links into nodes
        '''
        #node = self.nodes[nod.name]
        print('visit:' + node.name + ':' + str(node.visited))

        if (node.visited):
            self.dump("phase-cycle")
            raise Exception("Cycle in phase dependencies detected at '{0}'. Created phase-cycle.dot".format(node.name))
      
      
        if (node.level < lvl):
             node.level = lvl

        #var hls = Nil ++ node.before.filter(_.hard)
        hls = [e for e in node.before if e.hardCoded]

        while (len(hls) > 0):
            # hl is Edge...
            for hl in hls:
                #node.phaseobj = Some(node.phaseobj.get ++ hl.frm.phaseobj.get)
                node.objects.extend(hl.frm.objects)
                node.before = hl.frm.before
                try:
                    del self.nodes[hl.frm.name]
                except KeyError:
                    pass
                # self.nodes[hl.frm.name]
                #edges = edges.difference( hl)
                self.edges.discard(hl)
                #for edge in node.before:
                #    edge.to = node
                #node.before = set([DependencyGraphEdge(edge.frm, node, edge.hardCoded) for edge in node.before])
                b = set()
                #node.before.clear()
                for edge in node.before:
                    newEdge = DependencyGraphEdge(edge.frm, node, edge.hardCoded)
                    b.add(newEdge)
                    #self.edges.add(newEdge)
                node.before = b
            hls = [n for n in node.before if n.hardCoded]
      
        node.visited = True
        #self.nodes[node.name] = node
        #print('visit2:' + node.name + ':' + str(self.nodes[node.name].visited))
        for edge in node.before:
          self.collapseHardLinksAndLevels(edge.frm, lvl + 1)
      
        node.visited = False

    #!
    def validateAndEnforceHardlinks(self):
        ''' 
        Find all edges in the given graph that are hard links. 
        For each hard link we need to check that it's the only
        dependency. If not, then we will promote the
        other dependencies down
        '''
        hardlinks = [e for e in self.edges if e.hardCoded]
    
        #! why? not figured the case
        for e in self.edges:
            if (e.hardCoded):
                if (len(e.frm.after) > 1):
                    self.dump("phase-order")
                    
                    preceeding = ', '.join([e.to.name for e in e.frm.after])
                    raise Exception("Element can not share hard dependency and placement requests: element: '{0}' requests: '{1}'. Created phase-order.dot".format(e.frm.name, preceeding))


        rerun = True
        while (rerun):
            rerun = False
            hardlinks = [e for e in self.edges if e.hardCoded]

            for hl in hardlinks:
                # sanity = before edges from hardcode 'to' links
                sanity = [n for n in hl.to.before if n.hardCoded]
                sanityLen = len(sanity)
                if (sanityLen == 0):
                    raise Exception("There is no runs right after dependency, where there should be one! This is not supposed to happen!")
                else:
                    if (sanityLen > 1):
                        self.dump("phase-order")
                        following = ', '.join([e.frm.name for e in sanity])
                        raise Exception("Multiple elements depend immediately on '{0}': dependents: {1}. Created phase-order.dot".format(sanity[0].to.name, following))
                    else:
                        # Get soft edges from before hardcodes
                        promote = [e for e in hl.to.before if not e.hardCoded]
                         
                        # kill all but hard links
                        # Script-lang grief. This copys someplace,
                        # So need to rereference self.edges to remove
                        for l in hl.to.before:
                          if not l.hardCoded:
                              self.edges.remove(l)
                        # keep dereferenced data up-to-date
                        hl.to.before.clear()
                        hl.to.before.add(sanity[0])

                        for edge in promote:
                            rerun = True
                            # move the soft edge up to the hard edge start.
                            self.info(
                                "promote the dependency of " + edge.frm.name
                                + ": "
                                + edge.to.name + " => " + hl.frm.name
                                )
                            # Script-lang grief. This copys someplace,
                            # So need to rereference self.edges to insert
                            newEdge = DependencyGraphEdge(
                                edge.frm,
                                hl.frm,
                                edge.hardCoded
                                )
                            # keep dereferenced data up-to-date
                            hl.frm.before.add(newEdge)
                            self.edges.add(newEdge)

    def removeDanglingNodes(self):
        ''' 
        Remove all nodes in the given graph that have no orderable element.
        This happens when dependences are declared on no source element.
        Make sure to clean up all edges when removing the node object
        `Inform` with warnings, if an external phase has a
        dependency on something that is dropped.
        '''
        #for (node <- nodes.values filter (_.phaseobj.isEmpty)) {
        emptyNodes = [n for n in self.nodes.values() if (not n.objects)]

        for emptyNode in emptyNodes:
            msg = "dropping node with no phase object '{0}'".format(emptyNode.name)
            self.info(msg)
            
            #informProgress(msg)
            #self.nodes -= node.phasename
            # should not throw, we put it in
            del self.nodes[emptyNode.name]
    
            # Only dropped if was placed before?
            for edge in emptyNode.before:
                # this should not throw, we put it in
                self.edges.remove(edge)
                # update the node lists
                edge.frm.after.remove(edge)

            for edge in emptyNode.after:
                # this should not throw, we put it in
                self.edges.remove(edge)
                # update the node lists
                edge.to.before.remove(edge)
            

    def dump(self, title):
        graphToDotFile(self, title)

####################################  

# _phasesSetToDepGraph
# : mutable.HashSet[SubComponent]
#! put in class as constructor?
def graphOrderableToGraph(graphOrderableSet, firstElem):
    '''
    Given the phases set, will build a dependency graph from the phases set
    Using the aux. method of the DependencyGraph to create nodes and edges.
    '''
    graph = DependencyGraph()
    
    for e in graphOrderableSet:
        fromnode = graph.getUpdateNodeByObj(e)
        
        #! that requiresBefore for us? and placedAfter?
        # runsRightAfter
        if(not e.after):
            # runsAfter
            for name in e.placeAfter:
                tonode = graph.getUpdateNodeByName(name)
                graph.softConnectNodes(fromnode, tonode)
            for name in e.placeBefore:
                if (name != firstElem):
                    tonode = graph.getUpdateNodeByName(name)
                    graph.softConnectNodes(tonode, fromnode)
                else:
                    raise Exception("Before placement requested on '{0}' (nominated as first) element in '{1}'".format(firstElem, fromnode.name))
        else:
            tonode = graph.getUpdateNodeByName(e.after)
            graph.hardConnectNodes(fromnode, tonode)
            
    return graph
        


# Output the phase dependency graph at this stage
# Int
def dumpStage(graph, stage, nodesToPrint):
    #for n in nodesToPrint:
        n = 'phase'
        graphToDotFile(graph, "{0}-{1}".format(n, stage))
        

#computePhaseAssembly
def order(phasesSet, firstElem):
    '''
    Called by Global#computePhaseDescriptors to compute phase order.
    '''
    # Add all phases in the set to the graph
    graph = graphOrderableToGraph(phasesSet, firstElem)
    '''
    val dot = settings.genPhaseGraph.valueSetByUser

    '''
    dumpStage(graph, 1, None)
    
    # Remove nodes without phaseobj
    graph.removeDanglingNodes()

    dumpStage(graph, 2, None)

    # checks hard links and promote nodes down the tree
    graph.validateAndEnforceHardlinks()

    dumpStage(graph, 3, None)

    # test for cycles, assign levels and collapse hard links into nodes
    graph.collapseHardLinksAndLevels(graph.getUpdateNodeByName(firstElem), 1)

    dumpStage(graph, 4, None)
    
    # assemble the compiler
    l = graph.compilerPhaseList()
    
    lNames = [n.name for n in l]
    print('output: ')
    print(', '.join(lNames))
    return l


# DependencyGraph, String
#? Use the graphviz builder?
def graphToDotFile(graph, filename):
    '''
    This is a helper method, that given a dependency graph will generate a graphviz dot
    file showing its structure.
    Plug-in supplied phases are marked as green nodes and hard links are marked as blue edges.
    '''
    #sbuf = new StringBuilder
    b = []
    extnodes = set()
    fatnodes = set()
    b.append("digraph G {\n")
    for edge in graph.edges:
        b.append('"')
        edge.frm.addNames(b)
        b.append("(" + str(edge.frm.level) + ')" -> "')
        edge.to.addNames(b) 
        b.append("(" + str(edge.to.level) + ')"')
        # is it an external plugin?
        #if (not edge.frm.objects.get.head.internal):
            #extnodes.add(edge.frm)
        #! not sure is correct, but what is tail of element, and why?
        #edge.frm.phaseobj foreach (phobjs => if (phobjs.tail.nonEmpty) fatnodes += edge.frm )
        if (len(edge.frm.objects) > 1):
            fatnodes.add(edge.frm)
        #! not sure is correct, looking for empty list?
        #edge.to.phaseobj foreach (phobjs => if (phobjs.tail.nonEmpty) fatnodes += edge.to )
        if (len(edge.to.objects) > 1):
            fatnodes.add(edge.to)
        b.append(' [color="')
        color = "#0000ff" if (edge.hardCoded) else "#000000"
        b.append(color)
        b.append('"]\n')

    for node in extnodes:
        b.append('"')
        node.addNames(b)
        b.append("(" + str(node.level) + ")" + '" [color="#00ff00"]\n')

    #!x fatnodes duplicating, despute sets?
    for node in fatnodes:
        b.append('"')
        node.addNames(b)
        b.append("(" + str(node.level) + ")" + '" [color="#0000ff"]\n')
    
    b.append("}\n")
    out = ''.join(b)
    #print(out)
    graphviz.builder.write(out, 'build', filename)
    graphviz.builder.toFormat('build', filename, 'png')


