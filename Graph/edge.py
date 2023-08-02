# TODO add a function that returns a list of the edges that connect two vertices. arguments that apply to a tuple like (2, 3)

class Edge:
    """Represents an undirected edge in a graph."""
    
    # Dunder methods
    
    def __init__(self, vertices:tuple, weight:int|float=1) -> object:
        
        from vertex import Vertex
        assert isinstance(vertices, tuple), "Vertices must be provided in a tuple."
        assert len(vertices) == 2, "The vertex tuple must contain exactly 2 vertex objects."
        assert isinstance(vertices[0], Vertex), "Vertex 1 must be an instance if Vertex."
        assert isinstance(vertices[1], Vertex), "Vertex 2 must be an instance if Vertex."

        self.connected_to = sorted(vertices)
        self._is_directed: bool = False
        vertices[0].add_edge(self)
        vertices[1].add_edge(self)
        self._weight = weight
            
    def __str__(self) -> str:
        return f"({self.connected_to[0]}, {self.connected_to[1]}, {self._weight})"
        
    def __repr__(self) -> str:
        return self.__str__()
    
    def __del__(self) -> None:
        self._weight = None
            
    # Properties
    
    @property
    def vertices(self) -> tuple:
        """Returns a tuple of the vertex objects that the edge is connected to."""
        return self.connected_to
    
    @property
    def weight(self) -> int | float:
        """Returns the weight of the edge."""
        return self._weight

    # Instance methods
    
    def is_connected_to(self, vertex:int|object) -> bool:
        return vertex in self.connected_to

    # Class methods

    @classmethod
    def are_adjacent(cls, e1, e2) -> bool:
        """Whether the two given edges are adjacent."""
        return e1.vertices[0] in e2.vertices or e1.vertices

    @classmethod
    def are_parallel(cls, e1, e2) -> bool:
        """Whether the two given undirected edges are parallel."""
        return e1.vertices == e2.vertices