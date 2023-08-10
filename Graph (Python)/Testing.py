from graph import Graph
v = int(input())
e = int(input())
G = Graph(vertices=[i for i in range(v)], edges=[(int(input()), int(input())) for e in range(e)])
from Utils.visualization import Visualization
Visualization(G)
print("YES") if G.is_complete else print("NO")
