
# Class for define the node type used in DCStar
class DCStarNode:

    # Class constructor
    # @state: state of node (defined in a logical sequence of cuts)
    # @cost: node cost, defined by three-level priority
    def __init__(self, state, cost):
        self.__state = state
        self.__cost = cost


    # Method for get the node state
    def get_state(self):
        return self.__state


    # Method for get the node cost
    def get_cost(self):
        return self.__cost


    # Method for defining the cost
    def set_cost(self, cost):
        self.__cost = cost


    # Method for get the list of successors of this node.
    # The list of successor nodes is composed of DCStarNode type elements
    def successors(self):
        return [DCStarNode(successor, (0, 0, 0)) for successor in self.__state.get_successors()]


    # Overriding is-lower-than method
    def __lt__(self, node):
        return self.__cost < node.get_cost()


    # Overriding is-greater-than method
    def __gt__(self, node):
        return self.__cost > node.get_cost()


    # Overriding is-equal-to method
    def __eq__(self, node):
        return self.__cost == node.get_cost()
