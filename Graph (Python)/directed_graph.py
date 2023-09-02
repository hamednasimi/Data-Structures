from graph import Graph
from vertex import Vertex
from directed_edge import DirectedEdge


class DirectedGraph(Graph):
    """
    Provides the fundamental facilities for directed graphs.
    """

    # Dunder methods

    def __init__(self, vertices: list = None, edges: list = None) -> None:

        super().__init__(vertices=vertices, edges=edges)

        # Primary instance variables
        # Replacement for the Graph degree_sequence
        self._degree_sequence: list = []  # Not used in a directed graph
        self._in_degree_sequence: list = []
        self._out_degree_sequence: list = []

        # Secondary instance variables
        # Whether the graph is simple
        self._is_simple: bool = False

    # Properties
    
    @property
    def is_simple(self) -> bool:
        """
        Always returns False. A directed graph can't be simple.
        """
        return False

    # Instance methods

    def edge(self, v1: int | object, v2: int | object, weight: int = 1) -> DirectedEdge:
        """
        Creates and returns an Edge object, connecting the two given vertices.
        """
        assert isinstance(v1, int) or isinstance(v1, Vertex), \
            "The vertex arguments must either be vertex indices or vertex objects."
        assert isinstance(v2, int) or isinstance(v2, Vertex), \
            "The vertex arguments must either be vertex indices or vertex objects."
        if isinstance(v1, int):
            v1 = self.v(v1)
        if isinstance(v2, int):
            v2 = self.v(v2)
        if v1 is None:
            raise KeyError("The given v1 index/vertex does not exist.")
        if v2 is None:
            raise KeyError("The given v2 index/vertex does not exist.")
        new_edge = DirectedEdge(vertices=tuple([v1, v2]), weight=weight)
        self._edges.append(new_edge)
        self._edge_count += 1
        self._update_adj()
        self._reset_highest_weight_len()
        return new_edge

    def e(self, v1: int | Vertex, v2: int | Vertex = None) -> list | int:
        """
        Returns a list of all the edges connecting the two given vertices.
        """
        assert isinstance(v1, int) or isinstance(v1, Vertex), \
            "The vertex arguments must either be vertex indices or vertex objects."
        assert isinstance(v2, int) or isinstance(v2, Vertex), \
            "The vertex arguments must either be vertex indices or vertex objects."
        if isinstance(v1, int):
            v1 = self.v(v1)
        if isinstance(v2, int):
            v2 = self.v(v2)
        return [e for e in self._edges if e.vertices == [v1, v2]]

    def remove_edge(self, edge: object) -> None:
        """
        Removes the given edge.
        The edge argument must be an Edge instance reference because there might be \
        multiple edges connecting the two vertices with the same tuple notation \
        in which case the deletion procedure is ambiguous. 
        """
        assert isinstance(edge, DirectedEdge), "The edge argument must be an Edge instance reference."
        self._removed_edges.append(edge)
        self._edges.remove(edge)
        self._edge_count -= 1
        for vertex in edge.vertices:
            vertex.edges.remove(edge)
        edge.vertices = None
        edge.leaves = None
        edge.to = None
        self._update_adj()
        self._reset_highest_weight_len()
        del edge

    def incident_to(self, vertex: Vertex | int) -> list:
        """
        Returns the edges that incident to the given vertex.
        """
        if isinstance(vertex, int):
            return self.v(vertex).in_edges
        return vertex.in_edges

    def deg(self, vertex: int | Vertex, count_self_loop: bool = True) -> int:
        """
        Returns the degree of the given vertex.
        """
        if isinstance(vertex, int):
            vertex = self.v(vertex)
        return vertex.deg(count_self_loop)

    def incident_from(self, vertex: Vertex | int) -> list:
        """
        Returns the edges that incident from the given vertex.
        """
        if isinstance(vertex, int):
            return self.v(vertex).out_edges
        return vertex.out_edges

    def incident_on(self, vertex: Vertex | int) -> None:
        """
        Not Implemented.
        """
        raise NotImplementedError()

    def _simple_bfs(self, vertex: Vertex) -> None:
        """
        Not Implemented.
        """
        raise NotImplementedError()

    def eccentricity(self, vertex: int | object) -> None:
        """
        Not Implemented.
        """
        raise NotImplementedError()
