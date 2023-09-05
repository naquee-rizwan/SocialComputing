import snap
from graph import Graph
from plot import Plot


class Graph2(Graph):
    def __init__(self):
        super().__init__()
        # Create a directed random graph on 100 nodes and 1k edges
        self.graph = snap.GenRndGnm(snap.TNGraph, 100, 1000)
        graph_plot = Plot()
        graph_plot.update_graph(self.graph)
        graph_plot.draw_graph_viz("graph2", "Graph 2")
