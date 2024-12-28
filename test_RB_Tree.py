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

    def test_delete_leaf_node(self):
        """ Test deletion of a leaf node """
        self.populate_tree()

        self.tree.delete(5)  # 5 is a leaf node
        self.assertIsNone(self.tree.search(5), "Leaf node 5 should have been deleted")

        # Ensure all other values are intact
        for value in [20, 15, 25, 10, 30, 35]:
            self.assertIsNotNone(self.tree.search(value), f"Value {value} should still exist in the tree")

        # Verify tree remains a valid Red-Black Tree
        self.assertTrue(self.tree.is_valid(),
                        "Tree should still satisfy Red-Black properties after leaf deletion")

    def test_delete_node_with_one_child(self):
        """ Test deletion of a node with one child """
        self.populate_tree()

        self.tree.delete(30)  # 30 has one child (35)
        self.assertIsNone(self.tree.search(30), "Node 30 should have been deleted")
        self.assertIsNotNone(self.tree.search(35), "Node 35 should remain in the tree")

        # Verify tree remains valid
        self.assertTrue(self.tree.is_valid(),
                        "Tree should still satisfy Red-Black properties after deleting a node with one child")

    def test_delete_node_with_two_children(self):
        """ Test deletion of a node with two children """
        self.populate_tree()

        self.tree.delete(20)  # 20 has two children: 15 and 25
        self.assertIsNone(self.tree.search(20), "Node 20 should have been deleted")

        # Verify that the in-order successor or predecessor replaced the node correctly
        self.assertIsNotNone(self.tree.search(15), "Node 15 should remain")
        self.assertIsNotNone(self.tree.search(25), "Node 25 should remain")

        # Verify tree remains valid
        self.assertTrue(self.tree.is_valid(),
                        "Tree should still satisfy Red-Black properties after deleting a node with two children")

    def test_delete_root_node(self):
        """ Test deletion of the root node """
        self.populate_tree()

        self.tree.delete(20)  # Root node has two children
        self.assertIsNone(self.tree.search(20), "Root node 20 should have been deleted")

        # Ensure the tree has a new root and remains valid
        self.assertIsNotNone(self.tree.root, "Tree should have a new root after deletion of the old root")
        self.assertTrue(self.tree.is_valid(),
                        "Tree should satisfy Red-Black properties after root deletion")

    def test_delete_non_existent_node(self):
        """ Test deleting a node that doesn't exist """
        self.populate_tree()

        before_count = self.tree.count_nodes()
        self.tree.delete(100)  # Node 100 does not exist
        after_count = self.tree.count_nodes()

        self.assertEqual(before_count, after_count,
                         "Tree node count should not change when deleting a non-existent node")
        self.assertTrue(self.tree.is_valid(),
                        "Tree should remain valid after attempting to delete a non-existent node")

    def test_delete_last_node(self):
        """ Test deleting the last node in the tree """
        self.tree.insert(10)  # Single node
        self.tree.delete(10)  # Delete that single node

        self.assertIsNone(self.tree.root, "Root should be None after deleting the last remaining node")
        self.assertEqual(self.tree.count_nodes(), 0, "Tree should have 0 nodes after deleting the last node")
        self.assertTrue(self.tree.is_valid(), "Tree should remain valid after deleting the last node")

    def test_delete_empty_tree(self):
        """ Test deletion from an empty tree """
        self.tree.delete(10)  # Deleting from an empty tree should be a no-op
        self.assertIsNone(self.tree.root, "Root should still be None for an empty tree")
        self.assertEqual(self.tree.count_nodes(), 0, "Tree should still have 0 nodes for an empty tree")
        self.assertTrue(self.tree.is_valid(), "Empty tree should remain valid")

    def test_delete_multiple_values(self):
        """ Test deleting multiple nodes successively """
        self.populate_tree()

        # Delete values one by one
        for value in self.values:
            self.tree.delete(value)
            self.assertIsNone(self.tree.search(value), f"Node {value} should have been deleted")
            self.assertTrue(self.tree.is_valid(), f"Tree should remain valid after deleting {value}")

        # Ensure the tree is empty after all deletions
        self.assertIsNone(self.tree.root, "Tree should be empty after deleting all nodes")
        self.assertEqual(self.tree.count_nodes(), 0, "Tree should have 0 nodes after deleting all nodes")


if __name__ == "__main__":
    unittest.main()