# TODO add a function that returns a list of the edges that connect two vertices. arguments that apply to a tuple like (2, 3)

class Edge:
    """Represents an edge in a graph."""
    
    # Dunder methods
    
    def __init__(self, vertices:tuple, weight:int|float=1, directed=False):
        
        from vertex import Vertex
        assert isinstance(vertices, tuple), "Vertices must be provided in a tuple."
        assert len(vertices) == 2, "The vertex tuple must contain exactly 2 vertex objects."
        assert isinstance(vertices[0], Vertex), "Vertex 1 must be an instance if Vertex."
        assert isinstance(vertices[1], Vertex), "Vertex 2 must be an instance if Vertex."

        self._connected_to: tuple = vertices
        self._is_directed: bool = directed
        if self._is_directed:
            self._leaves: object = vertices[0]
            self._to: object = vertices[1]
            vertices[0].add_out_edge(self)
            vertices[1].add_in_edge(self)
        else:
            self._connected_to = sorted(self._connected_to)
        vertices[0].add_edge(self)
        vertices[1].add_edge(self)
        self._weight = weight
        
    def __del__(self):
        for v in self._connected_to:
            v.delete_edge(self)
        if self._is_directed:
            self._leaves = None
            self._to = None
        else:
            self._connected_to = None
            
    def __str__(self):
        return f"({self._connected_to[0]}, {self._connected_to[1]}, {self._weight})"
        
    def __repr__(self):
        return self.__str__()
    
    def __getitem__(self, key):
        """In a directed graph, returns the origin [0], destination [1] or weight [2] vertex."""
        assert self._is_directed, "The graph is not directed. use (.vertices) instead."
        if key in [0, 1]:
            return self.vertices[key]
        elif key == 2:
            return self._weight
        else:
            raise KeyError("The provided key must either be 0, 1 or 2.")
            
    # Properties
    
    @property
    def vertices(self):
        """Returns a tuple of the vertex objects that the edge is connected to."""
        return self._connected_to
    
    @property
    def weight(self):
        """Returns the weight of the edge."""
        return self._weight

    @property
    def leaves(self):
        """If the graph is directed, returns the vertex object that the edge is incident from/leaves."""
        if self._is_directed: return self._leaves
        else: raise AttributeError("In an undirected graph, an edge can't have an origin vertex.")

    @property
    def to(self):
        """If the graph is directed, returns the vertex object that the edge is incident to/enters."""
        if self._is_directed: return self._to
        else: raise AttributeError("In an undirected graph, an edge can't have a destination vertex.")
    
    # Instance methods
    
    def is_connected_to(self, vertex:int|object):
        pass # TODO

    def leaves_from(self, vertex:int|object):
        pass # TODO
    
    def goes_to(self, vertex:int|object):
        pass # TODO
    
    # Class methods

    @classmethod
    def are_adjacent(self, e1, e2) -> bool:
        """Whether the two given edges are adjacent."""
        assert isinstance(e1, Edge), "e1 must be an instance if Edge."
        assert isinstance(e2, Edge), "e1 must be an instance if Edge."
        # TODO

    @classmethod
    def are_parallel(self, e1, e2) -> bool:
        """Whether the two given edges are parallel."""
        # TODO

    @classmethod
    def leaves_(cls, vertex:object):
        """Returns a list of edge objects that incident from/leave the given vertex. Returns an empty list if none exist.

        Args:
            vertex (Vertex): The vertex object.
        """
        from vertex import Vertex
        if isinstance(vertex, Vertex):
            return vertex.out_edges
        else:
            raise KeyError("The given vertex must be of type Vertex.")
    
    @classmethod
    def to_(cls, vertex:object):
        """Returns a list of edge objects that incident to/enter the given vertex. Returns an empty list if none exist.

        Args:
            vertex (Vertex): The vertex object.
        """
        from vertex import Vertex
        if isinstance(vertex, Vertex):
            return vertex.in_edges
        else:
            raise KeyError("The given vertex must be of type Vertex.")