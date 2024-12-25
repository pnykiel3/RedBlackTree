import os
import unittest
from graphviz import Digraph


class Node:
    def __init__(self, value, color='red'):
        self.value = value
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

    def grandparent(self):
        if self.parent is None:
            return None
        return self.parent.parent

    def sibling(self):
        if self.parent is None:
            return None
        if self == self.parent.left:
            return self.parent.right
        return self.parent.left

    def uncle(self):
        if self.parent is None:
            return None
        return self.parent.sibling


class RBTree:

    def __init__(self):
        self.root = None

    def insert(self, value):
        new = Node(value)
        if self.root is None:
            self.root = new
            self.root.color = 'black'
        else:
            # Attempt to insert the new node
            inserted = self.insert_node(self.root, new)

            # Only apply fix if the node was actually inserted (not a duplicate)
            if inserted:
                self.fix(new)


    def insert_node(self, old, new):
        """
        Recursively insert a node into the BST tree.
        Tree needs to be fixed after insertion to maintain the properties of the Red-Black Tree.
        :param old: potential parent node
        :param new: the node to insert
        :return: True if the node was inserted, False if it was a duplicate
        """
        if new.value == old.value:
            # Ignore duplicates
            return False
        if new.value < old.value:
            if old.left is None:
                old.left = new
                new.parent = old
                return True
            else:
                return self.insert_node(old.left, new)
        else:
            if old.right is None:
                old.right = new
                new.parent = old
                return True
            else:
                return self.insert_node(old.right, new)


    def fix(self, node):
        while node != self.root and node.parent.color == 'red':
            grandparent = node.grandparent()
            if node.parent == grandparent.left:
                uncle = grandparent.right
                if uncle and uncle.color == 'red':  # Case 1
                    node.parent.color = 'black'
                    uncle.color = 'black'
                    grandparent.color = 'red'
                    node = grandparent
                else:
                    if node == node.parent.right:  # Case 2
                        node = node.parent
                        self.left_rotate(node)
                    node.parent.color = 'black'  # Case 3
                    grandparent.color = 'red'
                    self.right_rotate(grandparent)
            else:
                uncle = grandparent.left
                if uncle and uncle.color == 'red':  # Case 1
                    node.parent.color = 'black'
                    uncle.color = 'black'
                    grandparent.color = 'red'
                    node = grandparent
                else:
                    if node == node.parent.left:  # Case 2
                        node = node.parent
                        self.right_rotate(node)
                    node.parent.color = 'black'  # Case 3
                    grandparent.color = 'red'
                    self.left_rotate(grandparent)
        self.root.color = 'black'

    def right_rotate(self, node):
        old_left = node.left
        node.left = old_left.right
        if old_left.right:
            old_left.right.parent = node
        old_left.parent = node.parent
        if node.parent is None:
            self.root = old_left
        elif node == node.parent.right:
            node.parent.right = old_left
        else:
            node.parent.left = old_left
        old_left.right = node
        node.parent = old_left

    def left_rotate(self, node):
        old_right = node.right
        node.right = old_right.left
        if old_right.left:
            old_right.left.parent = node
        old_right.parent = node.parent
        if node.parent is None:
            self.root = old_right
        elif node == node.parent.left:
            node.parent.left = old_right
        else:
            node.parent.right = old_right
        old_right.left = node
        node.parent = old_right

    def search(self, value):
        """
        Search the tree for a node with the given value.
        Return the node if found, or None if not found.
        """
        current = self.root  # Start from the root
        while current:
            if current.value == value:  # Node found
                return current
            elif value < current.value:  # Search in the left subtree
                current = current.left
            else:  # Search in the right subtree
                current = current.right
        return None  # Value not found in the tree


    def minimum(self, node = None):
        if node is None:
            node = self.root
        while node.left:
            node = node.left
        return node


    def maximum(self, node = None):
        if node is None:
            node = self.root
        while node.right:
            node = node.right
        return node

    def height(self, node=None, _root_call=True):
        """
        Calculate the height of the tree starting from the given node.

        The height of a node is the number of edges on the longest path from the node to a leaf.
        The height of an empty tree is defined as -1.

        Args:
            node (Node, optional): The starting node to calculate the height from.
                                   If None, the root of the tree is used. Defaults to None.
            _root_call (bool, optional): Internal flag to distinguish between the initial
                                         function call and recursive calls. Should not
                                         be modified by users. Defaults to True.

        Returns:
            int: The height of the tree.
        """
        if _root_call and node is None:
            node = self.root  # Start from the root if no node is specified

        if node is None:  # Height of an empty tree or subtree
            return -1

        left_height = self.height(node.left, False)
        right_height = self.height(node.right, False)
        return max(left_height, right_height) + 1

    def count_nodes(self, node = None, _root_call=True):
        if _root_call and node is None:
            node = self.root  # Start from the root if no node is specified
        if node is None:
            # Number of nodes in an empty tree
            return 0
        return 1 + self.count_nodes(node.left, False) + self.count_nodes(node.right, False)


    def clear(self):
        def remove_refs(node):
            if node:
                remove_refs(node.left)
                remove_refs(node.right)
                node.left = node.right = node.parent = None

        remove_refs(self.root)
        self.root = None

    def successor(self, node):
        """
            Find the successor of a given node in the Red-Black Tree.
            The successor of a node is the node with the smallest key
            greater than the key of the given node.
           Args:
                node (Node): The node for which the successor is to be found.
            Returns:
                Node or None: The successor node if it exists, otherwise None.
            """
        if node.right:
            return self.minimum(node.right)
        old = node
        while old.parent and old == old.parent.right:
            old = old.parent
        return old.parent


    def predecessor(self, node):
        """
        Find the predecessor of a given node in the Red-Black Tree.
        The predecessor of a node is the node with the largest key
        smaller than the given node's key. If the left subtree of the
        given node exists, the predecessor is the maximum node in the
        left subtree. Otherwise, the predecessor is the nearest ancestor
        for which the given node is in the right subtree.
        Args:
            node (RBTreeNode): The node for which the predecessor is to be found.
        Returns:
            RBTreeNode or None: The predecessor node if it exists, otherwise None.
        """

        if node.left:
            return self.maximum(node.left)
        old = node
        while old.parent and old == old.parent.left:
            old = old.parent
        return old.parent


    def preorder(self):
        def traverse(node):
            if not node:
                return
            print(node.value, end=' ')
            traverse(node.left)
            traverse(node.right)

        traverse(self.root)
        print()



    def postorder(self):
        def traverse(node):
            if not node:
                return
            traverse(node.left)
            traverse(node.right)
            print(node.value, end=' ')
        traverse(self.root)
        print()


    def inorder(self):
        node = self.minimum()
        while node:
            print(node.value, end=' ')
            node = self.successor(node)
        print()


    def visualize(self, filename="red_black_tree"):
        def add_edges(graph, node):
            if not node:
                return
            color = "black" if node.color == "black" else "red"
            graph.node(str(node.value), str(node.value),
                       fillcolor=color, style="filled", fontcolor="white")
            if node.left:
                graph.edge(str(node.value), str(node.left.value))
                add_edges(graph, node.left)
            if node.right:
                graph.edge(str(node.value), str(node.right.value))
                add_edges(graph, node.right)

        graph = Digraph(comment="Red-Black Tree")
        graph.attr("node", shape="circle", fontcolor="white", style="filled")
        if self.root:
            add_edges(graph, self.root)

        # Render the graph and save it as a PNG file
        output_path = graph.render(filename, format="png", cleanup=True)

        # Automatically open the generated image
        try:
            os.system(f"xdg-open {output_path}")  # For Linux
        except Exception as e:
            print(f"Unable to open the file: {e}")



