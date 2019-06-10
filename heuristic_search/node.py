
# La classe Node equivale al singolo nodo del grafo.
class Node:

    # Si definisce il costruttore, definendo le variabili 'state', 'parent'
    # e la lista dei nodi adiacenti
    def __init__(self, state, parent_node=None):

        self.state = state
        self.parent = parent_node


    # La funzione path ritorna i percorsi inerenti ai nodi figli partendo dal 
    # nodo analizzato come radice. 
    # Se il nodo non ha figli allora ritorna il suo stato, altrimenti ritorna
    # il suo stato e in aggiunta, in modo ricorsivo, la lista dei figli con 
    # i propri percorsi fino a giungere ai nodi finali.
    def path(self):

        if self.parent is None:
            return [self.state]
        else:
            return self.parent.path() + [self.state]
       
    def __lt__ (self, other):
        
        return self.state[1] < other.state[1]
    
    def __eq__(self, other):
        
        if other is None:
            return False
        if not isinstance(other, Node):
            return False
        return self.state[1] == other.state[1]    
    
    
