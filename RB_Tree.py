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
            self.insert_node(self.root, new)
            self.fix(new)


    def insert_node(self, old, new):
        """
        Recursively insert a node into the BST tree.
        Tree needs to be fixed after insertion to maintain the properties of the Red-Black Tree.
        :param old: potential parent node
        :param new: the node to insert
        """

        if new.value < old.value:
            if old.left is None:
                old.left = new
                new.parent = old
            else:
                self.insert_node(old.left, new)
        else:
            if old.right is None:
                old.right = new
                new.parent = old
            else:
                self.insert_node(old.right, new)



    def fix(self, node):

        while node != self.root and node.parent.color
