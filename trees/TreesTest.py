import unittest

#from tokens import *
from trees import *
from Kinds import *
from trees.TreeTraverser import CallbackTraverser
import trees.Flags


class CallbackPrinter(CallbackTraverser):
    def __init__(self, tree):
      CallbackTraverser.__init__(self, tree)

    def comment(self, tree):
      print('comment found!')

    def constant(self, tree):
      print('constant: ' + tree.data)

    def mark(self, tree):
      print('mark: ' + tree.data)

    def definingExpression(self, tree):
      print('expression (def): ' + tree.actionMark.data)

    def expression(self, tree):
      print('expression: ' + tree.actionMark.data)

    def definingExpressionWithBody(self, tree):
      print('expression with body (def): ' + tree.actionMark.data)

    def expressionWithBody(self, tree):
      print('expression with body: ' + tree.actionMark.data)



class TestTrees(unittest.TestCase):
    '''
    python3 -m unittest wildio.IOTest
    '''
    def setUp(self):
      tb = ExpressionWithBody('main')
      tb.returnKind = Kind('String')
      tp = Mark('xfoo')
      tc = Comment('commentary')
      tsc = Constant('done!', STRING_CONSTANT)
      t2 = Expression('+')
      t3 = Constant('3.14', FLOAT_CONSTANT)
      t4 = Constant('9', INTEGER_CONSTANT)
      
      #t5 = Expression('annotation')
      tb.appendChild(tp)
      tb.appendBody(tc)
      t2.appendChild(t3)
      t2.appendChild(t4)
      tb.appendBody(t2)
      tb.appendBody(tsc)

      self.testTree = tb

    def test_tree(self):
      '''
      python3 -m unittest trees.TreesTest.TestTrees.test_tree
      '''
      print(self.testTree.toString())

    def test_tree_pretty(self):
      '''
      python3 -m unittest trees.TreesTest.TestTrees.test_tree
      '''
      print(self.testTree.toPrettyString())

    def test_print_marks(self):
      PrintMarks(self.testTree, False)

    def test_visitor_builder(self):
      '''
      python3 -m unittest trees.TreesTest.TestTrees.test_visitor_builder
      '''
      b = VisitorBuilder(self.testTree)
      print(b.result())

    def test_visitor_builder_rebuilder(self):
      '''
      python3 -m unittest trees.TreesTest.TestTrees.test_visitor_builder_rebuilder
      '''
      b = VisitorBuilderRebuilder(self.testTree, True)
      print(b.result())

    def test_visitor_builder_pretty(self):
      '''
      python3 -m unittest trees.TreesTest.TestTrees.test_visitor_builder_pretty
      '''
      b = PrettyVisitorBuilder(self.testTree, True)
      print(b.result())

    def test_visitor_builder_terse(self):
      '''
      python3 -m unittest trees.TreesTest.TestTrees.test_visitor_builder_pretty
      '''
      b = TerseVisitorBuilder(self.testTree)
      print(b.result())

    def test_visitor_builder_terse_pretty(self):
      '''
      python3 -m unittest trees.TreesTest.TestTrees.test_visitor_builder_pretty
      '''
      b = TersePrettyVisitorBuilder(self.testTree)
      print(b.result())

    def test_callback_traverser(self):
      '''
      python3 -m unittest trees.TreesTest.TestTrees.test_callback_traverser
      '''
      CallbackPrinter(self.testTree)

    def test_flags(self):
      '''
      python3 -m unittest trees.TreesTest.TestTrees.test_flags
      '''
      '''
      f = Flags.Flags()
      assert(f.get(4) == False)
      f.on(4)
      assert(f.get(4) == True)
      f.off(4)
      assert(f.get(4) == False)
      '''

      f = Flags.Flags({'named': False, 'isEggy': True})
      print( f.get('named') )
      print( f.get('isEggy') )
      assert(f.get('isEggy') == True)
      f.off('isEggy')
      assert(f.get('isEggy') == False)
      f.on('named')
      assert(f.get('named') == True)
