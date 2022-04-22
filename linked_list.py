class LinkedQueue:
    """
        Implementation of queue data structure with singly linked list.
    """
    class _Node:

        __slots__ = "_element", "_next"

        def __init__(self, element, next):
            self._element = element
            self._next = next

    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    def __len__(self):
        return self._size

    def first(self):
        if self.is_empty():
            raise ValueError("Empty queue!")

        return self._head._element

    def is_empty(self):
        return len(self) == 0

    def enqueue(self, e):
        node = self._Node(e, None)
        if self.is_empty():
            self._head = node
        else:
            self._tail._next = node
        self._tail = node
        self._size += 1

    def dequeue(self):

        if self.is_empty():
            raise ValueError("You can't dequeue f")

        old_value = self._head._element
        self._head = self._head._next
        self._size -= 1

        if self.is_empty():
            self._tail = None

        return old_value


class LinkedStack:

    class _Node:
        __slots__ = "_element", "_next"

        def __init__(self, element, next):
            self._element = element
            self._next = next

    def __init__(self):
        self._head = None
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return len(self) == 0

    def top(self):
        if self.is_empty():
            raise ValueError("Empty stack!")
        return self._head._element

    def push(self, e):
        self._head = self._Node(e, self._head)
        self._size += 1

    def pop(self):
        if self.is_empty():
            raise ValueError("Empty stack!")
        value = self._head._element
        self._head = self._head._next
        self._size -= 1
        return value


class CircularLinkedList:
    """
        The implementation for a circular linked list.
    """
    pass


class DoublyLinkedList:
    """
        The implementation for a positional doubly linked list.
    """

    class _Node:
        __slots__ = "_element", "_prev", "_next"

        def __init__(self, element, prev, next):
            self._element = element
            self._prev = prev
            self._next = next

    class Position:

        def __init__(self, container, node):
            self._container = container
            self._node = node

        def __eq__(self, other):
            return type(self) == type(other) and self._node is other._node

        def __ne__(self, other):
            return not (self == other)

        def element(self):
            return self._node

        def __repr__(self):
            return "Position(container, node)"

    def _validate(self, p):
        if not isinstance(p, self.Position):
            raise ValueError(f"{p} must be instance of {self.Position}!")

        if p._container is not self:
            raise ValueError(f"{p} must be an instance of {self}!")

        if p._node._next is None:
            raise ValueError(f"{p} is a deprecated position!")

        return p._node

    def _make_position(self, node):
        if node is self._header or node is self._trailer:
            return None
        return self.Position(self, node)

    def __init__(self):
        self._header = self._Node(None, None, None)
        self._trailer = self._Node(None, None, None)
        self._header._next = self._trailer
        self._trailer._prev = self._header
        self._size = 0

    def __repr__(self):
        return "DoublyLinkedList"

    def __len__(self):

        return self._size

    def is_empty(self):
        return len(self) == 0

    def first(self):
        """
            Returns the position of the firste element or None if the list is empty.
        """

        return self._make_position(self._header._next)

    def last(self):
        """
            Returns the position of the last element or None if the list is empty.
        """

        return self._make_position(self._trailer._prev)

    def before(self, p):
        """
            Returns the position of the node that is before position p or None if p is first.
        """
        node = self._validate(p)
        return self._make_position(node._prev)

    def after(self, p):
        """
            Returns the position of the node that is after the position p or None if p is last.
        """
        node = self._validate(p)
        return self._make_position(node._next)

    def __iter__(self):
        """
            Generate an iteration of the nodes of the list.
        """
        cursor = self.first()
        while cursor is not None:
            yield cursor.element()
            cursor = self.after(cursor)

    def insert_between(self, e, predecessor, successor):
        """
            Inserts element e between predecessor and successor, and return the position of the new node.
        """
        node = self._Node(e, predecessor, successor)
        predecessor._next = node
        successor._prev = node
        self._size += 1
        return self._make_position(node)

    def insert_first(self, e):
        """
            Insert e at the front of the list, and return the position of that node.
        """
        return self.insert_between(e, self._header, self._header._next)

    def insert_last(self, e):

        """
            Insert e at the end of the list, and return the position of that node.
        """
        return self.insert_between(e, self._trailer, self._trailer._prev)

    def _delete_node(self, p):
        """
           Deletes node at position p, and returns the element.
        """
        node = self._validate(p)
        predecessor = node._prev
        successor = node._next
        predecessor._next = successor
        successor._prev = predecessor
        self._size -= 1
        element = node._element
        node._prev = node._element = node._next = None  # deleted node
        return element

    def delete_first(self):
        """
            Remove and return the first element of the list; raise an error if the list is empty.
        """
        if self.is_empty():
            raise ValueError("Empty List!")

        return self._delete_node(self._header._next)

    def delete_last(self):
        """
            Remove and return the last element of the list; raise an error if the list is empty.
        """
        if self.is_empty():
            raise ValueError("Empty List!")
        return self._delete_node(self._trailer._prev)
