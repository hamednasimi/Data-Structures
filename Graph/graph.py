from vertex import Vertex
from edge import Edge


class Graph:
    """
    Provides the fundamental facilities for undirected graphs.
    """

    # Dunder methods

    def __init__(self, vertices: list = None, edges: list = None) -> None:

        if vertices:
            assert isinstance(vertices, list),\
                "The vertices must be provided in a set."
        if vertices:
            assert Graph.vertex_set_check(vertices),\
                "The vertex set must consist of integers starting at 0 and incrementing in steps of 1."
        if edges:
            assert isinstance(edges, list),\
                "The edges must be provided in a list of tuples, each with 3 integers at most."

        # Primary instance variables
        # The vertex list containing vertex objects
        self._vertices: list = list()  
        # The edge set / binary relation containing edge objects
        self._edges: list = list()  
        # The number of vertices
        self._vertex_count: int = len(vertices) if vertices else 0  
        # The number of edges
        self._edge_count: int = len(edges) if edges else 0  
        # The main string representation for str() and print()
        self._representation: str = ""
        # The reverse sorted degree sequence
        self._degree_sequence: list = []

        # Secondary instance variables
        # Whether the graph is simple
        self._is_simple: bool = None
        # Whether edges in the graph have weights other than 1 and 0 (updated by self.connect())
        self._is_weighted: bool = None
        # Whether every vertex in the graph has at least one edge to every other vertex other than to itself
        self._is_complete: bool = None
        # Whether the graph has at least one pendent vertex
        self._has_pendent: bool = None
        # Whether the graph has at least one isolated vertex
        self._has_isolated: bool = None
        # Whether any two vertices have parallel edges
        self._is_multigraph: bool = None
        # Whether the graph has at least one self-loop
        self._has_self_loop: bool = None
        # Whether every vertex in the graph has a degree of 3 except for one that has the degree v - 1
        self._is_wheel: bool = None

        # Matrix representation attributes
        self._simple_adjacency_matrix: list =\
            [[0 for _ in range(self._vertex_count)] for _ in range(self._vertex_count)]
        self._distance_matrix: list =\
            [[0 for _ in range(self._vertex_count)] for _ in range(self._vertex_count)]
            
        # Miscellaneous
        self._highest_vertex_index: int = self._vertex_count
        self._removed_vertices: list = []
        self._removed_edges: list = []
        self._highest_weight_len: int = 1

        # Initializations
        # Create and add the vertex references
        if vertices != None:
            for v in vertices:
                self._vertices.append(Vertex(v))
        # Create and add the edge references
        if edges != None:
            for e in edges:
                if len(e) == 2:  # No weight is given, defaults to 1
                    self.edge(e[0], e[1])
                if len(e) == 3:  # The weight is provided
                    self.edge(e[0], e[1], e[2])
            self._update_adj()
            self._reset_highest_weight_len()

    def __str__(self) -> str:
        '''The main string representation for str() and print().'''
        self._representation = ""
        for i in range(self._vertex_count):
            for j in range(self._vertex_count):
                current_element = str(self._simple_adjacency_matrix[i][j])
                self._representation += " " * (self._highest_weight_len - len(current_element)) + current_element
                self._representation += " "
            self._representation += ("\n") if i != self._vertex_count - 1 else ""
        return str(self._representation)

    def __repr__(self) -> str:
        return self.__str__()

    def __getitem__(self, index) -> list:
        """Returns the vertex with the given index."""
        return self._vertices[index]

    # Properties

    @property
    def vertices(self) -> list:
        """Returns a list of all vertices in the graph"""
        return self._vertices

    @property
    def edges(self) -> list:
        """Returns a list of all edges in the graph"""
        return self._edges

    @property
    def adj(self) -> list:
        """Updates and returns the simple adjacency matrix."""
        self._update_adj()
        return self._simple_adjacency_matrix
    
    @property
    def degree_sequence(self) -> list:
        """Updates and returns the degree sequence of the graph."""
        self._degree_sequence = []
        for vertex in self._vertices:
            self._degree_sequence.append(self.deg(vertex))
        self._degree_sequence.sort(reverse=True)
        return self._degree_sequence
    
    @property
    def has_self_loop(self) -> bool:
        """Whether the graph has at least one self loop."""
        self._has_self_loop = False
        for edge in self._edges:
            if edge._is_self_loop:
                self._has_self_loop = True
                break
        return self._has_self_loop
    
    @property
    def is_weighted(self) -> bool:
        """Returns True if the graph is weighted (there are different weights than 1)."""
        self._is_weighted = False
        for edge in self._edges:
            if edge.weight != 1:
                self._is_weighted = True
                break
        return self._is_weighted
    
    @property
    def is_multigraph(self) -> bool:
        """
        Returns True if the graph is a multigraph.\
        A multigraph has more than one edge between two vertices.
        """
        self._is_multigraph = False
        for vertex in self._vertices:
            vertex_list = []
            for edge in vertex.edges:
                if edge.vertices[0] != vertex:
                    vertex_list.append(edge.vertices[0])
                else:
                    vertex_list.append(edge.vertices[1])
            for v in vertex_list:
                if vertex_list.count(v) > 1:
                    self._is_multigraph = True
                    break
        return self._is_multigraph
    
    @property
    def check_if_simple(self) -> bool:
        """
        Returns True if the graph is simple.\
        A simple graph is unweighted, has no self-loops and has no parallel edges.
        """
        self._is_simple = (not self.is_weighted) and (not self.has_self_loop) and (not self.is_multigraph)
        return self._is_simple
    
    @property
    def is_complete(self) -> bool:
        """Whether every vertex in the graph has at least one edge to every other vertex except for itself"""
        self._is_complete = True
        ds = self.degree_sequence
        for i, vertex in enumerate(self._vertices):
            if not (ds[i] == self._vertex_count - 1 and not self.loop(vertex)):
                self._is_complete = False
                break
        return self._is_complete
    
    @property
    def isolated(self) -> list:
        """Returns a list of all isolated vertices."""
        return [vertex for vertex in self._vertices if vertex.is_isolated]
    
    @property
    def pendent(self):
        """Returns a list of all pendent vertices."""
        return [vertex for vertex in self._vertices if vertex.is_pendent]

    # Instance methods

    def vertex(self, value=None) -> object:
        """
        Creates and returns a new isolated vertex object that is associated with the graph.
        """
        new_vertex = Vertex(index=self._highest_vertex_index, value=value)
        self._highest_vertex_index += 1
        self._vertices.append(new_vertex)
        self._simple_adjacency_matrix.append(
            [0 for _ in range(self._vertex_count)])
        for row in self._simple_adjacency_matrix:
            row.extend([0])
        self._vertex_count += 1
        return new_vertex

    def v(self, index) -> object:
        """
        Returns the vertex with the index if it exists. Else returns None.
        """
        for v in self._vertices:
            if v.index == index:
                return v
        return None  # In case the vertex with the given index is not present

    def remove_vertex(self, vertex: int | object) -> None:
        """
        Deletes the given vertex reference. Removes all the edges that are connected to it as well. \
        Removing a verted does not shift the remaining vertices' index and adding new vertices \
        afterwards will yield higher index values than the all time highest.\
        The vertex will exist but inaccessible to the user.\
        It is not recommended to access and modify the removed vertex.
        """
        if isinstance(vertex, int):
            vertex = self.v(vertex)
        if vertex in self._vertices and vertex not in self._removed_vertices:
            # Remove edges to the vertex
            for _ in range(len(vertex.edges)):
                self.remove_edge(vertex.edges[0])
            # Remove the vertex from the graph
            deleting_vertex_index = vertex.index
            self._removed_vertices.append(deleting_vertex_index)
            self._edge_count -= len(vertex.edges)
            self._vertices.remove(vertex)
            self._simple_adjacency_matrix[deleting_vertex_index] = [
                -1 for _ in range(self._vertex_count)]
            for row in self._simple_adjacency_matrix:
                row[deleting_vertex_index] = -1
            del vertex
            # Reset self._highest_weight_len
            self._reset_highest_weight_len()
        else:
            raise KeyError(
                "The given vertex does not exist or is already removed.")

    def edge(self, v1: int | object, v2: int | object, weight: int = 1) -> object:
        """Creates and returns an Edge object, connecting the two given vertices."""
        assert isinstance(v1, int) or isinstance(v1, Vertex),\
            "The vertex arguments must either be vertex indices or vertex objects."
        assert isinstance(v2, int) or isinstance(v2, Vertex),\
            "The vertex arguments must either be vertex indices or vertex objects."
        if isinstance(v1, int):
            v1 = self.v(v1)
        if isinstance(v2, int):
            v2 = self.v(v2)
        if v1 is None:
            raise KeyError("The given v1 index/vertex does not exist.")
        if v2 is None:
            raise KeyError("The given v2 index/vertex does not exist.")
        new_edge = Edge(vertices=tuple([v1, v2]), weight=weight)
        self._edges.append(new_edge)
        self._edge_count += 1
        self._update_adj()
        self._reset_highest_weight_len()
        return new_edge

    def e(self, v1: int | object, v2: int | object) -> list:
        """Returns a list of all the edges connecting the two given vertices."""
        assert isinstance(v1, int) or isinstance(v1, Vertex),\
            "The vertex arguments must either be vertex indices or vertex objects."
        assert isinstance(v2, int) or isinstance(v2, Vertex),\
            "The vertex arguments must either be vertex indices or vertex objects."
        if isinstance(v1, int):
            v1 = self.v(v1)
        if isinstance(v2, int):
            v2 = self.v(v2)
        return [e for e in self._edges if e not in self._removed_edges and (e.vertices == [v1, v2] or e.vertices == [v2, v1])]

    def remove_edge(self, edge: object) -> None:
        """
        Removes the given edge.
        The edge argument must be an Edge instance reference because there might be \
        multiple edges connecting the two vertices with the same tuple notation \
        in which case the deletion procedure is ambiguous. 
        """
        assert isinstance(edge, Edge),\
            "The edge argument must be an Edge instance reference."
        self._removed_edges.append(edge)
        self._edges.remove(edge)
        self._edge_count -= 1
        for vertex in edge.connected_to:
            vertex.edges.remove(edge)
        edge.connected_to = None
        self._update_adj()
        self._reset_highest_weight_len()
        del edge
        
    def loop(self, vertex):
        """Returns True if the given vertex has at least one self-loop."""
        if isinstance(vertex, int):
            vertex = self.v(vertex)
        return vertex.loop

    def _update_adj(self) -> None:
        """Updates self._simple_adjacency_matrix with the new edge value."""
        self._simple_adjacency_matrix: list = [
            [0 for _ in range(self._vertex_count)] for _ in range(self._vertex_count)]
        for edge in self._edges:
            i1 = edge.vertices[0].index
            i2 = edge.vertices[1].index
            if i1 != i2:
                self._simple_adjacency_matrix[i1][i2] += edge.weight
            self._simple_adjacency_matrix[i2][i1] += edge.weight

    def _reset_highest_weight_len(self) -> None:
        """Resets the highest weight length for the string representation of the adjacency matrix."""
        self._highest_weight_len = 1
        for row in self._simple_adjacency_matrix:
            for element in row:
                l = len(str(element))
                if l > self._highest_weight_len:
                    self._highest_weight_len = l

    def deg(self, vertex: int | object, count_self_loop=True) -> int:
        """Returns the degree of the given vertex."""
        if isinstance(vertex, int):
            vertex = self.v(vertex)
        return vertex.deg(count_self_loop)

    def weight_deg(self, vertex: int | object, count_self_loop=True) -> int:
        """Returns the summed weight of all edges to the vertex."""
        if isinstance(vertex, int):
            vertex = self.v(vertex)
        return vertex.weight_deg(count_self_loop)
     
    def update(self, all_: bool = False) -> None:
        """
        Updates graph attributes.
        By default it updates the primary attributes only. To update all (including self.is_wheel()), use all_=True.
        """
        raise NotImplementedError()

    # Class / static methods

    @staticmethod
    def vertex_set_check(a: set) -> bool:
        """Returns True if the given set starts at 0 and is ascending by 1. Else returns False."""
        if a[0] != 0:
            return False
        check = True
        for i in range(len(a)):
            if i == 0:
                continue
            if not isinstance(a[i], int):
                return False
            if a[i] - 1 != a[i - 1]:
                check = False
                break
        return check
