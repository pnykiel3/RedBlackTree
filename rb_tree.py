"""Red Black Tree Implementation"""
from graphviz import Digraph

class Node:
    """
    Represents a node in a tree structure, with attributes for value, color, and
    references to its parent, left child, and right child nodes.
    """
    def __init__(self, value, color='red'):
        self.value = value
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

    def grandparent(self):
        """
        Determines and returns the grandparent of the current node.

        The method checks if the `parent` attribute of the current node exists.
        If it does not exist, the function returns `None`. Otherwise, the grandparent
        of the current node is accessed via the `parent` attribute of the `parent`.

        :return: The grandparent of the current node, or `None` if no parent exists at
                 any level.
        """
        if self.parent is None:
            return None
        return self.parent.parent

    def sibling(self):
        """
        Determines the sibling of the current node in a binary tree.

        If the current node has a parent node, it checks whether the current node is
        the left child or the right child of the parent and returns the respective
        sibling node. If there is no parent, it returns None.

        :return: The sibling node of the current node if it exists, otherwise None.
        """
        if self.parent is None:
            return None
        if self == self.parent.left:
            return self.parent.right
        return self.parent.left

    def uncle(self):
        """
        Determines the uncle of the current node in a tree structure. The uncle is the
        sibling of the parent node. If the parent node does not exist, the method
        returns None.

        :return: The uncle node if it exists, or None if the parent does not exist.
        """
        if self.parent is None:
            return None
        return self.parent.sibling()


class RBTree:
    """
    Red Black Tree implementation.
    """

    def __init__(self):
        self.root = None

    def insert(self, value):
        """
        Inserts a new value into the red-black tree by creating a new node and placing it
        at the appropriate position within the tree. If the tree is empty, the new node
        becomes the root and its color is set to black. If the value to be inserted is
        already present in the tree, it will not be inserted. After a successful insertion,
        the red-black tree properties are restored through rebalancing.

        :param value: The value to be inserted into the tree.
        :return: None
        """
        new = Node(value)
        if self.root is None:
            self.root = new
            self.root.color = 'black'
        else:
            # Attempt to insert the new node
            inserted = self.__insert_node(self.root, new)

            # Only apply fix if the node was actually inserted (not a duplicate)
            if inserted:
                self.__fix_insert(new)
        print(f"Inserted {value} into the tree.")

    def __insert_node(self, old, new):
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
            return self.__insert_node(old.left, new)

        if old.right is None:
            old.right = new
            new.parent = old
            return True
        return self.__insert_node(old.right, new)

    def __fix_insert(self, node):
        """
        Fixes the red-black tree property violations after an insertion operation.

        This function ensures that the red-black tree invariants are maintained
        following an insertion which might violate these properties. The algorithm
        corrects the tree by appropriately recoloring and performing rotations when
        necessary. It addresses three distinct cases for violations involving the
        node's uncle being red, the node being on the same side as its uncle, or
        opposite. Additionally, it guarantees that the root of the tree remains black.

        :param node: The newly inserted node in the red-black tree which may cause
                     violations in tree properties.
        :return: None
        """
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
                        self.__left_rotate(node)
                    node.parent.color = 'black'  # Case 3
                    grandparent.color = 'red'
                    self.__right_rotate(grandparent)
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
                        self.__right_rotate(node)
                    node.parent.color = 'black'  # Case 3
                    grandparent.color = 'red'
                    self.__left_rotate(grandparent)
        self.root.color = 'black'

    def delete(self, value):
        """
        Deletes a value from the binary search tree. If the value is not present in the
        tree, it prints a message indicating that the value was not found. When the
        value is found, it performs a deletion process to maintain the structure of
        the tree, then confirms the deletion through a message.

        :param value: The value to be deleted from the binary search tree.
        :return: None
        """
        node = self.search(value)
        if node is None:
            print(f"Value {value} not found in the tree.")
            return

        # Perform standard BST deletion
        self.__delete_node(node)
        print(f"Deleted {value} from the tree.")

    def __delete_node(self, node):
        """
        Deletes a node from the tree, replacing it appropriately and maintaining tree
        balance and properties. If the node to delete has two children, its in-order
        successor is found and replaces it. Otherwise, the node is replaced with its
        single child or removed if it’s a leaf. Fixes are applied if necessary to resolve
        color and structural imbalances caused by deletion.

        :param node: The node to be deleted from the tree.
        :return: None
        """
        # Node to replace the current node
        if node.left and node.right:
            # Find the successor
            successor = self.minimum(node.right)
            node.value = successor.value
            node = successor

        child = node.left if node.left else node.right

        # Remove node and replace it with child
        if child:
            self.__replace_node(node, child)
            if node.color == 'black':
                self.__fix_delete(child)
        elif node.color == 'black':
            # Fix double-black case
            self.__fix_delete(node)
            self.__replace_node(node, None)
        else:
            self.__replace_node(node, None)

    def __replace_node(self, node, child):
        """
        Replaces a node in the binary tree with its child. This method updates the
        parent-child relationship of both the node being replaced and its child
        if applicable. If the node to be replaced is the root of the tree, the
        root reference is updated.

        :param node: The node to be replaced
        :param child: The child node that will replace the original node
        :return: None
        """
        if node.parent is None:
            self.root = child
        else:
            if node == node.parent.left:
                node.parent.left = child
            else:
                node.parent.right = child
        if child:
            child.parent = node.parent

    def __fix_delete(self, node):
        """
        Fixes the red-black tree node properties during the delete operation.

        This method ensures that the red-black tree properties are maintained after
        removal of a node, by performing the necessary rotations and color adjustments.
        The function considers whether the node is a left or right child and takes
        appropriate actions based on the sibling properties such as its color and
        the color of its children.

        :param node: Node to be fixed after delete operation.
        :return: None
        """
        while node != self.root and node.color == 'black':
            if node.parent is None:
                break
            if node == node.parent.left:
                sibling = node.parent.right
                if sibling.color == 'red':
                    sibling.color = 'black'
                    node.parent.color = 'red'
                    self.__left_rotate(node.parent)
                    sibling = node.parent.right
                if (not sibling.left or sibling.left.color == 'black') and \
                        (not sibling.right or sibling.right.color == 'black'):
                    sibling.color = 'red'
                    node = node.parent
                else:
                    if not sibling.right or sibling.right.color == 'black':
                        sibling.left.color = 'black'
                        sibling.color = 'red'
                        self.__right_rotate(sibling)
                        sibling = node.parent.right
                    sibling.color = node.parent.color
                    node.parent.color = 'black'
                    sibling.right.color = 'black'
                    self.__left_rotate(node.parent)
                    node = self.root
            else:
                sibling = node.parent.left
                if sibling.color == 'red':
                    sibling.color = 'black'
                    node.parent.color = 'red'
                    self.__right_rotate(node.parent)
                    sibling = node.parent.left
                if (not sibling.left or sibling.left.color == 'black') and \
                        (not sibling.right or sibling.right.color == 'black'):
                    sibling.color = 'red'
                    node = node.parent
                else:
                    if not sibling.left or sibling.left.color == 'black':
                        sibling.right.color = 'black'
                        sibling.color = 'red'
                        self.__left_rotate(sibling)
                        sibling = node.parent.left
                    sibling.color = node.parent.color
                    node.parent.color = 'black'
                    sibling.left.color = 'black'
                    self.__right_rotate(node.parent)
                    node = self.root
        node.color = 'black'

    def __right_rotate(self, node):
        """
        Performs a right rotation on the given node in a binary tree. This rotation updates
        the relationships between the node, its left child, and the parent nodes of both,
        restructuring the subtree to maintain proper tree properties. This method assumes
        the node has a left child, otherwise the operation cannot properly be carried out.

        :param node: The node on which the right rotation will be performed.
        :return: None
        """
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

    def __left_rotate(self, node):
        """
        Performs a left rotation on the given node within a binary tree. Updates the
        references and relationships between the node, its parent, and its right child
        to enforce the properties of a left rotation. This operation rebalances the
        tree structure around the specified node.

        :param node: The node to perform the left rotation on.
                     The node must have a non-null right child.
        :return: None
        """
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
        :param value: Value to be found
        :return: The node if found, or None if not found.
        """
        current = self.root  # Start from the root
        while current:
            if current.value == value:  # Node found
                print(f"Value {value} found in the tree.")
                return current
            if value < current.value:  # Search in the left subtree
                current = current.left
            else:  # Search in the right subtree
                current = current.right
        print(f"Value {value} not found in the tree.")
        return None  # Value not found in the tree

    def minimum(self, node=None):
        """
        Finds the minimum value node in a binary search tree starting from the given node.

        This method traverses the binary search tree to find the node with the smallest
        value. It begins at the specified node or defaults to the tree's root if no
        node is provided. The traversal continues down the left subtree until the
        leftmost node is reached, which has the minimum value in the tree/subtree
        being considered.

        :param node: The starting node for the search. If not provided, it will default
            to the root of the binary search tree.
        :return: The node containing the minimum value in the subtree rooted at the
            given node.
        """
        if node is None:
            node = self.root
        while node.left:
            node = node.left
        return node

    def maximum(self, node=None):
        """
        Finds the maximum value node in a binary search tree.

        This method traverses the binary search tree starting from the specified
        node (or from the root if no node is specified) to find and return the
        node with the maximum value. The maximum value node is located by moving
        along the right child nodes until the rightmost node is found.

        :param node: Node to begin the search from. Defaults to the root node if not specified.
        :return: The node containing the maximum value in the binary search tree.
        """
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

        :param node: The starting node to calculate the height from.
                     If None, the root of the tree is used. Defaults to None.
        :param _root_call: Internal flag to distinguish between the initial
                           function call and recursive calls. Should not
                           be modified by users. Defaults to True.
        :return: The height of the tree.
        """
        if _root_call and node is None:
            node = self.root  # Start from the root if no node is specified

        if node is None:  # Height of an empty tree or subtree
            return -1

        left_height = self.height(node.left, False)
        right_height = self.height(node.right, False)
        return max(left_height, right_height) + 1

    def count_nodes(self, node=None, _root_call=True):
        """
        Counts the total number of nodes in a binary tree starting from a given node. If no node
        is specified, the count begins from the root of the tree.

        This method computes the size of the binary tree through a recursive traversal,
        evaluating the subtrees of the given node (or root node by default) and summing
        their respective node counts. If the tree is empty, the result is zero.

        :param node: The starting node for the count. If not specified, defaults to the root
            node of the tree (assumed to be `self.root` within the method implementation).
        :param _root_call: Internal parameter indicating whether this is the first call
            to the method. It is used internally to determine correct behavior when no
            explicit `node` is provided. Defaults to True.
        :return: Total count of nodes present in the subtree starting from `node`, or in
            the entire tree if `node` is None upon the first call.
        """
        if _root_call and node is None:
            node = self.root  # Start from the root if no node is specified
        if node is None:
            # Number of nodes in an empty tree
            return 0
        return 1 + self.count_nodes(node.left, False) + self.count_nodes(node.right, False)

    def clear(self):
        """
        Clears the tree by removing all its nodes and resetting its root to None.

        This method effectively deletes all the nodes in the tree. The tree's root
        will be set to None, and any previously stored data in the tree will be made
        eligible for garbage collection by Python's garbage collector.

        :return: None
        """
        self.root = None  # Python garbage collector deletes unused objects
        print("Tree cleared.")

    def successor(self, node):
        """
        Find the successor of a given node in the Red-Black Tree.
        The successor of a node is the node with the smallest key
        greater than the key of the given node.

        :param node: The node for which the successor is to be found.
        :return: The successor node if it exists, otherwise None.
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

        :param node: The node for which the predecessor is to be found.
        return: The predecessor node if it exists, otherwise None.
        """

        if node.left:
            return self.maximum(node.left)
        old = node
        while old.parent and old == old.parent.left:
            old = old.parent
        return old.parent

    def preorder(self):
        """
        Performs a preorder traversal on a binary tree, starting from the root node.
        Visits the root node first, followed by visiting the left subtree and then
        the right subtree. The values of the visited nodes are printed in sequence.

        :return: None
        """

        def __traverse(node):
            if not node:
                return
            print(node.value, end=' ')
            __traverse(node.left)
            __traverse(node.right)

        __traverse(self.root)
        print()

    def postorder(self):
        """
        Performs a post-order traversal of a binary tree.

        The post-order traversal visits nodes in the following order:
        1. Traverse the left subtree.
        2. Traverse the right subtree.
        3. Visit the root node.

        The method prints the values of the nodes in post-order sequence.

        :return: None
        """

        def __traverse(node):
            if not node:
                return
            __traverse(node.left)
            __traverse(node.right)
            print(node.value, end=' ')

        __traverse(self.root)
        print()

    def inorder(self):
        """
        Traverse a binary search tree (BST) in inorder fashion and print the
        values of each node sequentially. Inorder traversal visits the nodes
        in ascending order of their values in a BST. The traversal starts from
        the smallest node and proceeds to each successive node according to
        their order in the tree.

        :return: None
        """
        node = self.minimum()
        while node:
            print(node.value, end=' ')
            node = self.successor(node)
        print()

    def visualize(self, filename="red_black_tree"):
        """
        Generates a visual representation of a Red-Black Tree as a graph and outputs
        it as a PNG image file. The graph displays nodes with colors representing
        corresponding Red-Black Tree node properties (red for red nodes and black for
        black nodes). It also establishes edges between nodes to reflect the tree
        structure. Renders the graph using Graphviz.

        :param filename: The name of the output PNG file where the tree visualization
                         will be saved. Defaults to "red_black_tree".
        :return: The path of the rendered PNG file.
        """

        def __add_edges(graph, node):
            if not node:
                return
            color = "black" if node.color == "black" else "red"
            graph.node(str(node.value), str(node.value),
                       fillcolor=color, style="filled", fontcolor="white")
            if node.left:
                graph.edge(str(node.value), str(node.left.value))
                __add_edges(graph, node.left)
            if node.right:
                graph.edge(str(node.value), str(node.right.value))
                __add_edges(graph, node.right)

        graph = Digraph(comment="Red-Black Tree")
        graph.attr("node", shape="circle", fontcolor="white", style="filled")
        if self.root:
            __add_edges(graph, self.root)

        # Render the graph and save it as a PNG file
        graph.render(filename, format="png", cleanup=True)
        graph.view()

    def is_valid(self):
        """
        Validates whether the current tree satisfies Red-Black Tree properties.
        :return: True if valid, False otherwise.
        """

        def __check_properties(node):
            """
            Check if the tree rooted at the given node satisfies Red-Black Tree properties:
            1. A node is either red or black.
            2. The root is always black.
            3. Red nodes must have black children (no two consecutive red nodes).
            4. Every path from a node to its descendant NULL nodes
               must have the same number of black nodes.

            :param node: The current node to validate.

            Returns:
                (int, bool): A tuple containing the black height of the subtree
                and a boolean indicating whether the subtree is valid.
            """
            if node is None:  # Base case: Every NULL leaf has black height 1
                return 1, True

            left_black_height, left_valid = __check_properties(node.left)
            right_black_height, right_valid = __check_properties(node.right)

            # Check for both subtrees validity
            if not left_valid or not right_valid:
                return 0, False

            # Rule 4: Both sides must have the same black height
            if left_black_height != right_black_height:
                return 0, False

            # Rule 3: Red nodes cannot have red children
            if node.color == "red":
                if ((node.left and node.left.color == "red")
                    or (node.right and node.right.color == "red")):
                    return 0, False

            # Increment the black height for black nodes
            return (left_black_height + 1 if node.color == "black" else left_black_height), True

        # Rule 2: The root must be black
        if self.root and self.root.color != "black":
            return False

        # Validate all other properties
        _, is_valid_tree = __check_properties(self.root)
        return is_valid_tree


# Basic test
if __name__ == "__main__":
    # Create an example Red-Black Tree
    tree = RBTree()
    values = [20, 15, 10, 25, 30, 5, 35, 1]

    # Insert values into the tree
    print("Inserting values into the Red-Black Tree:")
    for v in values:
        tree.insert(v)

    # Visualize the tree
    print("\nVisualizing the tree after insertions:")
    tree.visualize()

    # Additionally, print traversal results
    print("\nPreorder Traversal:")
    tree.preorder()

    print("\nPostorder Traversal:")
    tree.postorder()

    print("\nInorder Traversal:")
    tree.inorder()
