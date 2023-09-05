import snap
from graph import Graph


class Graph4(Graph):
    def __init__(self):
        super().__init__()
        # Generate a network using Forest Fire model
        self.graph = snap.GenForestFire(1000, 0.35, 0.35)

    def perform_operations(self):
        # Convert to undirected graph
        undirected_graph = self.graph.ConvertGraph(snap.TUNGraph)
        self.print_nodes_and_edges(undirected_graph, "Undirected graph")

        # Get largest weakly connected component of graph
        weakly_connected_component = self.graph.GetMxWcc()
        self.print_nodes_and_edges(weakly_connected_component, "Weakly connected component")

        # Get a subgraph induced on nodes {0,1,2,3,4,5}
        sub_graph = self.graph.GetSubGraph([0, 1, 2, 3, 4])
        self.print_nodes_and_edges(sub_graph, "Sub Graph")

        # Get 3-core of graph
        three_core_of_graph = self.graph.GetKCore(3)
        self.print_nodes_and_edges(three_core_of_graph, "3-core of graph")

        # Delete nodes of out degree 10 and in degree 5
        self.graph.DelDegKNodes(10, 5)
        self.print_nodes_and_edges(self.graph, "Graph after nodes deletion")