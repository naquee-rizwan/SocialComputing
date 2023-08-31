import snap

line_separator = "--------------------------------------------------"


class Graph:
    def __init__(self, graph):
        self.graph = graph

    def print_details_of_graph(self):
        print("Graph: Nodes %d, Edges %d" % (self.graph.GetNodes(), self.graph.GetEdges()))

        print(line_separator)

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
            print("Edge (%d, %d)" % (EI.GetSrcNId(), EI.GetDstNId()))

        print(line_separator)

        # Traverse the edges by nodes
        for NI in self.graph.Nodes():
            for Id in NI.GetOutEdges():
                print("Edge (%d, %d)" % (NI.GetId(), Id))

        print(line_separator)

        # Traverse the edges by nodes
        # TODO - Yet to verify whether this implementation is correct or not
        for NI in self.graph.Nodes():
            for Id in NI.GetInEdges():
                print("Edge (%d, %d)" % (Id, NI.GetId()))

        print(line_separator)


class Graph2(Graph):
    def __init__(self):
        # Create a directed random graph on 100 nodes and 1k edges
        self.graph = snap.GenRndGnm(snap.TNGraph, 100, 1000)
        super().__init__(self.graph)


class Graph1(Graph):
    def __init__(self):
        # Create a graph PNGraph
        self.graph = snap.TNGraph.New()
        self.graph.AddNode(1)
        self.graph.AddNode(5)
        self.graph.AddNode(32)
        self.graph.AddEdge(1, 5)
        self.graph.AddEdge(5, 1)
        self.graph.AddEdge(5, 32)
        super().__init__(self.graph)


def intro(show_output_for=1):
    if show_output_for == 1:
        graph = Graph1()
    elif show_output_for == 2:
        graph = Graph2()
    graph.print_details_of_graph()


if __name__ == "__main__":
    intro(2)
