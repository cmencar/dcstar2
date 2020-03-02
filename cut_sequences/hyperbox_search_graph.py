
# Class for defining the node for the hyperboxes' search graph
class HyperboxSearchGraphNode:

    # Class constructor
    # @value: value related to node
    def __init__(self, value):
        self.value = value
        self.adjacents = list()


    # Method for insert a new adiacent node
    # @adiacent: node to be added
    def add_adjacent(self, adjacent):
        self.adjacents.append(adjacent)


    # Method for acquire adiacents nodes
    def get_adjacents(self):
        return self.adjacents


    # Method for set node value
    # @value: value related to node
    def set_value(self, value):
        self.value = value


    # Method for acquire node value
    def get_value(self):
        return self.value



#
class HyperboxSearchGraph:

    #
    def __init__(self, intervals):

        self.nodes = list()

        self.evaluated_point = None

        start = HyperboxSearchGraphNode(None)

        dimensions_number = len(intervals)
        self.nodes.append(list([start]))

        for dimension_index in range(0, dimensions_number):

            dimension_intervals_number = len(intervals[dimension_index])
            nodes_dim = list()
            for dimension_interval_index in range(0, dimension_intervals_number):
                nodes_dim.append(HyperboxSearchGraphNode(intervals[dimension_index][dimension_interval_index]))
            self.nodes.append(nodes_dim)

        dimension_index = 0
        dimension_interval_index = 1
        while dimension_index < dimensions_number and dimension_interval_index < dimensions_number + 1:
            for node in self.nodes[dimension_index]:
                for adjacent in self.nodes[dimension_interval_index]:
                    node.add_adjacent(adjacent)
            dimension_index = dimension_index + 1
            dimension_interval_index = dimension_interval_index + 1

        self.evaluated_point = self.nodes[0][0]


    #
    def get_evaluated_point(self):
        return self.evaluated_point


    #
    def set_evaluated_point(self, point):
        self.evaluated_point = point


    #
    def get_adjacent_of_evaluated_point(self):
        return self.evaluated_point.get_adjacents()