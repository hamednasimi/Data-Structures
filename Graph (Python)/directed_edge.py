from edge import Edge


class DirectedEdge(Edge):
    """
    Represents a directed edge in a graph.
    """

    # Dunder methods

    def __init__(self, vertices: tuple, weight: int | float = 1) -> None:

        super().__init__(vertices=vertices, weight=weight)

        self._connected_to: list = list(vertices)
        self._is_directed: bool = True
        self._leaves: object = vertices[0]
        self._to: object = vertices[1]
        vertices[0].add_out_edge(self)
        vertices[1].add_in_edge(self)
        vertices[0].add_edge(self)
        vertices[1].add_edge(self)

    def __str__(self) -> str:
        return f"({self._leaves}, {self._to}, {self._weight})"

    def __getitem__(self, key: int) -> object | int | float:
        """
        In a directed graph, returns the origin [0], destination [1] or weight [2] vertex.
        """
        if key == 0:
            return self._leaves
        elif key == 1:
            return self._to
        elif key == 2:
            return self._weight
        else:
            raise KeyError("The provided key must either be origin [0], destination [1] or weight [2].")

    def __del__(self) -> None:
        self._leaves = None
        self._to = None

    # Properties

    @property
    def vertices(self) -> list:
        """
        Returns a tuple of the vertex objects that the edge is connected to.
        """
        return self._connected_to

    @vertices.setter
    def vertices(self, value: object | None) -> None:
        """
        Setter for self._connected_to attribute.
        """
        self._connected_to = value

    @property
    def leaves(self) -> object:
        """
        Returns the vertex object that the edge is incident from/leaves.
        """
        return self._leaves

    @leaves.setter
    def leaves(self, value: object | None) -> None:
        """
        Setter for self._leaves attribute.
        """
        self._leaves = value

    @property
    def to(self) -> object:
        """
        Returns the vertex object that the edge is incident to/enters.
        """
        return self._to

    @to.setter
    def to(self, value: object | None) -> None:
        """
        Setter for self._to attribute.
        """
        self._to = value

    # Instance methods

    def incident_from(self, vertex: int | object) -> bool:
        """
        Returns True if the edge is incident from/leaves the given vertex.
        """
        return vertex in self._leaves

    def incident_to(self, vertex: int | object) -> bool:
        """
        Returns True if the edge is incident to/enters the given vertex.
        """
        return vertex in self._to

    # Class methods

    @classmethod
    def are_parallel(cls, e1, e2) -> bool:
        """
        Whether the two given directed edges are parallel.
        """
        return e1.leaves == e2.leaves and e1.to == e2.to
