class Stack:
    """Provides the base functionalities of a the stack data structure."""

    # Dunder methods

    def __init__(self) -> None:

        # The main stack list
        self._stack: list = []
        # Signifying the top of the stack (-1 means the stack is empty)
        self._size: int = -1

    def __str__(self) -> str:
        """The string format of the stack."""
        return str(f"length: {self._size}, {self._stack}")

    def __repr__(self) -> str:
        """The string representation for print and Jupyter."""
        return str(self._stack)

    # Properties

    @property
    def stack(self) -> list:
        """Returns the stack list."""
        return self._stack

    @property
    def size(self) -> int:
        """Returns the size of the stack (starts at -1 meaning the stack is emptyand goes up to the length -1)"""
        return self._size

    @property
    def top(self) -> object:
        """Returns the element at the top of the stack."""
        return self._stack[self._size]

    # Instance methods

    def push(self, value) -> None:
        """Pushes the given value argument to the top of the stack."""
        self._stack.append(value)
        self._size += 1

    def pop(self) -> object:
        """Removes and returns the top element of the stack."""
        top_element = self._stack.pop(self._size)
        self._size -= 1
        return top_element
