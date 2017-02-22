import unittest

#from genCode import MCodeContext

#import genCode
from graphviz.builder import GraphBuilder, DigraphBuilder
import graphviz.builder

class TestGZ(unittest.TestCase):
    '''
    python3 -m unittest graphviz.GZTest
    '''
    #def setUp(self):


    def test_graph_builder(self):
      '''
      python3 -m unittest graphviz.GZTest.TestGZ.test_graph_builder
      '''
      b = GraphBuilder('GZTest', {
      'fontname': '"sans bold"',
      'shape': 'doublecircle',
      'style' : 'filled'
      })
      b.node('A', attrs={ 'label': '"STOP!"', 'color': 'red'})
      b.node('C', attrs={
      'fillcolor': 'green', 
      'color': 'black',
      'fontcolor':'white',
      'label': '"go"'
      })
      b.edge('A', 'B', 'C')
      b.nodeCluster('A', 'B', 'C', attrs={'rank':'same'})
      r = b.result()
      graphviz.builder.write(r, 'build', 'gztest')
      #print(r)
      graphviz.builder.toFormat('build', 'gztest', 'png')



    def test_digraph_builder(self):
      '''
      python3 -m unittest graphviz.GZTest.TestGZ.test_digraph_builder
      '''
      b = DigraphBuilder('GZTest', {
      'fillcolor': 'orange',
      'shape': 'circle',
      'style' : 'filled'
      })
      
      b.edge('A', 'B', 'C')
      r = b.result()
      graphviz.builder.write(r, 'build', 'gztest')
      #print(b.result())
      graphviz.builder.toFormat('build', 'gztest', 'png')
