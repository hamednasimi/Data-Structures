from vertex import Vertex
from edge import Edge

class Graph:
    """
    Provides the fundamental facilities for directed and undirected graphs. Mixed graphs are not supported.
    """

    # Dunder methods

    def __init__(self, vertices: list = None, edges: list = None,  directed=False, auto_update=True) -> object:
        
        # TODO make the initializer be able to take vertex objects

        # Asserts
        if vertices: assert isinstance(vertices, list), "The vertices must be provided in a set."
        if vertices: assert Graph.vertex_set_check(vertices), "The vertex set must consist of integers starting at 0 and incrementing in steps of 1."
        if edges: assert isinstance(edges, list), "The edges must be provided in a list of tuples, each with 3 integers at most."
        if directed: assert isinstance(directed, bool), "Direction must be a boolean value."
        if auto_update: assert isinstance(auto_update, bool), "auto_update must be a boolean value."
        
        # Primary instance variables
        self._vertices: list = list() # The vertex set containing vertex objects
        self._edges: list = list() # The edge set / binary relation containing edge objects
        self._vertex_count: int = len(vertices) if vertices else 0 # The number of vertices
        self._edge_count: int = len(edges) if edges else 0 # The number of edges
        self._is_directed: bool = directed # Whether edges in the graph are directed
        self._auto_update: bool = auto_update # Whether to update the primary attributes automatically after each new vertex/edge addition
        if not self._is_directed:
            self._degree_sequence: list = []
        elif self._is_directed:
            self._in_degree_sequence: list = []
            self._out_degree_sequence: list = []
        
        # Secondary instance variables
        self._is_simple: bool = None # Whether the graph is simple 
        self._is_weighted: bool = False # Whether edges in the graph have weights other than 1 and 0 (updated by self.connect())
        self._is_complete: bool = None # Whether every vertex in the graph has at least one edge to every other vertex other than to itself
        self._has_pendent: bool = None # Whether the graph has at least one pendent vertex
        self._has_isolated: bool = None # Whether the graph has at least one isolated vertex
        self._is_multigraph: bool = None # Whether any two vertices have parallel edges
        self._representation: str = "" # The main string representation for str() and print()
        self._is_wheel: bool = None
        
        # Matrix representation attributes
        self._simple_adjacency_matrix: list = [[0 for _ in range(self._vertex_count)] for _ in range(self._vertex_count)]
        self._distance_matrix: list = [[0 for _ in range(self._vertex_count)] for _ in range(self._vertex_count)]
        
        # Initializations
        # Create and add the vertex references
        if vertices != None:
            for v in vertices:
                self._vertices.append(Vertex(v))
        # Create and add the edge references
        if edges != None:
            for e in edges:
                if len(e) == 2: # No weight is given, defaults to 1
                    self.edge(e[0], e[1])
                if len(e) == 3: # The weight is provided
                    self.edge(e[0], e[1], e[2])
        
    def __str__(self):
        '''The main string representation for str() and print().'''
        self._representation = ""
        for i in range(self._vertex_count):
            for j in range(self._vertex_count):
                self._representation += str(self._simple_adjacency_matrix[i][j])
                self._representation += " "
            self._representation += ("\n") if i != self._vertex_count - 1 else ""
        return str(self._representation)
    
    def __repr__(self):
        return self.__str__()
    
    def __getitem__(self, index):
        """Returns the vertex with the given index."""
        return self._vertices[index]
        
    # Properties
    
    @property
    def vertices(self):
        return self._vertices
    
    @property
    def edges(self):
        return self._edges
    
    @property
    def adj(self):
        return self._simple_adjacency_matrix
    
    # Instance methods
    
    def vertex(self, value=None):
        """
        Creates and returns a new isolated vertex object that is associated with the graph.
        """
        new_vertex = Vertex(index=len(self._vertices), value=value)
        self._vertices.append(new_vertex)
        self._simple_adjacency_matrix.append([0 for _ in range(self._vertex_count)])
        for row in self._simple_adjacency_matrix:
            row.extend([0])
        self._vertex_count += 1
        return new_vertex
    
    def v(self, index):
        """
        Returns the vertex with the index if it exists. Else returns None.
        """
        for v in self._vertices:
            if v.index == index:
                return v
        return None # In case the vertex with the given index is not present
    
    def edge(self, v1:int|object, v2:int|object, weight:int=1):
        """
        Creates and returns an Edge object, connecting the two given vertices.
        """
        assert isinstance(v1, int) or isinstance(v1, Vertex), "The vertex arguments must either be vertex indices or vertex objects."
        assert isinstance(v2, int) or isinstance(v2, Vertex), "The vertex arguments must either be vertex indices or vertex objects."
        if isinstance(v1, int):
            v1 = self.v(v1)
        if isinstance(v2, int):
            v2 = self.v(v2)
        if v1 is None: raise KeyError("The given v1 index/vertex does not exist.")
        if v2 is None: raise KeyError("The given v2 index/vertex does not exist.")
        new_edge = Edge(vertices=(v1, v2), weight=weight, directed=self._is_directed)
        self._edges.append(new_edge)
        self._edge_count += 1
        self.update_adj(new_edge)
        return new_edge
    
    def e(self, v1:int|object, v2:int|object):
        """Returns a list of all the edges connecting the two given vertices."""
        assert isinstance(v1, int) or isinstance(v1, Vertex), "The vertex arguments must either be vertex indices or vertex objects."
        assert isinstance(v2, int) or isinstance(v2, Vertex), "The vertex arguments must either be vertex indices or vertex objects."
        if isinstance(v1, int):
            v1 = self.v(v1)
        if isinstance(v2, int):
            v2 = self.v(v2)
        if self._is_directed:
            return [e for e in self._edges if e.vertices == [v1, v2]]
        else:
            return [e for e in self._edges if e.vertices == [v1, v2] or e.vertices == [v2, v1]]
    
    def update_adj(self, edge:object):
        """Updates self._simple_adjacency_matrix with the new edge value"""
        if self._is_directed:
            self._simple_adjacency_matrix[edge[0].index][edge[1].index] += edge[2]
        else:
            i1 = edge.vertices[0].index
            i2 = edge.vertices[1].index
            if i1 != i2:
                self._simple_adjacency_matrix[i1][i2] += edge.weight
            self._simple_adjacency_matrix[i2][i1] += edge.weight
    
    def update(self, all_:bool=False):
        '''
        Updates graph attributes.
        By default it updates the primary attributes only. To update all (including self.is_wheel()), use all_=True.
        '''
        raise NotImplementedError()
        # TODO
    
    # Class / static methods

    @staticmethod
    def vertex_set_check(a:set):
        """Returns True if the given set starts at 0 and is ascending. Else returns False."""
        if a[0] != 0:
            return False
        check = True
        for i in range(len(a)):
            if i == 0: continue
            if not isinstance(a[i], int): return False
            if a[i] - 1 != a[i - 1]:
                check = False
                break
        return check