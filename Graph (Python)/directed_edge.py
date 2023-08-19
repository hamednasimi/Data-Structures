from .edge import Edge


class DirectedEdge(Edge):
    """Represents a directed edge in a graph."""

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
        return f"({self._leaves}, {self.connected_to[1]}, {self._weight})"

    def __getitem__(self, key) -> object | int | float:
        """In a directed graph, returns the origin [0], destination [1] or weight [2] vertex."""
        if key in [0, 1]:
            return self.vertices[key]
        elif key == 2:
            return self._weight
        else:
            raise KeyError("The provided key must either be origin [0], destination [1] or weight [2].")

    def __del__(self) -> None:
        # TODO self._leaves.delete_edge(self) using the directed_graph's remove_edge method instead
        # TODO self._to.delete_edge(self) using the directed_graph's remove_edge method instead
        self._leaves = None
        self._to = None

    # Properties

    @property
    def leaves(self) -> object:
        """Returns the vertex object that the edge is incident from/leaves."""
        return self._leaves

    @property
    def to(self) -> object:
        """Returns the vertex object that the edge is incident to/enters."""
        return self._to

    # Instance methods

    def incident_from(self, vertex: int | object) -> bool:
        """Returns True if the edge is incident from/leaves the given vertex."""
        return vertex in self._leaves

    def incident_to(self, vertex: int | object) -> bool:
        """Returns True if the edge is incident to/enters the given vertex."""
        return vertex in self._to

    # Class methods

    @classmethod
    def are_parallel(cls, e1, e2) -> bool:
        """Whether the two given directed edges are parallel."""
        return e1.leaves == e2.leaves and e1.to == e2.to
