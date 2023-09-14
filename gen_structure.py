import sys
import snap
import os
import matplotlib.pyplot as plt


class GenStructure:

    def __init__(self):
        self.undirected_graph = snap.TUNGraph.New()
        self.rounding_factor = 4

        self.rnd = snap.TRnd(42)
        self.rnd.Randomize()

        self.plots_directory_path = 'plots'

        edge_list_file_path = sys.argv[1]
        self.subgraph_name = edge_list_file_path.split('/')[-1].split('.')[0]
        self.edge_list_file = open(edge_list_file_path, 'r')
        self.construct_graph()
        self.edge_list_file.close()

    def plot_graph(self, file_name, _dictionary: {}, x_label, y_label, title):
        plot_filedir = os.path.join(self.plots_directory_path, file_name)

        plt.figure()
        plt.title(title)
        plt.scatter(list(_dictionary.keys()), list(_dictionary.values()), s=10)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.savefig(plot_filedir)

    def add_node_to_graph(self, node):
        try:
            self.undirected_graph.AddNode(int(node))
        except RuntimeError:
            # print("Runtime Exception encountered while adding duplicated node")
            pass

    def add_edge_to_graph(self, node_1, node_2):
        self.undirected_graph.AddEdge(int(node_1), int(node_2))

    def construct_graph(self):
        for nodes in self.edge_list_file:
            self.add_node_to_graph(nodes.split()[0])
            self.add_node_to_graph(nodes.split()[1])
            self.add_edge_to_graph(nodes.split()[0], nodes.split()[1])

    def print_number_of_nodes_and_edges(self):
        print("Number of nodes:", self.undirected_graph.GetNodes())
        print("Number of edges:", self.undirected_graph.GetEdges())

    def print_number_of_nodes_with_given_degree(self):
        print("Number of nodes with degree=7:", snap.CntOutDegNodes(self.undirected_graph, 7))

    def print_nodes_with_maximum_degree(self):
        out_deg = snap.TIntPrV()
        snap.GetNodeOutDegV(self.undirected_graph, out_deg)
        max_degree = -1
        max_deg_nodes = []
        for item in out_deg:
            if max_degree < item.GetVal2():
                max_deg_nodes = [item.GetVal1()]
                max_degree = item.GetVal2()
            elif max_degree == item.GetVal2():
                max_deg_nodes.append(item.GetVal1())

        print("Node id(s) with highest degree:", end=' ')
        length_of_list = len(max_deg_nodes)
        for index, nodes in enumerate(max_deg_nodes):
            if index == length_of_list - 1:
                print(nodes)
            else:
                print(str(nodes) + ", ", end=' ')

    def plot_degree_distribution(self):
        deg_to_cnt = snap.TIntPrV()
        snap.GetOutDegCnt(self.undirected_graph, deg_to_cnt)
        degree_count = {}
        for item in deg_to_cnt:
            degree_count[item.GetVal1()] = item.GetVal2()

        self.plot_graph(
            'deg_dist_' + self.subgraph_name + '.png',
            degree_count,
            "Degree",
            "Nodes",
            "Degree Distribution ({})".format(self.subgraph_name)
        )

    def print_approximate_full_diameter(self):
        print("Approximate full diameter:", snap.GetBfsFullDiam(self.undirected_graph, 1000, False))

    def print_approximate_effective_diameter(self):
        print("Approximate effective diameter:", round(
            snap.GetBfsEffDiam(self.undirected_graph, 1000, False),
            self.rounding_factor
        ))

    def plot_short_path_lengths_distribution_in_network(self):

        shortest_path_dist = {}
        for node_id in self.undirected_graph.Nodes():
            dictionary = snap.TIntH()
            snap.GetShortPath(self.undirected_graph, node_id.GetId(), dictionary)
            for item in dictionary:
                item_ = dictionary[item]
                if item_ in shortest_path_dist:
                    shortest_path_dist[item_] += 1
                else:
                    shortest_path_dist[item_] = 1

        self.plot_graph(
            'shortest_path_' + self.subgraph_name + '.png',
            shortest_path_dist,
            "Shortest Path Length",
            "Frequency",
            "Shortest Path Distribution ({})".format(self.subgraph_name)
        )

    def print_fraction_of_nodes_in_largest_connected_component(self):
        print("Fraction of nodes in largest connected component:", round(
            snap.GetMxScc(self.undirected_graph).GetNodes() / self.undirected_graph.GetNodes(), self.rounding_factor
        ))

    def print_number_of_bridges(self):
        print("Number of edge bridges:", len(self.undirected_graph.GetEdgeBridges()))

    def print_number_of_articulation_points(self):
        print("Number of articulation points:", len(self.undirected_graph.GetArtPoints()))

    def plot_distribution_of_size_of_connected_components(self):
        connected_component = snap.TIntPrV()
        snap.GetSccSzCnt(self.undirected_graph, connected_component)
        connected_component_dictionary = {}
        for component in connected_component:
            connected_component_dictionary[component.GetVal1()] = component.GetVal2()

        self.plot_graph(
            'connected comp_' + self.subgraph_name + '.png',
            connected_component_dictionary,
            "Size of Connected Components",
            "Components",
            "Connected Component Distribution ({})".format(self.subgraph_name)
        )

    def print_average_clustering_coefficient(self):
        print("Average clustering coefficient:", round(
            snap.GetClustCf(self.undirected_graph, -1),
            self.rounding_factor
        ))

    def print_number_of_triads(self):
        print("Number of triads:", snap.GetTriads(self.undirected_graph, -1))

    def print_clustering_coefficient_of_randomly_selected_node(self):
        node_id = self.undirected_graph.GetRndNId(self.rnd)
        node_cluster_coefficient = snap.GetNodeClustCf(self.undirected_graph, node_id)
        print("Clustering coefficient of random node {}: {}".format(
            node_id, round(node_cluster_coefficient, self.rounding_factor)
        ))

    def print_number_of_triads_of_randomly_selected_node(self):
        node_id = self.undirected_graph.GetRndNId(self.rnd)
        node_num_triads = snap.GetNodeTriads(self.undirected_graph, node_id)
        print("Number of triads random node {} participates: {}".format(node_id, node_num_triads))

    def plot_distribution_of_clustering_coefficient(self):
        clustering_coefficient_vector = snap.TFltPrV()
        snap.GetClustCf(self.undirected_graph, clustering_coefficient_vector, -1)
        degree_coefficient_distribution = {}
        for pair in clustering_coefficient_vector:
            degree_coefficient_distribution[pair.GetVal1()] = pair.GetVal2()

        self.plot_graph(
            'clustering_coeff_' + self.subgraph_name + '.png',
            degree_coefficient_distribution,
            "Degree",
            "Clustering Coefficient",
            "Clustering Coefficient Distribution ({})".format(self.subgraph_name)
        )

    def print_top_five_nodes_by_degree_centrality(self):
        degree_centrality_list = []
        for nodes in self.undirected_graph.Nodes():
            degree_centrality = self.undirected_graph.GetDegreeCentr(nodes.GetId())
            degree_centrality_list.append((-degree_centrality, nodes.GetId()))
        degree_centrality_list.sort()
        print("Top 5 nodes by degree centrality:", end='')
        for centrality, node in degree_centrality_list[:5]:
            print('', node, end='')
        print()

    def print_top_five_nodes_by_closeness_centrality(self):
        closeness_centrality_list = []
        for nodes in self.undirected_graph.Nodes():
            closeness_centrality = self.undirected_graph.GetClosenessCentr(nodes.GetId())
            closeness_centrality_list.append((-closeness_centrality, nodes.GetId()))
        closeness_centrality_list.sort()
        print("Top 5 nodes by closeness centrality:", end='')
        for centrality, node in closeness_centrality_list[:5]:
            print('', node, end='')
        print()

    def print_top_five_nodes_by_betweenness_centrality(self):
        betweenness_centrality_list = []
        nodes_map, edges_map = self.undirected_graph.GetBetweennessCentr(1.0)
        for node in nodes_map:
            betweenness_centrality_list.append((-nodes_map[node], node))
        betweenness_centrality_list.sort()
        print("Top 5 nodes by betweenness centrality:", end='')
        for centrality, node in betweenness_centrality_list[:5]:
            print('', node, end='')
        print()


generate_structure = GenStructure()

generate_structure.print_number_of_nodes_and_edges()
generate_structure.print_number_of_nodes_with_given_degree()
generate_structure.print_nodes_with_maximum_degree()
# generate_structure.plot_degree_distribution()
generate_structure.print_approximate_full_diameter()
generate_structure.print_approximate_effective_diameter()
# generate_structure.plot_short_path_lengths_distribution_in_network()
generate_structure.print_fraction_of_nodes_in_largest_connected_component()
generate_structure.print_number_of_bridges()
generate_structure.print_number_of_articulation_points()
# generate_structure.plot_distribution_of_size_of_connected_components()
generate_structure.print_average_clustering_coefficient()
generate_structure.print_number_of_triads()
generate_structure.print_clustering_coefficient_of_randomly_selected_node()
generate_structure.print_number_of_triads_of_randomly_selected_node()
# generate_structure.plot_distribution_of_clustering_coefficient()
generate_structure.print_top_five_nodes_by_degree_centrality()
generate_structure.print_top_five_nodes_by_closeness_centrality()
generate_structure.print_top_five_nodes_by_betweenness_centrality()
