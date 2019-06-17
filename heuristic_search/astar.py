from heuristic_search.pqueue import PriorityQueue
from heuristic_search.node import Node

# Algoritmo A* per la ricerca del percorso ottimale
# da uno stato iniziale ad uno finale
def astar(problem):

    # variabile per la valutazione dei rami valutati dall'algoritmo
    branches_taken = 0
    
    # la coda con priorità per inserire i percorsi gia valutati
    closed = PriorityQueue()

    # la coda con piorità per inserire i percorsi da valutare
    front = PriorityQueue()  

    # definisce il nodo di partenza del grafo
    start_node =  Node(problem.start_state)

    # in primo luogo, definisce i percorsi che dal nodo di partenza porta agli altri nodi figli.
    # Di questi percorsi ne stima un costo in base alla funzione estimate_cost.
    # Infine definisce una tupla in cui sono presenti la lista dei costi stimati dei percorsi calcolati
    # e il nodo iniziale definito in precedenza
    estimated_node = (problem.estimate_cost(start_node.path()), start_node) 

    # inserisce all'interno della coda dei percorsi da valutare i percorsi stimati
    front.put(estimated_node)

    # finchè nella coda dei percorsi da valutare sarà presente almeno un percorso
    while not front.empty():
        
        # incremento del contatore dei rami valutati
        branches_taken = branches_taken + 1

        # si acquisisce una tupla relativa al nodo corrente che si sta analizzando
        # momentaneamente e il costo stimato del percorso in cui il nodo
        # corrente ne fa da radice. Il percorso acquisito ha il prezzo minore nella
        # coda con priorità 'front'
        (path_estimated_cost, current_node) = front.get()

        # acquisisce lo stato del nodo corrente
        current_state = current_node.state

        # se il nodo analizzato non è un nodo finale, ovvero ha più adiacenti
        if not problem.unique_successors:

            # allora si inserisce nella coda con priorità 'closed'
            # il nodo corrente e il relativo percorso con costo stimato
            closed.put((path_estimated_cost, current_node))

        # se lo stato del nodo corrente è quello che si ricercava
        if problem.goal(current_state):

            # allora si restituisce il percorso del nodo corrente
            # poiche è quello giusto
            return (current_node.path(), branches_taken)

        else:
            
            # acquisisce i nodi adiacenti del nodo corrente per effettuare una valutazione
            successors = problem.successors(current_state)

            # per ogni nodo nella lista dei nodi adiacenti del nodo corrente
            for successor_state in successors:

                # viene creata una istanza di nodo, definito come 'successore' 
                # in cui lo stato del nodo è uguale allo stato del nodo adiacente
                # valutato e il suo 'parente' è uguale al nodo corrente valutato
                successor_node = Node(successor_state, parent_node=current_node)

                # definizione del costo stimato del percorso dal nodo di partenza al nodo 'successore'  
                path_estimated_cost = problem.estimate_cost(successor_node.path())

                # se il nodo analizzato non è un nodo finale, ovvero ha nodi adiacenti
                if not problem.unique_successors:

                    # acquisisci la lista dei nodi adiacenti del nodo 'successori' non valutati
                    estimated_node = front.find(successor_state)

                    # se ci sono nodi adiacenti al nodo successore
                    if estimated_node is not None:

                        # se il percorso del nodo adiacente è migliore del percorso ottimale
                        # preso a priori (poiche la coda con priorità definisce come primo
                        # elemento il percorso migliore tra la lista dei nodi 'successivi')
                        if path_estimated_cost < estimated_node[0]:

                            # viene rimosso dalla lista dei nodi da valutare i percorsi
                            # dei nodi adiacenti
                            front.remove(estimated_node)

                            # si inserisce nella lista dei nodi da valutare il percorso
                            # dell'adiacente migliore
                            front.put((path_estimated_cost, successor_node))

                    # se non ci sono nodi adiacenti
                    else:

                        # acquisisci la lista dei nodi adiacenti del nodo 'successori' gia valutati
                        estimated_node = closed.find(successor_state)

                        # se ci sono nodi adiacenti
                        if estimated_node is not None:

                            # se il percorso del nodo adiacente è migliore del percorso ottimale
                            # preso a priori (poiche la coda con priorità definisce come primo
                            # elemento il percorso migliore tra la lista dei nodi 'successivi')
                            if path_estimated_cost < estimated_node[0]:

                                # si inserisce nella lista dei nodi da valutare il percorso
                                # dell'adiacente migliore
                                front.put((path_estimated_cost, successor_node))

                                # viene rimosso dalla lista dei nodi valutati i percorsi
                                # dei nodi adiacenti
                                closed.remove(estimated_node)
                        
                        # se invece non ci sono nodi adiacenti
                        else:

                            # inseriamo all'interno della coda con priorità 'front'
                            # il nodo 'successore' e il costo del suo percorso
                            front.put((path_estimated_cost, successor_node))
                
                # se il nodo analizzato è un nodo finale, ovvero non ha nodi adiacenti
                else:

                    # si inserisce all'interno della coda con priorità 'front'
                    # il nodo 'successore' e il costo del suo percorso
                    front.put((path_estimated_cost, successor_node))

    # nessun risultato trovato
    return (None, branches_taken)
