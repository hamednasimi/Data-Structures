from Utils.BFS_state import BFSState


class Vertex:
    """
    Represents a vertex in a graph.
    """

    # Dunder methods

    def __init__(self, index: int, value: object = None, directional_graph: bool = False) -> None:

        assert isinstance(index, int), "The index must be of type int."

        # Attributes
        self._index: int = index
        self._value: object = value
        self._edges_a: list = []
        self._in_edges_a: list = []
        self._out_edges_a: list = []
        self._loop: bool = False
        self._directional_graph: bool = directional_graph
        self._BFS_state: BFSState = BFSState.UNSEEN

    def __str__(self) -> str:
        return f"{self._index}"

    def __repr__(self) -> str:
        return self.__str__()

    def __del__(self) -> None:
        self._index = None
        del self._value
        self._value = None

    def __lt__(self, other: object) -> bool:  # <
        return self._index < other.index

    def __le__(self, other: object) -> bool:  # <=
        return self._index <= other.index

    def __eq__(self, other: object) -> bool:  # ==
        return self is other

    def __ne__(self, other: object) -> bool:  # !=
        return self is not other

    def __gt__(self, other: object) -> bool:  # >
        return self._index > other.index

    def __ge__(self, other: object) -> bool:  # >=
        return self._index >= other.index

    # Properties

    @property
    def index(self) -> int:
        """
        Returns the index of the vertex in the vertex set.
        """
        return self._index

    @index.setter
    def index(self, new_index) -> None:
        """
        Sets the index of the vertex to the new value.
        """
        self._index = new_index

    @property
    def value(self) -> object:
        """
        Returns the value of the vertex.
        """
        return self._value

    @value.setter
    def value(self, value) -> None:
        """
        Sets the value of the vertex.
        """
        self._value = value

    @value.deleter
    def value(self) -> None:
        """
        Deletes the value of the vertex. Sets it to None.
        """
        self._value = None

    @property
    def edges(self) -> list:
        """
        Returns a list of all edges that are connected to the vertex.
        """
        return self._edges_a

    @property
    def in_edges(self) -> list:
        """
        Returns a list of all edges that are connected to the vertex.
        """
        return self._in_edges_a

    @property
    def out_edges(self) -> list:
        """
        Returns a list of all edges that are connected to the vertex.
        """
        return self._out_edges_a

    @property
    def loop(self) -> bool:
        """
        Returns True if the vertex has a self-loop edge.
        """
        self._loop = False
        for edge in self._edges_a:
            if edge.is_self_loop:
                self._loop = True
        return self._loop

    @property
    def is_isolated(self) -> bool:
        """
        Returns True if the vertex is isolated
        (there is no edge connected to the vertex. A self-looping vertex is not pendent).
        """
        return self.deg(count_self_loop=False) == 0

    @property
    def is_pendent(self) -> bool:
        """
        Returns True if the given vertex is pendent
        (there is only 1 edge connected to the vertex. A self-looping vertex is not pendent).
        """
        return self.deg(count_self_loop=False) == 1

    @property
    def adjacent_vertices(self) -> list:
        """
        Returns a list of the vertices that are adjacent to self.
        """
        adjacent_vertices = []
        for edge in self._edges_a:
            if edge.connected_to[0] == self:
                adjacent_vertices.append(edge.connected_to[1])
            else:
                adjacent_vertices.append(edge.connected_to[0])
        return adjacent_vertices

    # Instance methods

    def add_edge(self, edge: object) -> None:
        """
        Connects the vertex to the given edge.
        """
        self._edges_a.append(edge)

    def add_in_edge(self, edge: object) -> None:
        """
        Adds incoming edge.
        """
        self._in_edges_a.append(edge)

    def add_out_edge(self, edge: object) -> None:
        """
        Adds outgoing edge.
        """
        self._out_edges_a.append(edge)

    def deg(self, count_self_loop: bool = True) -> tuple | int:
        """
        Returns the degree of the vertex.
        If the graph is directed returns a tuple containing the in and out degrees.
        If the graph is not directed returns an int.
        """
        if self._directional_graph:
            if count_self_loop:
                deg = tuple([len(self._in_edges_a), len(self._out_edges_a)])
            else:
                deg = tuple([sum([1 if not edge.is_self_loop else 0 for edge in self._in_edges_a]),
                             sum([1 if not edge.is_self_loop else 0 for edge in self._out_edges_a])])
        else:
            if count_self_loop:
                deg = len(self._edges_a)
            else:
                deg = sum([1 if not edge.is_self_loop else 0 for edge in self._edges_a])
        return deg

    def weight_deg(self, count_self_loop: bool = True) -> tuple:
        """
        Returns the summed weight of all edges to the vertex.
        """
        if self._directional_graph:
            if count_self_loop:
                deg = tuple([sum([i.weight for i in self._in_edges_a]),
                             sum([i.weight for i in self._out_edges_a])])
            else:
                deg = tuple([sum([i.weight for i in self._in_edges_a if not i.is_self_loop]),
                             sum([i.weight for i in self._out_edges_a if not i.is_self_loop])])
        else:
            if count_self_loop:
                deg = tuple([sum([i.weight for i in self._edges_a])])
            else:
                deg = tuple([sum([i.weight for i in self._edges_a if not i.is_self_loop])])
        return deg

    def is_adjacent_to(self, vertex: object) -> bool:
        """
        Whether the given vertex is adjacent to self.
        """
        check = False
        for edge in self._edges_a:
            if edge.is_connected_to(vertex):
                check = True
                break
        return check
