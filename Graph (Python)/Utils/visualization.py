from pyvis.network import Network
from graph import Graph


class Visualization:

    def __init__(self, graph: object):
        """Visualizes the graph."""
        if graph is None:
            raise RuntimeError("The graph parameter must be provided.")
        if isinstance(graph, Graph):
            directed = False
        else:
            directed = True
        self.sketch = Network(notebook=True, directed=directed, cdn_resources="remote")
        for vertex in graph.vertices:
            self.sketch.add_node(n_id=vertex.index, label=str(vertex.index), shape="circle",)
        for edge in graph.edges:
            self.sketch.add_edge(edge.connected_to[0].index, edge.connected_to[1].index)
        self.sketch.show("Graph.html")
        # TODO show all of the graph details in a separate node

    def update(self):
        """Use if you've changed any parameters of the graph components."""
        self.sketch.show("Graph.html")
