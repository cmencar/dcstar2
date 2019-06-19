# -*- coding: utf-8 -*-
import sys
sys.path.append('../')

import random
from genetic_algorithm.GeneticEvolution import GeneticEvolution
from genetic_algorithm.DeapGeneticGuide import DeapGeneticGuide
from genetic_algorithm.GeneticGuideProblem import GeneticGuideProblem
from genetic_algorithm.SecondLevelHeuristic import SecondLevelHeuristic
from genetic_algorithm.levenshtein import levenshtein
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
  


class Individual():
    
    def __init__ (self, individual_dim):
        
        self.genome = None
        
        self.individual_dim = individual_dim
        
        random.seed()
        
        self.create()
    
    
    def generate(self, individual_class, individual_dim):

        # definizione del genoma dell'individuo
        genome = list()
    
        # settaggio iniziale del genoma con
        # i geni tutti a zero
        for i in range (individual_dim):
            genome.append(0)
    
        # definizione di un numero casuale di geni impostati
        # secondo la sequenza 
        random_set_genes = random.randint(2, individual_dim)
    
        # per ogni elemento nella sequenza 
        for sequence_number in range(random_set_genes):
    
             # definizione di un indice casuale dove inserire
             # il gene della sequenza
            random_index = random.randint(0, individual_dim-1)
    
            # se all'indice determinato esiste gia un elemento 
            # si definisce un nuovo indice
            while genome[random_index] != 0:
                random_index = random.randint(0, individual_dim-1)
    
            # definizione del valore del gene dell'individuo
            # all'indice valutato
            genome[random_index] = sequence_number
    
        # ritorna il genoma dal quale definire l'individuo
        return individual_class(genome)

    
    # Funzione di valutazione dell'individuo
    def evaluate(self, individual):
    
        # definizione della variabile di valutazione
        valutation = 0 
    
        # per ogni attributo dell'individuo
        for gene in individual:
    
            # se è diverso da zero aumenta la valutazione
            if gene != 0:
                valutation = valutation + 1
    
        # restituisce la valutazione finale
        return valutation,
    
    
    def create(self):
        
        # Numero di individui selezionati per la 
        # selezione per torneo
        selected_for_tournament = 5 
        
        # Numero di individui
        # N.B. Per evitare la convergenza è utile inserire
        # la grandezza della popolazione maggiore del
        # numero di generazioni
        population_size = 100 
        
        # Generazioni di evoluzioni della popolazione
        generations = 10
        
        # grado di mutazione (percentuale)
        mutation_rate = 0.2
        
        # grado di accoppiamento (percentuale)
        mating_rate = 0.5
        
        # numero di individui finali acquisiti
        selected_best = 1
        
        # definizione di un oggetto per la creazione della guida genetica
        genetic_guide:GeneticEvolution = DeapGeneticGuide(self.evaluate,
                                                          self.generate,
                                                          self.individual_dim,
                                                          mutation_rate,
                                                          mating_rate,
                                                          selected_for_tournament)
        
        # evoluzione e acquisizione degli individui
        # migliori dalla guida genetica
        self.genome = genetic_guide.evolve(population_size, 
                                           generations, 
                                           selected_best)[0]


          
    
# Classe per la definizione di un Problem
# inerente ad un grafo utilizzando la guida genetica
class GeneticGuideGraphProblem(GeneticGuideProblem):
    
    state_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]
    
    adiacent_list = {
            "A" : [('B', 1), ('D', 1)],
            "B" : [('A', 1), ('C', 1)],
            "C" : [('B', 1), ('D', 1), ('E', 1)],
            "D" : [('A', 1), ('C', 1), ('F', 1)],
            "E" : [('C', 1), ('F', 1), ('H', 1)],
            "F" : [('D', 1), ('E', 1), ('H', 1), ('G', 1)],
            "G" : [('F', 1)],
            "H" : [('E', 1), ('F', 1), ('I', 1), ('J', 1), ('K', 1)],
            "I" : [('H', 1), ('J', 1)],
            "J" : [('H', 1), ('I', 1), ('L', 1)],
            "K" : [('H', 1), ('L', 1)],
            "L" : [('K', 1), ('J', 1)],
            "M" : [] # nodo irraggiungibile
            }
    
    distance_list = [
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],  
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
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
        
        
        self.slh_generator = self.create_second_level_heuristic()
    
    
    
    # Metodo per il calcolo del costo del percorso
    def estimate_cost (self, path):
        
        (g, second_level_heuristic) = self.g(path)
        h = self.h(path)
        return g + (second_level_heuristic + h)
    
    
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
        
        string_path = self.stringfy_path(path)
        
        second_level_heuristic = self.slh_generator.get(string_path)
        
        return path_length, second_level_heuristic

    
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


    def create_second_level_heuristic (self):
        
        self.individual = Individual(len(self.state_list))
        
        string_individual = self.stringfy_individual(self.individual.genome, " ")

        second_level_heuristic = SecondLevelHeuristic(levenshtein, string_individual)
        
        return second_level_heuristic



    def stringfy_path (self, path):
        
        string_path = []
        
        for state in path:
            string_path.append(state[0])
        
        return string_path
    

    
    def stringfy_individual (self, individual, initializator):
        
        string_individual = []

        for i in range(0, len(individual)):
            string_individual.append(initializator)        
        
        for i in range(0, len(individual)):
            
            state_index = individual[i]
            
            if state_index != 0:
            
                state = self.state_list[i]
                string_individual[state_index-1] = state
        
        string_individual = [x for x in string_individual if x != initializator]
        
        print(string_individual)
        
        return string_individual
        
        
        #return string_individual
    