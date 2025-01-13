""" Red Black Tree Unit Tests"""
from rb_tree import RBTree


def set_up():
    """ Set up a new Red-Black Tree instance before each test """
    tree = RBTree()
    values = [20, 15, 10, 25, 30, 5, 35, 1]  # Values for testing
    add_values(tree, values)
    return tree

def add_values(tree, values):
    """ Insert a list of values into the given Red-Black Tree. """
    for value in values:
        tree.insert(value)


def test_is_valid():
    """ Test the validity of the Red-Black Tree """
    tree = set_up()
    assert tree.root.value == 15
    assert tree.root.color == "black"
    assert tree.root.left.value == 5
    assert tree.root.left.color == "black"
    assert tree.root.left.left.value == 1
    assert tree.root.left.left.color == "red"
    assert tree.root.left.right.value == 10
    assert tree.root.left.right.color == "red"
    assert tree.root.right.value == 25
    assert tree.root.right.color == "red"
    assert tree.root.right.left.value == 20
    assert tree.root.right.left.color == "black"
    assert tree.root.right.right.value == 30
    assert tree.root.right.right.color == "black"
    assert tree.root.right.right.right.value == 35
    assert tree.root.right.right.right.color == "red"
    assert tree.is_valid() is True, "Tree is invalid after setup"
    add_values(tree, [2025, 1410, 966, 1918])
    assert tree.root.value == 25
    assert tree.root.color == "black"
    assert tree.root.left.value == 15
    assert tree.root.left.color == "black"
    assert tree.root.left.left.value == 5
    assert tree.root.left.left.color == "black"
    assert tree.root.left.left.left.value == 1
    assert tree.root.left.left.left.color == "red"
    assert tree.root.left.left.right.value == 10
    assert tree.root.left.left.right.color == "red"
    assert tree.root.left.right.value == 20
    assert tree.root.left.right.color == "black"
    assert tree.root.right.value == 35
    assert tree.root.right.color == "black"
    assert tree.root.right.left.value == 30
    assert tree.root.right.left.color == "black"
    assert tree.root.right.right.value == 1410
    assert tree.root.right.right.color == "red"
    assert tree.root.right.right.left.value == 966
    assert tree.root.right.right.left.color == "black"
    assert tree.root.right.right.right.value == 2025
    assert tree.root.right.right.right.color == "black"
    assert tree.root.right.right.right.left.value == 1918
    assert tree.root.right.right.right.left.color == "red"

def test_search():
    """ Test the search method """
    tree = set_up()
    assert tree.search(10) is not None
    assert tree.search(100) is None
    assert tree.search(1) is not None
    assert tree.search(39) is None
    assert tree.search(15) is not None
    assert tree.search(25) is not None
    assert tree.search(2025) is None
    assert tree.search(0) is None

def test_insert_and_traversal(capsys):
    """ Test the insert and traversal (inorder, preorder, postorder) methods """
    tree = set_up()
    add_values(tree, [100, -5, 312, 511, 2, 8, 16, 100])
    assert tree.is_valid() is True

    # Expected results
    expected_inorder = "-5 1 2 5 8 10 15 16 20 25 30 35 100 312 511 \n"
    expected_preorder = "15 5 1 -5 2 10 8 25 20 16 35 30 312 100 511 \n"
    expected_postorder = "-5 2 1 8 10 5 16 20 30 100 511 312 35 25 15 \n"

    # Test Inorder
    _ = capsys.readouterr() # Clear output
    tree.inorder()
    captured = capsys.readouterr()
    assert captured.out == expected_inorder, f"Inorder failed: {captured.out}"

    # Test Preorder
    _ = capsys.readouterr() # Clear output
    tree.preorder()
    captured = capsys.readouterr()
    assert captured.out == expected_preorder, f"Preorder failed: {captured.out}"

    # Test Postorder
    _ = capsys.readouterr() # Clear output
    tree.postorder()
    captured = capsys.readouterr()
    assert captured.out == expected_postorder, f"Postorder failed: {captured.out}"

def test_delete():
    """ Test the delete method """
    tree = set_up()
    add_values(tree, [98, -2, 0, 8, 55, 32, 98, 123, -1, -9])
    assert tree.is_valid() is True, "Tree is invalid after setup"
    tree.delete(98)
    tree.delete(15)
    tree.delete(123)
    tree.delete(22222)
    tree.delete(30)
    assert tree.is_valid() is True, "Tree is invalid after deletion"
    assert tree.search(98) is None, "98 should have been deleted"
    assert tree.search(15) is None, "15 should have been deleted"
    assert tree.search(123) is None, "123 should have been deleted"
    assert tree.search(22222) is None, "22222 should have been deleted"
    assert tree.search(30) is None, "30 should have been deleted"

def test_minimum_and_maximum():
    """ Test the minimum and maximum methods """
    tree = set_up()
    assert tree.is_valid() is True, "Tree is invalid after setup"
    assert tree.minimum().value == 1, f"minimum() failed: Expected 1, got {tree.minimum().value}"
    assert tree.maximum().value == 35, f"maximum() failed: Expected 35, got {tree.maximum().value}"
    tree.delete(1)
    assert tree.is_valid() is True, "Tree is invalid after deletion"
    assert tree.minimum().value == 5, f"minimum() failed: Expected 5, got {tree.minimum().value}"
    tree.insert(44)
    assert tree.is_valid() is True, "Tree is invalid after insertion"
    assert tree.maximum().value == 44, f"maximum() failed: Expected 44, got {tree.maximum().value}"

def test_successor_and_predecessor():
    """ Test the successor and predecessor methods """
    tree = set_up()
    assert tree.is_valid() is True, "Tree is invalid after setup"
    assert tree.successor(tree.minimum()).value == 5, \
        f"successor() failed: Expected 5, got {tree.successor(tree.minimum()).value}"
    assert tree.predecessor(tree.maximum()).value == 30, \
        f"predecessor() failed: Expected 30, got {tree.predecessor(tree.maximum()).value}"
    tree.delete(1)
    assert tree.is_valid() is True, "Tree is invalid after deletion"
    assert tree.successor(tree.minimum()).value == 10, \
        f"successor() failed: Expected 10, got {tree.successor(tree.minimum()).value}"
    tree.insert(44)
    assert tree.is_valid() is True, "Tree is invalid after insertion"
    assert tree.predecessor(tree.maximum()).value == 35, \
        f"predecessor() failed: Expected 35, got {tree.predecessor(tree.maximum()).value}"

def test_height():
    """ Test the height method """
    tree = set_up()
    assert tree.is_valid() is True, "Tree is invalid after setup"
    assert tree.height() == 3, f"height() failed: Expected 3, got {tree.height()}"
    tree.delete(30)
    tree.delete(15)
    assert tree.is_valid() is True, "Tree is invalid after deletion"
    assert tree.height() == 2, f"height() failed: Expected 2, got {tree.height()}"
    tree.insert(100)
    tree.insert(200)
    tree.insert(500)
    assert tree.is_valid() is True, "Tree is invalid after insertion"
    assert tree.height() == 3, f"height() failed: Expected 3, got {tree.height()}"

def test_count_nodes():
    """ Test the count_nodes method """
    tree = set_up()
    assert tree.is_valid() is True, "Tree is invalid after setup"
    assert tree.count_nodes() == 8, f"count_nodes() failed: Expected 8, got {tree.count_nodes()}"
    assert tree.count_nodes(tree.search(5), False) == 3, \
        f"count_nodes() failed: Expected 3, got {tree.count_nodes(5)}"
    assert tree.count_nodes(tree.search(25), False) == 4, \
        f"count_nodes() failed: Expected 4, got {tree.count_nodes(25)}"
    assert tree.count_nodes(tree.search(1001), False) == 0, \
        f"count_nodes() failed: Expected 0, got {tree.count_nodes(100)}"
    assert tree.count_nodes(tree.search(35), False) == 1, \
        f"count_nodes() failed: Expected 1, got {tree.count_nodes(35)}"
    tree.delete(30)
    tree.delete(15)
    assert tree.is_valid() is True, "Tree is invalid after deletion"
    assert tree.count_nodes() == 6, f"count_nodes() failed: Expected 6, got {tree.count_nodes()}"

def test_clear():
    """ Test the clear method """
    tree = set_up()
    assert tree.is_valid() is True, "Tree is invalid after setup"
    tree.clear()
    assert tree.is_valid() is True, "Tree is invalid after clear"
    assert tree.root is None, "Tree should be empty after clear"
    assert tree.count_nodes() == 0, "Tree should have 0 nodes after clear"
