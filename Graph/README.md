Currently supports the very basic functionalities and attributes of a graph.

Usage:

```python

G = Graph(3, 2) # 3 vertices and 2 edges

G.connect(0, 1)
G.connect(1, 2)

print(G.adjacency_matrix)
print(G.is_simple)

```