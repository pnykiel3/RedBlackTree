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
        return self.parent.sibling()


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
                self.fix_insert(new)
        print(f"Inserted {value} into the tree.")


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


    def fix_insert(self, node):
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


    def delete(self, value):
        node = self.search(value)
        if node is None:
            print(f"Value {value} not found in the tree.")
            return

        # Perform standard BST deletion
        self.delete_node(node)
        print(f"Deleted {value} from the tree.")


    def delete_node(self, node):
        # Node to replace the current node
        if node.left and node.right:
            # Find the successor
            successor = self.minimum(node.right)
            node.value = successor.value
            node = successor

        child = node.left if node.left else node.right

        # Remove node and replace it with child
        if child:
            self.replace_node(node, child)
            if node.color == 'black':
                self.fix_delete(child)
        elif node.color == 'black':
            # Fix double-black case
            self.fix_delete(node)
            self.replace_node(node, None)
        else:
            self.replace_node(node, None)


    def replace_node(self, node, child):
        if node.parent is None:
            self.root = child
        else:
            if node == node.parent.left:
                node.parent.left = child
            else:
                node.parent.right = child
        if child:
            child.parent = node.parent


    def fix_delete(self, node):
        while node != self.root and node.color == 'black':
            if node.parent is None:
                break
            if node == node.parent.left:
                sibling = node.parent.right
                if sibling.color == 'red':
                    sibling.color = 'black'
                    node.parent.color = 'red'
                    self.left_rotate(node.parent)
                    sibling = node.parent.right
                if (not sibling.left or sibling.left.color == 'black') and \
                        (not sibling.right or sibling.right.color == 'black'):
                    sibling.color = 'red'
                    node = node.parent
                else:
                    if not sibling.right or sibling.right.color == 'black':
                        sibling.left.color = 'black'
                        sibling.color = 'red'
                        self.right_rotate(sibling)
                        sibling = node.parent.right
                    sibling.color = node.parent.color
                    node.parent.color = 'black'
                    sibling.right.color = 'black'
                    self.left_rotate(node.parent)
                    node = self.root
            else:
                sibling = node.parent.left
                if sibling.color == 'red':
                    sibling.color = 'black'
                    node.parent.color = 'red'
                    self.right_rotate(node.parent)
                    sibling = node.parent.left
                if (not sibling.left or sibling.left.color == 'black') and \
                        (not sibling.right or sibling.right.color == 'black'):
                    sibling.color = 'red'
                    node = node.parent
                else:
                    if not sibling.left or sibling.left.color == 'black':
                        sibling.right.color = 'black'
                        sibling.color = 'red'
                        self.left_rotate(sibling)
                        sibling = node.parent.left
                    sibling.color = node.parent.color
                    node.parent.color = 'black'
                    sibling.left.color = 'black'
                    self.right_rotate(node.parent)
                    node = self.root
        node.color = 'black'


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
                print(f"Value {value} found in the tree.")
                return current
            elif value < current.value:  # Search in the left subtree
                current = current.left
            else:  # Search in the right subtree
                current = current.right
        print(f"Value {value} not found in the tree.")
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
        self.root = None # Python garbage collector deletes unused objects
        print("Tree cleared.")


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
        graph.view()

    def is_valid(self):
        """
        Validates whether the current tree satisfies Red-Black Tree properties.
        Returns True if valid, False otherwise.
        """


        def check_properties(node):
            """
            Check if the tree rooted at the given node satisfies Red-Black Tree properties:
            1. A node is either red or black.
            2. The root is always black.
            3. Red nodes must have black children (no two consecutive red nodes).
            4. Every path from a node to its descendant NULL nodes must have the same number of black nodes.
    
            Args:
                node (Node): The current node to validate.
    
            Returns:
                (int, bool): A tuple containing the black height of the subtree and a boolean indicating
                whether the subtree is valid.
            """
            if node is None:  # Base case: Every NULL leaf has black height 1
                return 1, True
    
            left_black_height, left_valid = check_properties(node.left)
            right_black_height, right_valid = check_properties(node.right)
    
            # Check for both subtrees validity
            if not left_valid or not right_valid:
                return 0, False
    
            # Rule 4: Both sides must have the same black height
            if left_black_height != right_black_height:
                return 0, False
    
            # Rule 3: Red nodes cannot have red children
            if node.color == "red":
                if (node.left and node.left.color == "red") or (node.right and node.right.color == "red"):
                    return 0, False
    
            # Increment the black height for black nodes
            return (left_black_height + 1 if node.color == "black" else left_black_height), True
    
        # Rule 2: The root must be black
        if self.root and self.root.color != "black":
            return False
    
        # Validate all other properties
        _, is_valid_tree = check_properties(self.root)
        return is_valid_tree


if __name__ == "__main__":
    # Create an example Red-Black Tree
    tree = RBTree()
    values = [20, 15, 10, 25, 30, 5, 35, 1]

    # Insert values into the tree
    print("Inserting values into the Red-Black Tree:")
    for value in values:
        tree.insert(value)

    # Visualize the tree
    print("\nVisualizing the tree after insertions:")
    tree.visualize("rb_tree_test")

    # Additionally, print traversal results
    print("\nPreorder Traversal:")
    tree.preorder()

    print("\nPostorder Traversal:")
    tree.postorder()

    print("\nInorder Traversal:")
    tree.inorder()
