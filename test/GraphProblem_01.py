# -*- coding: utf-8 -*-
import sys
sys.path.append('../')

from heuristic_search.Problem import Problem
from GraphNode import GraphNode

class GraphProblem_01(Problem):
    
    state_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]
    
    adiacent_list = {
            "A" : [('B', 9), ('D', 6)],
            "B" : [('A', 9), ('C', 4)],
            "C" : [('B', 4), ('D', 7), ('E', 6)],
            "D" : [('A', 6), ('C', 7), ('F', 5)],
            "E" : [('C', 6), ('F', 7), ('H', 11)],
            "F" : [('D', 5), ('E', 7), ('H', 12), ('G', 3)],
            "G" : [('F', 3)],
            "H" : [('E', 11), ('F', 12), ('I', 2), ('J', 5), ('K', 3)],
            "I" : [('H', 2), ('J', 3)],
            "J" : [('H', 5), ('I', 3), ('L', 4)],
            "K" : [('H', 3), ('L', 2)],
            "L" : [('K', 2), ('J', 4)],
            "M" : [] # nodo irraggiungibile
            }
    
    distance_list = [
        [0, 9, 5, 6, 7, 10, 12, 14, 12, 16, 17, 17, 23],
        [9, 0, 4, 6, 8, 10, 11, 9, 11, 13, 16, 17, 18],
        [5, 4, 0, 7, 6, 6, 8, 10, 11, 13, 15, 16, 19],
        [6, 6, 7, 0, 5, 5, 8, 9, 11, 14, 14, 18, 17],
        [7, 8, 6, 5, 0, 7, 5, 11, 13, 15, 18, 21, 21],
        [10, 10, 6, 5, 7, 0, 3, 12, 12, 13, 14, 14, 13],
        [12, 11, 8, 8, 5, 3, 0, 2, 4, 6, 7, 9, 14],
        [14, 9, 10, 9, 11, 12, 2, 0, 2, 5, 3, 5, 13],
        [12, 11, 11, 11, 13, 12, 4, 2, 0, 3, 4, 5, 8],
        [16, 13, 13, 14, 15, 13, 6, 5, 3, 0, 1, 4, 10],
        [17, 16, 15, 14, 18, 14, 7, 3, 4, 1, 0, 2, 7],
        [17, 17, 16, 18, 21, 14, 9, 5, 5, 4, 2, 0, 7],
        [23, 18, 19, 17, 21, 13, 14, 13, 8, 10, 7, 7, 0],
        ]
    
    
    # Costruttore della classe Problem
    def __init__ (self, start_state, end_state):
        
        # stato di partenza
        self.start_state = start_state
        
        # stato di arrivo
        self.end_state = end_state
        
        # nodo iniziale, dato dalla coppia data dallo stato iniziale 
        # e la distanza di partenza (presa 0 di default in quanto è la
        # distanza da se stesso)
        self.start_node = GraphNode((self.start_state, 0))
        
        # flag per definire se un nodo ha più
        # di un nodo adiacente (usato per efficienza)
        self.unique_successors = False
        
        # lista di tutti i nodi presenti
        self.node_list = []
        
        # definisce il grafo sul quale lavorare per determinare il
        # percorso migliore 
        self.connect_nodes (self.adiacent_list)
    
    
    # Metodo per il calcolo del costo del percorso
    def estimate_cost (self, path):
        
        return self.g(path) + self.h(path)
    
    
    # Metodo per la restituzione della lunghezza del percorso
    def g (self, path):
        
        # inizializzazione della lunghezza complessiva del percorso
        path_length = 0
        
        # se il percorso acquisito ha più di un nodo
        if (len(path) > 1):
            
            # per ogni nodo presente all'interno del percorso
            # che non sia il nodo radice
            for node in range (1, len(path)):
                
                # acquisizione dello stato e della distanza
                (state, distance) = path[node]
                
                # somma della lunghezza finora calcolata
                # con la distanza dal nodo
                path_length  = path_length + distance
        
        # viene restituito la lunghezza totale del percorso
        return path_length
    
    
    # Metodo per la restituzione dell'euristica
    # del percorso
    def h(self, path):
        
        # se la lista delle distanze è None allora ritorna un valore arbritario
        if self.distance_list is None:
            return 0
        
        else:
            start_state_index = self.state_list.index(path[-1][0])
            end_state_index = self.end_state.index(self.end_state)
            
            heuristic_cost = self.distance_list[start_state_index][end_state_index]
            
            return heuristic_cost
    
    
    # Metodo per definire se lo stato analizzato è
    # quello definito come obiettivo finale
    def goal (self, state):
        
        # Ritorna true se sono uguali, false altrimenti
        return state[0] == self.end_state
    
    
    # Metodo per definire la lista di successori
    # di un determinato stato
    # Ritorna la lista degli elementi adiacenti al nodo
    def successors (self, state):
        
        # lista dei successori da restituire
        successors = []
        
        # lista dei nodi da analizzare 
        nodes = []
        
        # per ogni nodo presente nella lista dei nodi
        for node in self.node_list:
            
            # se lo stato del nodo analizzato è uguale
            # a quello fornito alla funzione
            if node.state == state[0]:
                
                # aggiunta del nodo alla lista dei nodi da analizzare
                nodes.append(node)
        
        # per ogni nodo da analizzare
        # (questo ciclo viene effettuato per scompattare gli
        # elementi presenti nelle liste, altrimenti difficili
        # da gestire per l'algoritmo A*)
        for node in nodes:
            
            # e per ogni nodo adiacente al nodo da analizzare
            for adiacent in node.adiacent_nodes:
                
                # aggiunta del nodo adiacente alla lista
                successors.append(adiacent)
            
        # restituzione della lista dei successori
        return successors
    

    # Metodo per la creazione del grafo definendo i 
    # collegamenti tra i nodi
    def connect_nodes (self, adiacent_list):
        
        # per ogni stato passato alla classe Problem in
        # fase di creazione
        for state in self.state_list:
            
            # definizione di un nuova istanza di Node
            node = GraphNode(state)
            
            # aggiunta dell'istanza alla lista dei nodi
            self.node_list.append(node)
  
        # scandendo nuovamente la lista degli stati 
        for state in self.state_list:
            
            # per ogni nodo inserito nella lista
            for node in self.node_list:
                
                # se lo stato del nodo è uguale allo stato analizzato
                if node.state == state:
                
                    # aggiunta di uno stato adiacente al nodo preso in esame
                    node.add_adiacent(adiacent_list[state])


    