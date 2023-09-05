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
