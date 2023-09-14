import numpy as np
import snap
import sys
from collections import deque

infinite_value = sys.maxsize
rounding_factor = 6


def write_to_file(file_path, centrality):
    output_file = open(file_path, 'w')

    for _tuple in centrality:
        output_file.write(str(_tuple[1]) + " " + str(-_tuple[0]) + "\n")

    output_file.close()


class Handler:

    def __init__(self, filename):
        self.graph_mapping_continuous = {}
        self.inverse_graph_mapping = {}
        self.global_counter = 0
        self.undirected_graph = snap.TUNGraph.New()
        self.edge_list_file = open(filename, 'r')
        self.construct_graph()
        self.edge_list_file.close()

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
            # This mapping is done because in sub-graphs, node IDs are not continuous.
            # This will help in space optimization.
            if nodes.split()[0] not in self.graph_mapping_continuous:
                self.graph_mapping_continuous[nodes.split()[0]] = self.global_counter
                self.inverse_graph_mapping[self.global_counter] = nodes.split()[0]
                self.global_counter += 1

            if nodes.split()[1] not in self.graph_mapping_continuous:
                self.graph_mapping_continuous[nodes.split()[1]] = self.global_counter
                self.inverse_graph_mapping[self.global_counter] = nodes.split()[1]
                self.global_counter += 1

            self.add_node_to_graph(self.graph_mapping_continuous[nodes.split()[0]])
            self.add_node_to_graph(self.graph_mapping_continuous[nodes.split()[1]])

            self.add_edge_to_graph(self.graph_mapping_continuous[nodes.split()[0]],
                                   self.graph_mapping_continuous[nodes.split()[1]])

    def compute_closeness(self):
        centrality = ClosenessCentrality(self).closeness_centrality()
        centrality.sort()
        file_path = 'centralities/closeness.txt'
        write_to_file(file_path, centrality)
        return centrality[:100]

    def compute_betweenness(self):
        centrality = BetweennessCentrality(self).betweenness_centrality()
        centrality.sort()
        file_path = 'centralities/betweenness.txt'
        write_to_file(file_path, centrality)
        return centrality[:100]

    def compute_pagerank(self):
        centrality = PageRank(self, damping_factor=0.8, biased_node=4).page_rank()
        centrality.sort()
        file_path = 'centralities/pagerank.txt'
        write_to_file(file_path, centrality)
        return centrality[:100]


class ClosenessCentrality:

    def __init__(self, _handler: Handler):
        self.handler = _handler
        self.undirected_graph = _handler.undirected_graph
        self.number_of_nodes_in_the_graph = self.undirected_graph.GetNodes()

    def calc_shortest_path_matrix(self):
        distance_matrix = np.array(
            [
                [infinite_value for _ in range(self.number_of_nodes_in_the_graph)]
                for _ in range(self.number_of_nodes_in_the_graph)
            ]
        )

        for node in self.undirected_graph.Nodes():
            distance_matrix[node.GetId()][node.GetId()] = 0
            node_id = node.GetId()
            distance_for_current_node_id = snap.TIntH()
            snap.GetShortPath(self.undirected_graph, node_id, distance_for_current_node_id)

            # Update the distance of all nodes from the current node
            for target_node_id in distance_for_current_node_id:
                distance_matrix[node_id][target_node_id] = distance_for_current_node_id[target_node_id]

        return distance_matrix

    def closeness_centrality(self):
        shortest_path_distance_matrix = self.calc_shortest_path_matrix()
        centrality = []

        for node in self.undirected_graph.Nodes():
            node_id = node.GetId()

            # Take the sum of all shortest paths from this node to every other node if these two nodes are connected
            # Also calculate the size of this connected component to apply in the formula. Otherwise, it will give
            # wrong results
            total_shortest_path_sum = 0
            size_of_connected_component = 0
            for number_ in shortest_path_distance_matrix[node_id]:
                if number_ != infinite_value:
                    total_shortest_path_sum += number_
                    size_of_connected_component += 1

            if total_shortest_path_sum > 0 and size_of_connected_component > 1:
                centrality_temp = (size_of_connected_component - 1) / float(total_shortest_path_sum)
                # After calculating centrality for connected component, normalize as to vary the centrality based on
                # size of connected component
                normalized_value = (centrality_temp *
                                    (size_of_connected_component / float(self.number_of_nodes_in_the_graph)))
                rounded_centrality = round(normalized_value, rounding_factor)
                # Taking negative value so that sorting can be applied easily
                centrality.append((-rounded_centrality, self.handler.inverse_graph_mapping[node_id]))
            else:
                centrality.append((0.0, self.handler.inverse_graph_mapping[node_id]))

        return centrality


class BetweennessCentrality:

    def __init__(self, _handler: Handler):
        self.handler = _handler
        self.undirected_graph = _handler.undirected_graph
        self.number_of_nodes = self.undirected_graph.GetNodes()
        self.nodes = self.undirected_graph.Nodes()
        self.weighted_nodes_list = [index for index in range(self.number_of_nodes)]
        self.nodes_edge_list_dictionary = {}

    def initialize_dictionary_by_value(self, value):
        _dictionary = {}
        for node in self.weighted_nodes_list:
            _dictionary[node] = value
        return _dictionary

    def initialize_dictionary_by_empty_list(self):
        _dictionary = {}
        for node in self.weighted_nodes_list:
            _dictionary[node] = []
        return _dictionary

    def betweenness_centrality(self):

        centrality = self.initialize_dictionary_by_value(0)

        for node in self.nodes:
            self.nodes_edge_list_dictionary[node.GetId()] = [edge for edge in node.GetOutEdges()]

        # Brandes' Algorithm
        for index in self.weighted_nodes_list:
            stack_for_current_node = []
            queue_for_current_node = deque([])

            pred_dictionary = self.initialize_dictionary_by_empty_list()
            sigma = self.initialize_dictionary_by_value(0)

            # Initializing with -1 to signify that the node is un-travelled in BFS algorithm
            distance = self.initialize_dictionary_by_value(-1)

            sigma[index] = 1
            distance[index] = 0
            queue_for_current_node.append(index)

            # Apply BFS algorithm and apply steps as applied in Page 4 (Recursive solution) in the below documentation
            # https://www.cl.cam.ac.uk/teaching/1617/MLRD/handbook/brandes.pdf
            while queue_for_current_node:
                node = queue_for_current_node.popleft()
                stack_for_current_node.append(node)
                for neighbour_node in self.nodes_edge_list_dictionary[node]:
                    if distance[neighbour_node] < 0:
                        distance[neighbour_node] = distance[node] + 1
                        queue_for_current_node.append(neighbour_node)
                    if distance[neighbour_node] == distance[node] + 1:
                        sigma[neighbour_node] = sigma[neighbour_node] + sigma[node]
                        pred_dictionary[neighbour_node].append(node)

            delta = self.initialize_dictionary_by_value(0)
            while stack_for_current_node:
                node = stack_for_current_node.pop()
                for node_i in pred_dictionary[node]:
                    # Here, (1 + delta[node]) is termed as MAGIC in the mentioned PDF
                    delta[node_i] = delta[node_i] + (sigma[node_i] / sigma[node]) * (1 + delta[node])
                if node != index:
                    centrality[node] = centrality[node] + delta[node]

        centrality_list = []
        for key in centrality:
            # Taking negative value and converting to list of tuples so that sorting can be applied easily
            centrality_list.append((-centrality[key], self.handler.inverse_graph_mapping[key]))

        return centrality_list


class PageRank:

    def __init__(self, _handler, damping_factor=0.8, tolerance=1e-5, maximum_iterations=200, biased_node=4):
        self.handler = _handler
        self.undirected_graph = _handler.undirected_graph
        self.number_of_nodes = self.undirected_graph.GetNodes()
        self.weighted_nodes_list = [index for index in range(self.number_of_nodes)]
        self.damping_factor = damping_factor
        self.tolerance = tolerance
        # Here assuming that page ranks will converge in 200 iterations
        self.maximum_iterations = maximum_iterations

        self.transition_probability = np.array(
            [
                [0. for _ in self.weighted_nodes_list]
                for _ in self.weighted_nodes_list]
        )

        self.biased_node = biased_node

    def adjust_values_of_transition_probability_to_fit_markovian(self):
        for index in range(len(self.transition_probability)):
            sum_from_all_nodes = sum(self.transition_probability[index])

            # Handle the case when every element in the row is 0
            if sum_from_all_nodes == 0.:
                update_row = []
                average_value = 1. / self.number_of_nodes
                for _ in self.weighted_nodes_list:
                    update_row.append(average_value)
                self.transition_probability[index] = update_row
            # Otherwise take the average of every element in that row
            else:
                self.transition_probability[index] = self.transition_probability[index] / sum_from_all_nodes

    def get_teleportation_matrix(self):
        # Create teleportation matrix (multiply Vector of all 1's to transpose of preference vector)
        biased_preference_vector = np.array([0. for _ in self.weighted_nodes_list])
        for node in self.weighted_nodes_list:
            if node % self.biased_node == 0:
                biased_preference_vector[node] = float(self.biased_node) / self.undirected_graph.GetNodes()
        biased_preference_vector = biased_preference_vector.reshape(1, -1)
        return np.matmul(
            np.ones(len(self.weighted_nodes_list)).reshape(1, -1).T, biased_preference_vector
        )

    def perform_power_iteration(self):
        # Power Iteration
        page_rank = np.random.rand(self.transition_probability.shape[1]).reshape(1, -1)
        for _ in range(self.maximum_iterations):
            page_rank_previous = page_rank
            page_rank_updated = np.dot(page_rank, self.transition_probability) / np.sum(page_rank)

            change_in_value = np.abs(page_rank_updated - page_rank_previous)
            page_rank = page_rank_updated

            # Check if maximum change in page rank for a node is less than tolerance
            if np.max(change_in_value) < self.tolerance:
                break

        return page_rank.reshape(-1)

    def page_rank(self):

        # Update diagonal element of the matrix
        for edge in self.undirected_graph.Edges():
            self.transition_probability[edge.GetSrcNId()][edge.GetDstNId()] = 1.
            self.transition_probability[edge.GetDstNId()][edge.GetSrcNId()] = 1.

        self.adjust_values_of_transition_probability_to_fit_markovian()

        # Update transition probability based on given damping factor
        self.transition_probability = (self.damping_factor * self.transition_probability +
                                       (1 - self.damping_factor) * self.get_teleportation_matrix())

        page_rank = self.perform_power_iteration()

        centrality = []
        for index in range(len(page_rank)):
            # Taking list of tuples as page rank
            # Taking negative of the value to have ease in sorting
            rounded_centrality = round(page_rank[index], rounding_factor)
            centrality.append((-rounded_centrality, self.handler.inverse_graph_mapping[index]))

        return centrality


graph_filename = sys.argv[1]
handler = Handler(graph_filename)

top_nodes_closeness = handler.compute_closeness()
top_nodes_betweenness = handler.compute_betweenness()
top_node_page_rank = handler.compute_pagerank()

top_node_ids_closeness = []
for score, node_id in top_nodes_closeness:
    top_node_ids_closeness.append(node_id)


top_node_ids_betweenness = []
for score, node_id in top_nodes_betweenness:
    top_node_ids_betweenness.append(node_id)

top_node_ids_page_rank = []
for score, node_id in top_node_page_rank:
    top_node_ids_page_rank.append(node_id)

print("Number of influencer nodes:",
      len(set(top_node_ids_closeness).intersection(top_node_ids_betweenness).intersection(top_node_ids_page_rank)))
