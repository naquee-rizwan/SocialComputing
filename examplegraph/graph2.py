import snap
from graph import Graph


class Graph2(Graph):
    def __init__(self):
        super().__init__()
        # Create a directed random graph on 100 nodes and 1k edges
        self.graph = snap.GenRndGnm(snap.TNGraph, 100, 1000)
