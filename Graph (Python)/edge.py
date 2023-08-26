class Edge:
    """Represents an undirected edge in a graph."""

    # Dunder methods

    def __init__(self, vertices: tuple, weight: int | float = 1) -> None:

        from vertex import Vertex
        assert isinstance(vertices, tuple), "Vertices must be provided in a tuple."
        assert len(vertices) == 2, "The vertex tuple must contain exactly 2 vertex objects."
        assert isinstance(vertices[0], Vertex), "Vertex 1 must be an instance if Vertex."
        assert isinstance(vertices[1], Vertex), "Vertex 2 must be an instance if Vertex."

        self.connected_to: list = sorted(list(vertices))
        self._is_directed: bool = False
        vertices[0].add_edge(self)
        vertices[1].add_edge(self)
        self._weight: int = weight
        self._is_self_loop: bool = self.connected_to[0] is self.connected_to[1]

        # Aliases
        self.incident_on = self.connected_to

    def __str__(self) -> str:
        """Returns the string representation of the edge object."""
        return f"({self.connected_to[0]}, {self.connected_to[1]}, {self._weight})"

    def __repr__(self) -> str:
        """Returns the representation of the edge object."""
        return self.__str__()

    def __del__(self) -> None:
        """
        Deletes the edge object.\
        The edge and vertex connection information deletion gets handled by the graph class.
        """
        self._weight = None

    # Properties

    @property
    def vertices(self) -> list:
        """Returns a tuple of the vertex objects that the edge is connected to."""
        return self.connected_to

    @property
    def weight(self) -> int | float:
        """Returns the weight of the edge."""
        return self._weight

    @property
    def is_self_loop(self) -> bool:
        """Returns True if the edge is a self-loop."""
        return self._is_self_loop

    loop = is_self_loop

    # Instance methods

    def is_connected_to(self, vertex: int | object) -> bool:
        return vertex in self.connected_to

    # Class methods

    @classmethod
    def are_adjacent(cls, e1: object, e2: object) -> bool:
        """Whether the two given edges are adjacent."""
        return e1.vertices[0] in e2.vertices or e1.vertices

    @classmethod
    def are_parallel(cls, e1: object, e2: object) -> bool:
        """Whether the two given undirected edges are parallel."""
        return e1.vertices == e2.vertices
