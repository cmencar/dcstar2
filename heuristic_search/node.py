
# Class that define a single node in the A* computation.
class Node:

    # Class constructor
    # @state: state included in node
    # @parent_node: ancestor node of this node
    def __init__(self, state, parent_node = None):
        self.state = state
        self.parent = parent_node


    # The path function returns the paths inherent to the child nodes starting from the analysed node as root.
    # If the node has no children then it returns its state, otherwise it returns its state and in addition,
    # in a recursive way, the list of children with its own paths to the final nodes.
    def path(self):
        if self.parent is None:
            return [self.state]
        else:
            return self.parent.path() + [self.state]


    # Method for overriding the 'lower-than' operator
    def __lt__(self, other):
        return self.state < other.state


    # Method for overriding the 'greater-than' operator
    def __gt__(self, other):
        return self.state > other.state


    # Method for overriding the 'equal-to' operator
    def __eq__(self, other):
        return self.state == other.state
    
