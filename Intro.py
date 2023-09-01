import snap

line_separator = "--------------------------------------------------"
new_line_separator = "\n" + line_separator + "\n"


class Graph:
    def __init__(self):
        self.graph = None

    @staticmethod
    def print_nodes_and_edges(generic_graph, output_string="Graph"):
        if len(output_string) > 0:
            print(output_string, end=" - ")

        print("Nodes %d, Edges %d" % (generic_graph.GetNodes(), generic_graph.GetEdges()),
              end=new_line_separator)

    def print_details_of_graph(self):
        self.print_nodes_and_edges(self.graph)

        # Traverse the nodes
        for NI in self.graph.Nodes():
            print("Node id %d with out-degree %d and in-degree %d" % (
                NI.GetId(),
                NI.GetOutDeg(),
                NI.GetInDeg()
            ))

        print(line_separator)

        # Traverse the edges
        for EI in self.graph.Edges():
            print("Edge (%d, %d)" % (
                EI.GetSrcNId(),
                EI.GetDstNId()
            ))

        print(line_separator)

        # Traverse the edges by nodes
        for NI in self.graph.Nodes():
            for Id in NI.GetOutEdges():
                print("Edge (%d, %d)" % (NI.GetId(), Id))

        print(line_separator)

        # Traverse the edges by nodes
        for NI in self.graph.Nodes():
            for Id in NI.GetInEdges():
                print("Edge (%d, %d)" % (Id, NI.GetId()))

        print(line_separator)


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


class Graph2(Graph):
    def __init__(self):
        super().__init__()
        # Create a directed random graph on 100 nodes and 1k edges
        self.graph = snap.GenRndGnm(snap.TNGraph, 100, 1000)


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


class IntroHelper:
    def __init__(self, show_output_for):
        self.graph = None
        self.show_output_for = show_output_for

    def intro(self):
        if self.show_output_for == 1:
            self.graph = Graph1()
        elif self.show_output_for == 2:
            self.graph = Graph2()
        elif self.show_output_for == 3:
            self.graph = Graph3()
        elif self.show_output_for == 4:
            self.graph = Graph4()
        elif self.show_output_for == 5:
            self.graph = Graph5()

        if self.show_output_for == 1 or self.show_output_for == 2:
            self.graph.print_details_of_graph()

        if self.show_output_for == 3:
            self.graph.print_nodes_and_edges(self.graph.graph)
            self.graph.save_graph_as_binary()
            self.graph.load_graph_from_binary()
            self.graph.save_graph_as_text_file()
            self.graph.load_graph_from_text_file()

        if self.show_output_for == 4:
            self.graph.print_nodes_and_edges(self.graph.graph)
            self.graph.perform_operations()

        if self.show_output_for == 5:
            self.graph.print_nodes_and_edges(self.graph.graph)
            self.graph.perform_operations()


if __name__ == "__main__":
    IntroHelper(show_output_for=5).intro()
