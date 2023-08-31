import snap


class Graph:
    def print_details_of_graph(self, graph):
        print("Graph: Nodes %d, Edges %d" % (graph.GetNodes(), graph.GetEdges()))

        # Traverse the nodes
        for NI in graph.Nodes():
            print("Node id %d with out-degree %d and in-degree %d" % (
                NI.GetId(),
                NI.GetOutDeg(),
                NI.GetInDeg()
            ))

        print("--------------------------------------------------")

        # Traverse the edges
        for EI in graph.Edges():
            print("Edge (%d, %d)" % (EI.GetSrcNId(), EI.GetDstNId()))

        print("--------------------------------------------------")

        # Traverse the edges by nodes
        for NI in graph.Nodes():
            for Id in NI.GetOutEdges():
                print("Edge (%d, %d)" % (NI.GetId(), Id))

        print("--------------------------------------------------")

        # Traverse the edges by nodes
        # TODO - Yet to verify whether this implementation is correct or not
        for NI in graph.Nodes():
            for Id in NI.GetInEdges():
                print("Edge (%d, %d)" % (Id, NI.GetId()))

        print("--------------------------------------------------")
        print("--------------------------------------------------")


class Graph_1(Graph):
    def __init__(self):
        # Create a graph PNGraph
        self.graph = snap.TNGraph.New()
        self.graph.AddNode(1)
        self.graph.AddNode(5)
        self.graph.AddNode(32)
        self.graph.AddEdge(1, 5)
        self.graph.AddEdge(5, 1)
        self.graph.AddEdge(5, 32)


class Graph_2:
    def __init__(self):
        # Create a directed random graph on 100 nodes and 1k edges
        self.graph = snap.GenRndGnm(snap.TNGraph, 100, 1000)


def intro(show_output_for=1):

if __name__ == "__main__":
    intro()
