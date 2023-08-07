from .edge import Edge

class DirectedEdge(Edge):
    """Represents a directed edge in a graph."""
    
    # Dunder methods
    
    def __init__(self, vertices:tuple, weight:int|float=1) -> object:
        
        from .vertex import Vertex
        assert isinstance(vertices, tuple), "Vertices must be provided in a tuple."
        assert len(vertices) == 2, "The vertex tuple must contain exactly 2 vertex objects."
        assert isinstance(vertices[0], Vertex), "Vertex 1 must be an instance if Vertex."
        assert isinstance(vertices[1], Vertex), "Vertex 2 must be an instance if Vertex."

        self._connected_to: tuple = vertices
        self._is_directed: bool = True
        self._leaves: object = vertices[0]
        self._to: object = vertices[1]
        vertices[0].add_out_edge(self)
        vertices[1].add_in_edge(self)
        vertices[0].add_edge(self)
        vertices[1].add_edge(self)
        self._weight = weight
    
    def __getitem__(self, key) -> object | int | float:
        """In a directed graph, returns the origin [0], destination [1] or weight [2] vertex."""
        assert self._is_directed, "The graph is not directed. use (.vertices) instead."
        if key in [0, 1]:
            return self.vertices[key]
        elif key == 2:
            return self._weight
        else:
            raise KeyError("The provided key must either be 0, 1 or 2.")
        
    def __del__(self) -> None:
        self._leaves.delete_edge(self)
        self._to.delete_edge(self)
        self._leaves = None
        self._to = None
        self._weight = None
    
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
    
    def incident_from(self, vertex:int|object) -> bool:
        """Returns True if the edge is incident from/leaves the given vertex."""
        return vertex in self._leaves
    
    def incident_to(self, vertex:int|object) -> bool:
        """Returns True if the edge is incident to/enters the given vertex."""
        return vertex in self._to
    
    # def remove_vertex(self, vertex):
    #     """Removes the given vertex's references from the edge."""
    
    # Class methods
    
    @classmethod
    def are_parallel(cls, e1, e2) -> bool:
        """Whether the two given directed edges are parallel."""
        return e1.leaves == e2.leaves and e1.to == e2.to
    
    