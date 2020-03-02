
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



# Class for defining Hyperbox's search graph
class HyperboxSearchGraph:

    # Class constructor
    # @intervals: set of intervals that form the hyperbox
    def __init__(self, intervals):

        # initializing the list of nodes
        self.nodes = list()

        # initializing evaluated node
        self.evaluated_node = None

        # defining starting node and adding it to the list of nodes
        start = HyperboxSearchGraphNode(None)
        self.nodes.append(list([start]))

        # defining the number of dimensions of hyperbox
        dimensions_number = len(intervals)

        # for each dimension defined by the set of intervals
        for dimension_index in range(0, dimensions_number):

            # define the number of intervals into the evaluated dimension
            dimension_intervals_number = len(intervals[dimension_index])

            # define a list of nodes for the evaluated dimension
            nodes_from_evaluated_dimension = list()

            # for each interval into the dimension, define a new node using
            # the evaluated interval and insert it into list of nodes for the
            # evaluated dimension
            for interval_index in range(0, dimension_intervals_number):
                nodes_from_evaluated_dimension.append(HyperboxSearchGraphNode(intervals[dimension_index][interval_index]))

            # inserting the nodes for the evaluated dimension into the
            # list of all nodes
            self.nodes.append(nodes_from_evaluated_dimension)

        # resetting indexes
        dimension_index = 0
        interval_index = 1

        # for each interval into the set of interval passed
        while dimension_index < dimensions_number and interval_index < dimensions_number + 1:

            # Structuring nodes in graph: each node is associated to a particular level n
            # with 1 <= n <= d defining the adjacent nodes of the same node.
            # The initial node 'start' is associated with adjacent values (which in the graph
            # will be nodes with arcs entering from the initial node) and each subsequent node
            # is associated with other several adjacent nodes, parts of the list 'nodes'.
            # The nodes in the final level (i.e. those on level d) will have no adjacent values
            # and in them the search for the hyperbox will end.
            for node in self.nodes[dimension_index]:
                for adjacent in self.nodes[interval_index]:
                    node.add_adjacent(adjacent)
            dimension_index = dimension_index + 1
            interval_index = interval_index + 1

        # set the evaluated node as the starting node
        self.evaluated_node = self.nodes[0][0]


    # Method for get the evaluated node
    def get_evaluated_node(self):
        return self.evaluated_node


    # Method for set the evaluated node
    def set_evaluated_node(self, node):
        self.evaluated_node = node


    # Method for get the adjacent nodes of evaluated
    def get_adjacents(self):
        return self.evaluated_node.get_adjacents()
