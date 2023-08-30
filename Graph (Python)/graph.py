from edge import Edge
from vertex import Vertex


class Graph:
    """
    Provides the fundamental facilities for undirected graphs.
    """

    # Dunder methods

    def __init__(self, vertices: list = None, edges: list = None) -> None:

        if vertices:
            assert isinstance(vertices, list), \
                "The vertices must be provided in a set."
        if vertices:
            assert Graph.vertex_set_check(vertices), \
                "The vertex set must consist of integers starting at 0 and incrementing in steps of 1."
        if edges:
            assert isinstance(edges, list), \
                "The edges must be provided in a list of tuples, each with 3 integers at most."

        # Primary instance variables
        # The vertex list containing vertex objects
        self._vertices: list = list()
        # The edge set / binary relation containing edge objects
        self._edges: list = list()
        # The number of vertices
        self._vertex_count: int = len(vertices) if vertices else 0
        # The number of edges
        self._edge_count: int = 0
        # The reverse sorted degree sequence
        self._degree_sequence: list = []
        # The radius of the graph
        self._radius: int = 0
        # The diameter of the graph
        self._diameter: int = 0
        # The central vertices
        self._central: list = []
        # The sum of the degrees of all vertices
        self._n: int = 0

        # Secondary instance variables
        # Whether the graph is simple
        self._is_simple: bool = False
        # Whether edges in the graph have weights other than 1 and 0 (updated by self.connect())
        self._is_weighted: bool = False
        # Whether every vertex in the graph has at least one edge to every other vertex other than to itself
        self._is_complete: bool = False
        # Whether the graph has at least one pendent vertex
        self._has_pendent: bool = False
        # Whether the graph has at least one isolated vertex
        self._has_isolated: bool = False
        # Whether any two vertices have parallel edges
        self._is_multigraph: bool = False
        # Whether the graph has at least one self-loop
        self._has_self_loop: bool = False
        # Whether the graph is connected (every vertex has a path to every other vertex)
        self._is_connected: bool = False
        # Whether every vertex in the graph has a degree of 3 except for one that has the degree v - 1
        self._is_wheel: bool = False

        # Matrix representation attributes
        self._simple_adjacency_matrix: list = \
            [[0 for _ in range(self._vertex_count)] for _ in range(self._vertex_count)]
        self._distance_matrix: list = \
            [[0 for _ in range(self._vertex_count)] for _ in range(self._vertex_count)]

        # Miscellaneous
        # The main string representation for str() and print()
        self._representation: str = ""
        # The highest index created in the graph. Saved so the vertex deletions won't mess up new vertices
        self._highest_vertex_index: int = self._vertex_count
        # The removed vertices are saved here so any reference to them would not work
        self._removed_vertices: list = []
        # The removed edges are saved here so any reference to them would not work
        self._removed_edges: list = []
        # For use in representation
        self._highest_weight_len: int = 1

        # Initializations
        # Create and add the vertex references
        if vertices is not None:
            for v in vertices:
                self._vertices.append(Vertex(v))
        # Create and add the edge references
        if edges is not None:
            for e in edges:
                if len(e) == 2:  # No weight is given, defaults to 1
                    self.edge(e[0], e[1])
                elif len(e) == 3:  # The weight is provided
                    self.edge(e[0], e[1], e[2])
                else:
                    raise KeyError(
                        "The given edge must be provided as a tuple of 2 or 3 values e.g. (vertex, vertex[, weight])")
            self._reset_highest_weight_len()

    def __str__(self) -> str:
        """The main string representation for str() and print()."""
        self._representation = ""
        for i in range(self._vertex_count):
            for j in range(self._vertex_count):
                current_element = str(self._simple_adjacency_matrix[i][j])
                self._representation += " " * (self._highest_weight_len - len(current_element)) + current_element
                self._representation += " "
            self._representation += "\n" if i != self._vertex_count - 1 else ""
        return str(self._representation)

    def __repr__(self) -> str:
        return self.__str__()

    def __getitem__(self, index: int) -> list:
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
    def vertex_count(self) -> int:
        """Returns the number of vertices."""
        return self._vertex_count

    @property
    def edge_count(self) -> int:
        """Returns the number of vertices."""
        return self._edge_count

    @property
    def degree_sequence(self) -> list:
        """Updates and returns the degree sequence of the graph."""
        self._degree_sequence = []
        for vertex in self._vertices:
            self._degree_sequence.append(self.deg(vertex))
        self._degree_sequence.sort(reverse=True)
        return self._degree_sequence

    @property
    def radius(self) -> int:
        """Returns the radius of the graph."""
        e = []
        for vertex in self._vertices:
            e.append(self.eccentricity(vertex))
        self._radius = min(e)
        return self._radius

    @property
    def r(self) -> int:
        """Alias for the radius property."""
        return self.radius

    @property
    def diameter(self) -> int:
        """Returns the diameter of the graph."""
        e = []
        for vertex in self._vertices:
            e.append(self.eccentricity(vertex))
        self._diameter = max(e)
        return self._diameter

    @property
    def central(self) -> list:
        """
        Returns a list of all central vertices of the graph.\
        A central vertex's eccentricity is equal to the radius of the graph.
        """
        self._central = [vertex for vertex in self._vertices if self.eccentricity(vertex) == self._radius]
        return self._central

    @property
    def n(self) -> int:
        """Returns the sum of the degrees of all vertices."""
        if self._is_complete:
            self._n = self._vertex_count * (self._vertex_count - 1)
            return self._n
        else:
            self._n = sum(self.degree_sequence)
            return self._n

    @property
    def is_simple(self) -> bool:
        """
        Returns True if the graph is simple.\
        A simple graph is unweighted, has no self-loops and has no parallel edges.
        """
        self._is_simple = (not self.is_weighted) and (not self.has_self_loop) and (not self.is_multigraph)
        return self._is_simple

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
    def has_pendent(self) -> bool:
        """Returns True if the graph has at least one pendent vertex."""
        self._has_pendent = False
        if len(self.pendent) > 0:
            self._has_pendent = True
        return self._has_pendent

    @property
    def has_isolated(self) -> bool:
        """Returns True if the graph has at least one isolated vertex."""
        self._has_isolated = False
        if len(self.isolated) > 0:
            self._has_isolated = True
        return self._has_isolated

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
    def has_self_loop(self) -> bool:
        """Whether the graph has at least one self loop."""
        self._has_self_loop = False
        for edge in self._edges:
            if edge.is_self_loop:
                self._has_self_loop = True
                break
        return self._has_self_loop

    @property
    def is_connected(self) -> bool:
        """Whether the graph is connected (every vertex has a path to every other vertex)."""
        self._is_connected = True
        for i, row in enumerate(self.distance_matrix):
            for distance in row:
                if row.index(distance) != i and distance == 0:
                    self._is_connected = False
                    return self._is_connected
        return self._is_connected

    @property
    def is_wheel(self) -> bool:
        """
        Returns True if the graph is a wheel. (All edges have a degree of 3 \
        except for one vertex which has a degree of v - 1)
        """
        self._is_wheel = False
        if sorted(self.degree_sequence, reverse=True) == \
                [self.vertex_count - 1] + [3 for _ in range(self.vertex_count - 1)]:
            self._is_wheel = True
        return self._is_wheel

    @property
    def adj(self) -> list:
        """Updates and returns the simple adjacency matrix."""
        self._update_adj()
        return self._simple_adjacency_matrix

    @property
    def M(self) -> list:
        """Updates and returns the simple adjacency matrix (same as self.adj)."""
        self._update_adj()
        return self._simple_adjacency_matrix

    @property
    def distance_matrix(self) -> list:
        """Updates and returns the distance matrix."""
        if self.is_simple:
            for vertex in self._vertices:
                for i, element in enumerate(self._simple_bfs(vertex)):
                    self._distance_matrix[vertex.index][i] = element
            return self._distance_matrix

    @property
    def isolated(self) -> list:
        """Returns a list of all isolated vertices."""
        return [vertex for vertex in self._vertices if vertex.is_isolated]

    @property
    def pendent(self) -> list:
        """Returns a list of all pendent vertices."""
        return [vertex for vertex in self._vertices if vertex.is_pendent]

    # Instance methods

    def vertex(self, value: object = None) -> object:
        """
        Creates and returns a new isolated vertex object that is associated with the graph.
        """
        new_vertex = Vertex(index=self._highest_vertex_index, value=value)
        self._highest_vertex_index += 1
        self._vertices.append(new_vertex)
        self._simple_adjacency_matrix.append([0 for _ in range(self._vertex_count)])
        for row in self._simple_adjacency_matrix:
            row.extend([0])
        self._distance_matrix.append([0 for _ in range(self._vertex_count)])
        for row in self._distance_matrix:
            row.extend([0])
        self._vertex_count += 1
        return new_vertex

    def v(self, index: int) -> Vertex | None:
        """
        Returns the vertex with the index if it exists. Else returns None.
        """
        if index in self._removed_vertices:
            raise KeyError("The requested vertex is removed.")
        for v in self._vertices:
            if v.index == index:
                return v
        return None  # In case the vertex with the given index is not present

    def remove_vertex(self, vertex: int | Vertex) -> None:
        """
        Deletes the given vertex reference. Removes all the edges that are connected to it as well. \
        Removing a vertex does not shift the remaining vertices' index and adding new vertices \
        afterward will yield higher index values than the all-time highest.\
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
            raise KeyError("The given vertex does not exist or is already removed.")

    def edge(self, v1: int | object, v2: int | object, weight: int = 1) -> object:
        """Creates and returns an Edge object, connecting the two given vertices."""
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
        new_edge = Edge(vertices=tuple([v1, v2]), weight=weight)
        self._edges.append(new_edge)
        self._edge_count += 1
        self._update_adj()
        self._reset_highest_weight_len()
        return new_edge

    def e(self, v1: int | object, v2: int | object = None) -> list | int:
        """
        With only the v1 argument given, returns the eccentricity of the vertex.
        With both arguments, returns a list of all the edges connecting the two given vertices.
        """
        if v2 is None:
            return self.eccentricity(v1)
        assert isinstance(v1, int) or isinstance(v1, Vertex), \
            "The vertex arguments must either be vertex indices or vertex objects."
        assert isinstance(v2, int) or isinstance(v2, Vertex), \
            "The vertex arguments must either be vertex indices or vertex objects."
        if isinstance(v1, int):
            v1 = self.v(v1)
        if isinstance(v2, int):
            v2 = self.v(v2)
        return [e for e in self._edges if
                not (not (e not in self._removed_edges) or not (e.vertices == [v1, v2] or e.vertices == [v2, v1]))]

    def remove_edge(self, edge: object) -> None:
        """
        Removes the given edge.
        The edge argument must be an Edge instance reference because there might be \
        multiple edges connecting the two vertices with the same tuple notation \
        in which case the deletion procedure is ambiguous. 
        """
        assert isinstance(edge, Edge), \
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

    def loop(self, vertex: int | Vertex) -> bool:
        """Returns True if the given vertex has at least one self-loop."""
        if isinstance(vertex, int):
            vertex = self.v(vertex)
        return vertex.loop

    def deg(self, vertex: int | Vertex, count_self_loop: bool = True) -> int:
        """Returns the degree of the given vertex."""
        if isinstance(vertex, int):
            vertex = self.v(vertex)
        return vertex.deg(count_self_loop)

    def weight_deg(self, vertex: int | Vertex, count_self_loop: bool = True) -> int | tuple:
        """Returns the summed weight of all edges to the vertex."""
        if isinstance(vertex, int):
            vertex = self.v(vertex)
        return vertex.weight_deg(count_self_loop)

    def d(self, origin: int | object, destination: int | object) -> int:
        """
        Returns the shortest distance between the origin and destination as an int.\
        The distance is the number of edges between the two points.
        """
        if isinstance(origin, Vertex):
            origin = origin.index
        if isinstance(destination, Vertex):
            destination = destination.index
        return self.distance_matrix[origin][destination]

    def incident_on(self, vertex: int | Vertex) -> list:
        """Returns every edge connected to the vertex."""
        if isinstance(vertex, int):
            return self.v(vertex).edges
        return vertex.edges

    def eccentricity(self, vertex: int | object) -> int:
        """
        Returns the longest of shortest distances between the given vertex and all other vertices.
        """
        if isinstance(vertex, int):
            vertex = self.v(vertex)
        return max(self._simple_bfs(vertex))

    def _simple_bfs(self, vertex: Vertex) -> list:
        """Returns a list of the distances from the given vertex to all other vertices."""
        from Utils.BFS_state import BFSState
        distance = [0 for _ in range(self._highest_vertex_index)]
        if vertex not in self._removed_vertices:
            queue = []
            vertex._BFS_state = BFSState.SEEN
            if not vertex.is_isolated:
                queue.append(vertex)
                while len(queue) > 0:
                    current = queue.pop(0)
                    for edge in current.edges:
                        if edge.connected_to[0] == current:
                            other_vertex = edge.connected_to[1]
                        else:
                            other_vertex = edge.connected_to[0]
                        if other_vertex._BFS_state == BFSState.UNSEEN:
                            other_vertex._BFS_state = BFSState.SEEN
                            distance[other_vertex.index] = distance[current.index] + 1
                            queue.append(other_vertex)
                    current._BFS_state = BFSState.VISITED
            for v in self._vertices:
                v._BFS_state = BFSState.UNSEEN
        return distance

    def _update_adj(self, edge: Edge = None) -> None:
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
                length = len(str(element))
                if length > self._highest_weight_len:
                    self._highest_weight_len = length

    # Class / static methods

    @staticmethod
    def vertex_set_check(a: set | list) -> bool:
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

    @staticmethod
    def N(vertex_count) -> int:
        """Returns the sum of the degrees of a complete graph given the vertex count."""
        return vertex_count * (vertex_count - 1)

    @staticmethod
    def E(vertex_count) -> int:
        """
        Returns the maximum possible number of edges given the vertex count \
        assuming the graph is simple and complete.
        """
        return Graph.N(vertex_count) // 2

    @staticmethod
    def edge_subset(vertex_count: int) -> int:
        """
        Returns the number of possible subsets of edges with a certain number of vertices \
        assuming the graph is simple.
        """
        return 2 ** Graph.E(vertex_count)
