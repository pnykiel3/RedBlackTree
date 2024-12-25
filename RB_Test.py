import unittest

from RB_Tree import RBTree


class TestRBTree(unittest.TestCase):
    def setUp(self):
        """ Set up a new Red-Black Tree instance before each test """
        self.tree = RBTree()
        self.values = [20, 15, 10, 25, 30, 5, 35, 1]  # Values for testing

    def populate_tree(self):
        """ Helper method to insert predefined values into the tree. """
        for value in self.values:
            self.tree.insert(value)

    def test_insert_and_search(self):
        """ Test the insert and search methods """
        self.populate_tree()

        # Verify each value can be searched
        for value in self.values:
            node = self.tree.search(value)
            self.assertIsNotNone(node, f"Value {value} should be present in the tree")
            self.assertEqual(node.value, value, f"Search returned incorrect value for {value}")

        # Test searching for a missing value
        self.assertIsNone(self.tree.search(100), "The value 100 should not exist in the tree")

    def test_minimum_and_maximum(self):
        """ Test the minimum and maximum methods """
        self.populate_tree()

        # Verify the minimum value
        min_node = self.tree.minimum()
        self.assertIsNotNone(min_node)
        self.assertEqual(min_node.value, 1, "The minimum value should be 1")

        # Verify the maximum value
        max_node = self.tree.maximum()
        self.assertIsNotNone(max_node)
        self.assertEqual(max_node.value, 35, "The maximum value should be 35")

    def test_successor_and_predecessor(self):
        """ Test the successor and predecessor methods """
        self.populate_tree()

        node_10 = self.tree.search(10)
        self.assertIsNotNone(node_10)
        successor = self.tree.successor(node_10)
        self.assertEqual(successor.value, 15, "Successor of 10 should be 15")

        node_30 = self.tree.search(30)
        self.assertIsNotNone(node_30)
        predecessor = self.tree.predecessor(node_30)
        self.assertEqual(predecessor.value, 25, "Predecessor of 30 should be 25")

    def test_height(self):
        """ Test the height method """
        self.assertEqual(self.tree.height(), -1, "Height of an empty tree should be -1")

        self.populate_tree()
        height = self.tree.height()
        self.assertGreater(height, 0, "Height of a populated tree should be positive")

    def test_count_nodes(self):
        """ Test the count_nodes method """
        self.assertEqual(self.tree.count_nodes(), 0, "Empty tree should have 0 nodes")

        self.populate_tree()
        self.assertEqual(self.tree.count_nodes(), len(self.values),
                         f"Tree should have {len(self.values)} nodes after insertion")

    def test_preorder_traversal(self):
        """ Test the preorder traversal method """
        self.populate_tree()
        print("\nPreorder Traversal:")
        self.tree.preorder()  # self check: Ensure values are printed in correct traversal order

    def test_inorder_traversal(self):
        """ Test the inorder traversal method """
        self.populate_tree()
        print("\nInorder Traversal:")
        self.tree.inorder()  # Primitive check: Ensure values are printed in sorted order

    def test_postorder_traversal(self):
        """ Test the postorder traversal method """
        self.populate_tree()
        print("\nPostorder Traversal:")
        self.tree.postorder()  # Primitive check: Ensure values are printed in correct postorder

    def test_clear_tree(self):
        """ Test the clear method """
        self.populate_tree()
        self.tree.clear()
        self.assertIsNone(self.tree.root, "Tree root should be None after clearing")
        self.assertEqual(self.tree.count_nodes(), 0, "Tree should have 0 nodes after clearing")

    def test_visualize(self):
        """ Test the visualize method to ensure graph generation works without errors """
        self.populate_tree()
        self.tree.visualize("rb_tree_test")
        # Ensure visualization is generated (manual verification required)


if __name__ == "__main__":
    unittest.main()