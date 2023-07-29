Currently supports the very basic functionalities and attributes of a graph.

Usage:

```python

# 1. Initiate the empty graph and create the vertices and edges later on.
    G = Graph()
    # Add vertices and edges manually and save a reference to them
    v1 = G.vertex() # Add an isolated vertex
    v2 = G.v() 
    e1 = G.edge(v1, v2) # | e1 = v1.v2 | G.edge(v1, v2)
    
# 2. Initiate the graph using a vertex and edge set / binary relation
    G = Graph({1, 2, 3, 4}, [(1, 2), (1, 3), (4, 3)])
    
# ___
    # Access unreferenced vertices
    G.v(1) # references the vertex object itself so...
    v1 = G.v(1) # is also possible
    
    # Accessing unreferenced edges:
    G.e(1, 2) # references the edge objects connecting vertex 1 and vertex 2 if they exist. returns a tuple of edges
    e1 = G.e(v1, v2) # is also possible

```