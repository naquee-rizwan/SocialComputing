import snap
from graph import Graph
from plot import Plot


class Graph1(Graph):
    def __init__(self):
        super().__init__()
        # Create a graph PNGraph
        self.graph = snap.TNGraph.New()
        self.graph.AddNode(1)
        self.graph.AddNode(5)
        self.graph.AddNode(32)
        self.graph.AddEdge(1, 5)
        self.graph.AddEdge(5, 1)
        self.graph.AddEdge(5, 32)
        graph_plot = Plot()
        graph_plot.update_graph(self.graph)
        graph_plot.draw_graph_viz("graph1", "Graph 1")
        graph_plot.draw_gun_plot("graph1", "Graph 1")

