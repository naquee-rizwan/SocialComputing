import snap
from graph import Graph


class Graph3(Graph):
    def __init__(self):
        super().__init__()
        # Generate a network using Forest Fire model
        self.graph = snap.GenForestFire(1000, 0.35, 0.35)
        self.text_file_loaded_graph = None
        self.binary_file_loaded_graph = None

    def save_graph_as_binary(self):
        f_out = snap.TFOut("forest_fire_network.graph")
        self.graph.Save(f_out)
        f_out.Flush()

    def load_graph_from_binary(self):
        f_in = snap.TFIn("forest_fire_network.graph")
        self.binary_file_loaded_graph = snap.TNGraph.Load(f_in)
        self.print_nodes_and_edges(self.binary_file_loaded_graph)

    def save_graph_as_text_file(self):
        self.binary_file_loaded_graph.SaveEdgeList("forest_fire_network.txt", "Save as tab-separated list of edges")

    def load_graph_from_text_file(self):
        self.text_file_loaded_graph = snap.LoadEdgeList(snap.TNGraph, "forest_fire_network.txt", 0, 1)
        self.print_nodes_and_edges(self.text_file_loaded_graph)
