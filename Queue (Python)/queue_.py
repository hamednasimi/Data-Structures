class Queue_:
    """Provides the basic functionalities of a queue data structure."""

    # Dunder methods

    def __init__(self) -> None:

        # The main queue list
        self._queue: list = []
        # The length of the queue
        self._last: int = -1
        # The index 0 constant
        self.__first: int = 0

    # Properties

    @property
    def queue(self) -> list:
        """Returns the queue list itself."""
        return self._queue

    @property
    def last(self) -> int:
        """Returns the index at which the last element sits. -1 means the queue is empty."""
        return self._queue[self._last]

    @property
    def first(self) -> int:
        """Returns the index at which the last element sits. -1 means the queue is empty."""
        return self._queue[0]

    # Instance methods

    def enqueue(self, value) -> None:
        """Appends the given value to the end of the queue."""
        self._last += 1
        self._queue.append(value)

    def dequeue(self) -> object:
        """Removes and returns the first element in the queue."""
        if self._last < self.__first:
            raise KeyError("The queue is empty.")
        self._last -= 1
        return self._queue.pop(0)
