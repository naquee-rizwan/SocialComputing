import snap
from graph import Graph
from plot import Plot

line_separator = "--------------------------------------------------"


class Graph5(Graph):
    def __init__(self):
        super().__init__()
        # Generate a Preferential Attachment graph on 1000 nodes and node out degree of 3
        self.graph = snap.GenPrefAttach(10, 3)
        graph_plot = Plot()
        graph_plot.update_graph(self.graph)
        graph_plot.draw_graph_viz("graph5", "Graph 5")

    def perform_operations(self):
        # Get distribution of connected components (component size, count)
        connected_components_distribution = self.graph.GetWccSzCnt()

        for pairs in connected_components_distribution:
            print(pairs.GetVal1(), pairs.GetVal2())

        print(line_separator)

        # Get degree distribution pairs (degree, count)
        degree_distribution_pairs = self.graph.GetOutDegCnt()
        for pairs in degree_distribution_pairs:
            print(pairs.GetVal1(), pairs.GetVal2())

        print(line_separator)

        # Get first eigenvector of graph's adjacency matrix
        eigen_value = self.graph.GetLeadEigVec()
        print(len(eigen_value))
        for value in eigen_value:
            print(value)

        print(line_separator)

        # Get diameter of graph
        diameter = self.graph.GetBfsFullDiam(100)
        print("Diameter -", diameter)

        print(line_separator)

        # Count the number of triads in graph and get the clustering coefficient of graph
        print("Triads -", self.graph.GetTriads())

        print(line_separator)

        print("Clustering Coefficient -", self.graph.GetClustCf())

        print(line_separator)
