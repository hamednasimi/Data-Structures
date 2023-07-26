from Direction import Direction
def TODO():
    NotImplementedError()

# TODO Add a Vertex class and move the vertex methods to it
# TODO Add an Edge class and move the vertex methods to it
# TODO Add @property methods

class Graph:
    '''
    Provides the fundamental functionalities and attributes for directed and undirected graphs. Mixed graphs are not supported yet.
    '''

    '''
    |=============================|===============|=============================|
    |=============================| GRAPH METHODS |=============================|
    |=============================|===============|=============================|
    '''

    def __init__(self, vertices, edges=-1, directed=False, auto_update=True) -> object:
        
        assert vertices >= 1, "There must be at least one vertex."

        # Initializations
        self._vertices: int = vertices # The number of vertices
        self._edges: int = edges # The number of edges
        self._is_directed: Direction = directed # Whether edges in the graph are directed OR there are individual directed edges
        self._auto_update: bool = auto_update # Whether to update the primary attributes automatically after each new vertex/edge addition

        # Primary variable Attributes
        self._is_simple: bool = None # No vertex in the graph has any edge to itself
        self._is_weighted: bool = False # Whether edges in the graph have weights other than 1 and 0 (updated by self.connect())
        self._is_complete: bool = None # Whether every vertex in the graph has at least one edge to every other vertex other than to itself
        self._has_pendent: bool = None # Whether the graph has at least one pendent vertex
        self._has_isolated: bool = None # Whether the graph has at least one isolated vertex
        self._is_multigraph: bool = None # Whether any two vertices have parallel edges
        self._representation: str = "" # The main string representaion for str() and print()
        if self._is_directed == False:
            self._degree_sequence: list = []
        elif self._is_directed == True:
            self._in_degree_sequence: list = []
            self._out_degree_sequence: list = []
            
        # Secondary variable Attributes
        self._is_wheel: bool = None
        
        # Matrix representation attributes
        self._adjacency_matrix: list = [[0 for i in range(self._vertices)] for j in range(self._vertices)]
        self._distance_matrix: list = [[0 for i in range(self._vertices)] for j in range(self._vertices)]

    # Dunder methods
    
    def __str__(self) -> str:
        '''The main string representaion for str() and print().'''
        self._representation = ""
        for i in range(self._vertices):
            for j in range(self._vertices):
                self._representation += str(self._adjacency_matrix[i][j])
                self._representation += " "
            self._representation += ("\n") if i != self._vertices - 1 else ""
        return self._representation
    
    def __repr__(self):
        return self.__str__()
    
    def __getitem__(self, v) -> dict | int | float:
        '''Returns the row[v] of the adjacency matrix in the given index locations.'''
        return self._adjacency_matrix[v]
    
    # Properties
    
    @property
    def vertices(self) -> int:
        '''The number of vertices in the graph.'''
        return self._vertices

    @property
    def edges(self) -> int:
        '''The number of edges in the graph.'''
        return self._edges

    @property
    def directed(self) -> bool:
        '''Returns True if the graph is directed.'''
        return self._is_directed

    @property
    def digraph(self) -> bool:
        '''Returns True if the graph is a digraph.'''
        return self._is_directed

    @property
    def auto_update(self) -> bool:
        '''Returns True if the graph is on auto-update mode.'''
        return self._auto_update

    @property
    def is_simple(self) -> bool:
        '''Returns True if the graph is simple.'''
        return self._is_simple

    @property
    def is_weighted(self):
        '''Returns True if the graph is weighted.'''
        return self._is_weighted

    @property
    def is_complete(self):
        '''Returns True if the graph is complete.'''
        return self._is_complete

    @property
    def has_pendent(self):
        '''Returns True if the graph has at least one pendent vertex.'''
        return self._has_pendent

    @property
    def has_isolated(self):
        '''Returns True if the graph has at least one isolated vertex.'''
        return self._has_isolated

    @property
    def is_multigraph(self):
        '''Returns True if the graph is a multigraph.'''
        return self._is_multigraph

    @property
    def degree_sequence(self):
        '''
        Returns the degree sequence as a list.
        If the graph is weighted a tuple of two lists for in and out degrees will be returned.
        '''
        if self._is_weighted:
            return (self._in_degree_sequence, self._out_degree_sequence)
        else:
            return self._degree_sequence

    @property
    def is_wheel(self):
        '''Returns True if the graph is a wheel.'''
        return self._is_wheel

    @property
    def adjacency_matrix(self):
        '''Returns the adjacency matrix in 2D list / matrix form.'''
        return self._adjacency_matrix

    @property
    def distance_matrix(self):
        '''Returns the distance matrix in 2D list / matrix form.'''
        return self._distance_matrix
    
    # Update
    
    def update(self, all_=False) -> None:
        '''
        Updates graph attributes.
        By default it updates the primary attributes only. To update all (including self.is_wheel()), use all=True.
        Whether the graph is weighted or not is checked by self.connect()
        '''
        self.check_if_simple()
        self.check_if_complete()
        self.check_for_pendent()
        self.check_for_isolated()
        self.check_if_multigraph()
        
        if all_:
            self._is_wheel()
        
    # Primary Attributes
        
    def check_if_simple(self) -> bool:
        '''
        Returns True if the graph is simple.\n
        A simple graph is unweighted, has no self-loops and has no parallel edges.
        '''
        self._is_simple = (not self.is_weghted) and (not self.check_for_self_loop()) and (not self.is_multigraph)
        return self._is_simple
    
    def check_if_complete(self) -> bool:
        '''Whether every vertex in the graph has at least one edge to every other vertex except for itself'''
        self._is_complete = True
        for v in range(self._vertices):
            if not (self.deg(v) == self._vertices - 1 and not self.loop(v)):
                self._is_complete = False
                break
        return self._is_complete

    def check_for_pendent(self, which=False) -> bool | list:
        '''Whether the graph has a pendent / leaf vertex.'''
        self._has_pendent = False
        pendents = []
        for v in range(self._vertices):
            if self.is_pendent(v):
                self._has_pendent = True
                pendents.append(v)
        if which:
            return pendents
        else:
            return self._has_pendent

    def check_for_isolated(self, which=False) -> bool | list:
        '''Returns True if the graph has any isolated vertex.'''
        self._has_isolated = False
        isolated = []
        for v in range(self._vertices):
            if self.is_isolated(v):
                isolated.append(v)
                self._has_isolated = True
        if which:
            return isolated
        else:
            return self._has_isolated
        
    def check_for_self_loop(self, which=False):
        '''Returns True if the graph has at least one self-loop.'''
        check = False
        self_loops = []
        for v in range(self._vertices):
            if self.loop(v):
                check = True
                self_loops.append(v)
        if which:
            return self_loops
        else:
            return check

    def check_if_multigraph(self) -> bool:
        '''Whether the graph is a multigraph (has at least one parallel edge).'''
        TODO()
        
    def update_degree_sequence(self, sort=False, descending=False):
        if not self._is_directed:
            self._degree_sequence = [self.deg(v) for v in range(self._vertices)]
        else:
            self._in_degree_sequence = [self.deg(v, Direction=Direction.IN) for v in range(self._vertices)]
            self._out_degree_sequence = [self.deg(v, Direction=Direction.OUT) for v in range(self._vertices)]
        if sort:
            self._degree_sequence.sort(reverse=descending)
    # Secondary attributes
    
    def _is_wheel(self) -> bool:
        '''Whether the graph is a wheel (if every vertex has a degree of 3 except for one which has a degree of v - 1)'''
        TODO()
    
    # Other methods
    
    def extend(self) -> None:
        TODO()
        
    '''
    |=============================|================|=============================|
    |=============================| VERTEX METHODS |=============================|
    |=============================|================|=============================|
    '''

    def connect(self, v1, v2, value=1) -> None:
        '''Establish a connection between the two given vertices.'''
        assert 0 <= v1 < self._vertices and 0 <= v2 < self._vertices, "vertex out of range."
        if not self._is_weighted and value != 1:
            self.is_weghted = True
        if self._is_directed == False:
            self._adjacency_matrix[v1][v2] = value
            self._adjacency_matrix[v2][v1] = value
        elif self._is_directed == True:
            self._adjacency_matrix[v1][v2] = value
        if self._auto_update:
            self.update()

    def deg(self, v, direction=Direction.BOTH, count_self_loop=True, cumulative=True) -> int | float | tuple:
        '''
        Returns the number of edges connected to the given vertex.\n
        The function assumes that each vertex can have 1 self-loop at most.
        '''
        assert v >= 0 and v < self._vertices, "the given vertex index is out of bounds."
        deg = 0
        if self._is_directed == False:
            deg = sum([1 if i > 0 else 0 for i in self._adjacency_matrix[v]])
        elif self._is_directed == True:
            if direction == Direction.IN:
                deg = sum([1 if i > 0 else 0 for i in [i[v] for i in self._adjacency_matrix]])
            elif direction == Direction.OUT:
                deg = sum([1 if i > 0 else 0 for i in self._adjacency_matrix[v]])
            elif direction == Direction.BOTH:
                if cumulative:
                    deg = sum([1 if i > 0 else 0 for i in [i[v] for i in self._adjacency_matrix]]) +\
                        sum([1 if i > 0 else 0 for i in self._adjacency_matrix[v]])
                elif not cumulative:
                    deg = (sum([1 if i > 0 else 0 for i in [i[v] for i in self._adjacency_matrix]]),\
                        sum([1 if i > 0 else 0 for i in self._adjacency_matrix[v]]))
        if not count_self_loop and self._adjacency_matrix[v][v] > 0:
            if direction != Direction.BOTH:
                deg -= 1
            elif direction == Direction.BOTH:
                if cumulative:
                    deg -= 2
                else:
                    deg = (deg[0] - 1, deg[1] - 1)
        return deg

    def deg_by_value(self, v, direction=Direction.BOTH, count_self_loop=True, cumulative=False) -> int | float | tuple:
        '''
        Returns the value of edges connected to the given vertex.\n
        The function assumes that each vertex can have 1 self-loop at most.
        '''
        assert v >= 0 and v < self._vertices, "the given vertex index is out of bounds."
        deg = 0
        if self._is_directed == False:
            deg = sum(self._adjacency_matrix[v])
        elif self._is_directed == True:
            if direction == Direction.IN:
                deg = sum([i[v] for i in self._adjacency_matrix])
            elif direction == Direction.OUT:
                deg = sum(self._adjacency_matrix[v])
            elif direction == Direction.BOTH:
                if cumulative:
                    deg = sum([i[v] for i in self._adjacency_matrix]) + sum(self._adjacency_matrix[v])
                elif not cumulative:
                    deg = (sum([i[v] for i in self._adjacency_matrix]), sum(self._adjacency_matrix[v]))
        if not count_self_loop and self._adjacency_matrix[v][v] > 0:
            if direction != Direction.BOTH:
                deg -= self._adjacency_matrix[v][v]
            elif direction == Direction.BOTH:
                if cumulative:
                    deg -= (2 * self._adjacency_matrix[v][v])
                else:
                    deg = (deg[0] - self._adjacency_matrix[v][v], deg[1] - self._adjacency_matrix[v][v])
        return deg

    def is_pendent(self, v) -> bool:
        '''Whether the given vertex is pendent (there is only 1 edge connected to the vertex. A self-looping vertex is not pendent).'''
        return self.deg(v, count_self_loop=False) == 1

    def is_isolated(self, v) -> bool:
        '''Whether there are no edges connected to it.'''
        return self.deg(v, count_self_loop=False) == 0
    
    def loop(self, v) -> bool:
        '''Whether the given vertex has a self-loop edge.'''
        return self._adjacency_matrix[v][v] > 0

    def d(self, v1, v2) -> int | float:
        '''Returns the shortest distance between the two given vertices.'''
        TODO()

    def are_adjacent(self, v1, v2) -> bool:
        '''Whether the two given vertices are adjacent.'''
        return self._adjacency_matrix[v1][v2] > 0 or self._adjacency_matrix[v2][v1] > 0

    '''
    |=============================|==============|=============================|
    |=============================| EDGE METHODS |=============================|
    |=============================|==============|=============================|
    '''

    def are_adjacent(self, e1, e2) -> bool:
        '''Whether the two given edges are adjacent.'''
        TODO()

    def are_parallel(self, e1, e2) -> bool:
        '''Whether the two given edges are parallel.'''
        TODO()
