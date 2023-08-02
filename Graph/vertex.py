from edge import Edge

# TODO make the vertex be able to hold instances of other objects as value and be able to
# apply functions to them or call their methods
# -> v.apply(function=func, *args): v.func(*args)
# or for each adjacent vertex, apply a function to them

class Vertex:
    """Represents a vertex in a graph."""
        
    # Dunder methods

    def __init__(self, index:int, value:object=None):
        
        assert isinstance(index, int), "The index must be of type int."
        
        # Attributes
        self._index: int = index
        self._value: any = value
        self.edges_a: list = []
        self.in_edges_a: list = []
        self.out_edges_a: list = []
        
    def __str__(self):
        return f"{self._index}"
        
    def __repr__(self):
        return self.__str__()
    
    def __del__(self):
        self._index = None
        del self._value
        self._value = None
    
    def __lt__(self, other): # <
        return self._index < other.index
    def __le__(self, other): # <=
        return self._index <= other.index
    def __eq__(self, other): # ==
        return self is other
    def __ne__(self, other): # !=
        return self is not other
    def __gt__(self, other): # >
        return self._index > other.index
    def __ge__(self, other): # >=
        return self._index >= other.index
    
    # Properties
    
    @property
    def index(self):
        """Returns the index of the vertex in the vertex set."""
        return self._index
    
    @index.setter
    def index(self, new_index):
        """Sets the index of the vertex to the new value."""
        self._index = new_index
    
    @property
    def value(self):
        """Returns the value of the vertex."""
        return self._value
    
    @value.setter
    def value(self, value):
        """Sets the value of the vertex"""
        self._value = value
    
    @value.deleter
    def value(self):
        """Deletes the value of the vertex. Sets it to None."""
        self._value = None
        
    @property
    def edges(self):
        """Returns a list of all edges that are connected to the vertex."""
        return self.edges_a
        
    @property
    def in_edges(self):
        """Returns a list of all edges that are connected to the vertex."""
        return self.in_edges_a
        
    @property
    def out_edges(self):
        """Returns a list of all edges that are connected to the vertex."""
        return self.out_edges_a
    
    # Instance methods
    
    def add_edge(self, edge:object):
        """Connects the vertex to the given edge."""
        self.edges_a.append(edge)
    
    def add_in_edge(self, edge:object):
        """Adds incoming edge."""
        self.in_edges_a.append(edge)
    
    def add_out_edge(self, edge:object):
        """Adds outgoing edge."""
        self.out_edges_a.append(edge)
        
    # Private methods

    
    
    # Class / static methods
    
