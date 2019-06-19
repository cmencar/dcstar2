from heuristic_search.node import Node

# Classe per la definizione di un nodo
# utile all'interno del grafo
class GraphNode(Node):
    
    def __init__(self, state, parent_node=None):

        self.state = state
        self.parent = parent_node
        self.adiacent_nodes = []
        
    def path(self):

        if self.parent is None:
            return [self.state]
        else:
            return self.parent.path() + [self.state]
        
    def add_adiacent (self, adiacent):
        
        for node in adiacent:
            self.adiacent_nodes.append(node)
            
    def __lt__ (self, other):
        
        return self.state[1] < other.state[1]
    
    def __eq__(self, other):
        
        if other is None:
            return False
        if not isinstance(other, GraphNode):
            return False
        return self.state[1] == other.state[1]