from edge import Edge

class DirectedEdge(Edge):
    
    # Dunder methods
    
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
    
    
    
    # Instance methods
    
    
    
    # Class methods
    
    
    
    