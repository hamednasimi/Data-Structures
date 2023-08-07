Currently supports the very basic functionalities and attributes of a graph.

Usage:

```python
from graph import Graph
# There are two ways of creating a graph:
# 1. Initiate the empty graph and create the vertices and edges later on
G = Graph()
# Add vertices and edges manually and save a reference to them
vertex1 = G.vertex() # Add an isolated vertex
vertex2 = G.vertex()
edge1 = G.edge(vertex1, vertex2) # | G.edge(v1, v2)

# 2. Initiate the graph using a vertex and edge set / binary relation
G = Graph([0, 1, 2, 3, 4, 5], [(1, 2), (1, 3), (4, 3), (0, 1)])
    
# Working with vertices and edges:
# Accessing unreferenced vertices
v1 = G.v(1) # References the vertex object itself
v2 = G[0] # Indexing the graph object returns the vertex at the index

# Accessing unreferenced edges:
G.e(1, 2) # References the edge objects connecting vertex 1 and vertex 2 if they exist. returns a list of edges
e1 = G.e(v1, v2)[0] # is also possible

# Removing a vertex
G.remove_vertex(5) # Matrix representations of the graph will keep the entry for the removed vertex but the vertex is not referenceable

# Removing an edge
G.remove_edge(G.e(1, 2)[0]) # The argument must be an edge object reference

# Setting a vertex value which can be any object
v1.value = 42
v2.value = [420, 69]

# Degree of a vertex
print("Degree of 0: ", G.deg(0))

# Distance of two vertices
print("Distance of 2 and 1: ", G.d(2, v1))

print("==========")
# Representations
print(G) # Prints out the adjacency matrix
# or simply call G in jupyter

# You can use the pyvis extension to visualize the graph and edges
from Utils.visualization import Visualization
Visualization(G) # Generates an html file

# To get all vertices
print("Vertices: ", G.vertices)

# To get all edges
print("Edges: " , G.edges)

# Get the distance matrix
print("Distance matrix: ", G.distance_matrix) # Currently works only for simple graphs. Updates all the distances on every call

# Degree sequence
print("Degree sequence: ", G.degree_sequence)

print("==========")
# Attributes
# Whether the graph is simple
print("Is Simple: ", G.is_simple)

# Whether edges in the graph have weights other than 1 and 0 (updated by self.connect())
print("Is Weighted: ", G.is_weighted)

# Whether every vertex in the graph has at least one edge to every other vertex other than to itself
print("Is Complete: ", G.is_complete)

# Whether the graph has at least one pendent vertex
print("Has Pendent: ", G.has_pendent)

# Whether the graph has at least one isolated vertex
print("Has Isolated: ", G.has_isolated)

# Whether any two vertices have parallel edges
print("Is Multigraph: ", G.is_multigraph)

# Whether the graph has at least one self-loop
print("Has Self-loop: ", G.has_self_loop)
```