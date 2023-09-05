from examplegraph import Graph1, Graph2, Graph3, Graph4, Graph5


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
