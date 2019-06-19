# -*- coding: utf-8 -*-
import sys
sys.path.append('../')

from heuristic_search.Problem import Problem
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
            
    
# Classe per la definizione di un Problem
# inerente ad un grafo
class GraphProblem(Problem):
    
    # Costruttore della classe Problem
    def __init__ (self, state_list, adiacent_list, distance_list, start_state, end_state):
        
        # definizione della lista dei nodi
        self.state_list = state_list
        
        # definizione delle adiacenze dei nodi
        self.adiacent_list = adiacent_list
        
        # definizione delle distanze dei nodi
        self.distance_list = distance_list
        
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


    