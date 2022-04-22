class Tree:
    """ Abstract base class representing a tree structure. """

    class Position:

        def __eq__(self, other):
            return NotImplementedError("")

        def __ne__(self, other):
            return not (self == other)

    def root(self):
        """
      returns the position of the root not. If the tree is empty it return None
    """
        return NotImplementedError("")

    def is_root(self, p):
        """
    returns True if the position is a root not, or False if it is not.
    """
        return self.root() == p

    def parent(self, p):
        """
      returns the position the parent of position p or None if p is root.
    """
        return NotImplementedError("")

    def num_children(self, p):
        """
      returns the number of children of position p.
    """
        return NotImplementedError("")

    def children(self, p):
        """
      returns an iterator of the children of position p.
    """
        return NotImplementedError("")

    def is_leaf(self, p):
        """
    returns True if position p does not have any children.
    """
        return self.num_children(p) == 0

    def __len__(self):
        """
      return the number of positions in the tree.
    """
        return NotImplementedError("")

    def is_empty(self):
        """
      returns True if the tree does not contain any positions.
    """
        return len(self) == 0

    def positions(self):
        """
      returns an iterator of all position of the tree.
    """
        return NotImplementedError("")


class BinaryTree(Tree):
    """ Abstract base  class representing a binary tree. """

    def left(self, p):
        """ returns the position of the left child of p or None if p has no child. """

        return NotImplementedError("")

    def right(self, p):
        """ returns the position of the right  child of p or None if p has no right child """

        return NotImplementedError("")

    def sibling(self, p):
        """ returns the position that represents the sibling of p, or None if p has not sibling. """
        parent = self.parent(p)
        if parent is None:
            return None
        if self.left(parent) == p:
            return self.right(parent)
        else:
            return self.right(parent)

    def children(self, p):
        """ Generate an iteration of children of postion p. """

        if self.left(p) is not None:
            yield self.left(p)

        if self.right(p) is not None:
            yield self.right(p)


class LinkedBinary(BinaryTree):
    class _Node:

        __slots__ = '_element', '_parent', '_left', '_right'

        def __init__(self, element, parent=None, left=None, right=None):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right

    class Position(BinaryTree.Position):

        def __init__(self, container, node):
            self._container = container
            self._node = node

        def element(self):
            return self._node._element

        def __eq__(self, other):
            """
        returns True if other is a position representing the same location.
      """
            return type(self) == type(other) and self._node is other._node

    def _validate(self, p):
        """ Raise error if p is not a valid position otherwise return the node at position p. """

        if not isinstance(p, self.Position):
            raise ValueError(" p is not instance not Position class. ")
        if p._container is not self:
            raise ValueError("p doesn't belong the this tree. ")
        if p._node._parent is p._node:
            raise ValueError("p is a deprecated node. ")
        return p._node

    def _make_position(self, node):
        """
      If it is a root node and the tree is empty, then node is None.
    """
        return self.Position(self, node) if node is not None else None

    def __init__(self):
        self._root = None
        self._size = 0

    def __len__(self):
        return self._size

    def root(self):
        """
      returns the position of the root node.
    """
        return self._make_position(self._root)

    def parent(self, p):
        """
      returns the position of the parent of p.
    """
        node = self._validate(p)
        return self._make_position(node._parent)

    def left(self, p):
        """"
      returns the position of the left child of p.
    """

        node = self._validate(p)

        return self._make_position(node._left)

    def right(self, p):

        """
      returns the position of the right child of p.

    """

        node = self._validate(p)

        return self._make_position(node._right)

    def num_children(self, p):
        """ returns the number of children of position p. """

        node = self._validate(p)

        return node._left is not None + node._right is not None

    def add_root(self, e):
        """
      creates a root for an empty tree and returns the position of that root; an error occurs if the tree is not empty.

    """

        if self._root is not None:
            raise ValueError(" The tree is not empty! ")
        self._size = 1
        self._root = self._Node(e)
        return self._make_position(self._root)

    def add_left(self, p, e):
        """
    Create a new node with element e, and make it the left child of position p.
    If p already has a left child, raise an error.

    return the position of the left child.
    """

        node = self._validate(p)

        if node._left is not None:
            raise ValueError("p already has a left child! ")
        self._size += 1
        node._left = self._Node(e, node)
        return self._make_position(node._left)

    def add_right(self, p, e):
        """
      Create a new node with element e, and make the it right child of position p.

      If p already has a right  child, raise an error.

      return the position of the right  child.
    """

        node = self._validate(p)

        if node._right is not None:
            raise ValueError("p already has right child! ")

        self._size += 1

        node._right = self._Node(e, node)

        return self._make_position(node._right)

    def replace(self, p, e):

        """
      Replace the element stored at position p with element e,
      and return the previously stored element.

    """

        node = self._validate(p)
        old_value = node._element
        node._element = e

        return old_value

    def delete(self, p):
        """
      Remove the node at position p, replacing it with its child.

      If p has two children, raise an error.

      return the element that have previously been stored.
    """

        node = self._validate(p)

        if self.num_children(p) == 2:
            raise ValueError("p has two children! ")

        if node._left is not None:
            child = node._left
        else:
            child = node._right

        if child is not None:
            child._parent = node._parent

        if node is self._root:
            self._root = child
        else:
            parent = node._parent

            if node is parent._left:
                parent._left = child
            else:
                parent._right = child
        self._size -= 1
        node._parent = node  # Convention for a deleted node.

        return node._element

    def attach(self, p, t1, t2):
        """
      Attach the trees t1 and t2 as the left and right subtrees of a leaf node p.

      Reset t1 and t2 to empty trees.

      Raise an error if p is not a leaf node.

    """
        node = self._validate(p)

        if not self.is_leaf(p):
            raise ValueError("p must be a leaf node! ")

        if not type(self) is type(t1) is type(t2):
            raise ValueError("All trees must be of the same type. ")

        self._size += len(t1) + len(t2)

        if not t1.is_empty():
            t1._root._parent = node
            node._left = t1._root
            t1._root = None
            t1._size = 0

        if not t2.is_empty():
            t2._root._parent = node
            node._right = t2._root
            t2._root = None
            t2._size = 0

    def __iter__(self):
        """
      Generate an iteration of all elements stored within tree T.
    """
        for p in self.positions():
            yield p.element()


t1 = LinkedBinary()
p = t1.add_root(1)
t1.add_left(p, 2)
p = t1.add_right(p, 3)
t1.add_left(p, 4)

print(t1.left(t1.right(t1.root())).element())
