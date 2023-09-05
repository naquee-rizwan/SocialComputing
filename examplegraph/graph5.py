import snap
from graph import Graph


class Graph5(Graph):
    def __init__(self):
        super().__init__()
        # Generate a Preferential Attachment graph on 1000 nodes and node out degree of 3
        self.graph = snap.GenPrefAttach(1000, 3)

    def perform_operations(self):
        # TODO - Not understood
        # Get distribution of connected components (component size, count)
        connected_components_distribution = self.graph.GetWccSzCnt()
        print("Connected components distribution -", connected_components_distribution)

        # TODO - Not understood
        # Get degree distribution pairs (degree, count)
        degree_distribution_pairs = self.graph.GetOutDegCnt()
        print("Degree distribution pairs -", degree_distribution_pairs)

        # TODO - Not understood
        # Get first eigenvector of graph's adjacency matrix
        eigen_value = self.graph.GetLeadEigVec()
        print("Eigen value -", eigen_value)

        # Get diameter of graph
        diameter = self.graph.GetBfsFullDiam(100)
        print("Diameter -", diameter)

        # Count the number of triads in graph and get the clustering coefficient of graph
        print("Triads -", self.graph.GetTriads())
        print("Clustering Coefficient -", self.graph.GetClustCf())
