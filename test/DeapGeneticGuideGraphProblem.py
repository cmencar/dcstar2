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
    
    # Costruttore della classe
    def __init__(self, state, parent_node=None):

        self.state = state
        self.parent = parent_node
        self.adiacent_nodes = []
        
    # 
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

# ----------------------------------------------------------------------------  



# Classe per la definizione di un individuo utilizzato per il confronto
# e la valutazione della euristica di secondo livello.
# L'individuo viene creato utilizzando la classe 
# DeapGeneticGuide
class Individual():
    
    # costruttore della classe
    def __init__ (self, individual_dim, population_size, 
                  generations, mutation_rate, mating_rate, 
                  selected_for_tournament, selected_best):
        
        # definizione del genoma (l'individuo vero e proprio)
        self.genome = None
        
        # inizializzazione dei numeri pseudocasuali
        random.seed()
        
        # creazione dell'individuo
        self.create(individual_dim, 
                    population_size, 
                    generations, 
                    mutation_rate,
                    mating_rate, 
                    selected_for_tournament, 
                    selected_best)
    
    
    # Metodo di generazione dell'individuo
    # La funzione viene acquisita ed utilizzata
    # all'interno dell'istanza della classe DeapGeneticGuide
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
    # La funzione viene acquisita ed utilizzata
    # all'interno dell'istanza della classe DeapGeneticGuide
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
    
    
    # Funzione per la creazione degli individui
    # Restituisce il genome dell'individuo ottimali
    def create(self, individual_dim, population_size, generations, 
               mutation_rate, mating_rate, selected_for_tournament, 
               selected_best):
        
        # definizione di un oggetto per la creazione della guida genetica
        genetic_guide:GeneticEvolution = DeapGeneticGuide(self.evaluate,
                                                          self.generate,
                                                          individual_dim,
                                                          mutation_rate,
                                                          mating_rate,
                                                          selected_for_tournament)
        
        # evoluzione e acquisizione dell'individuo migliore dalla guida genetica
        self.genome = genetic_guide.evolve(population_size, 
                                           generations, 
                                           selected_best)[0]

#----------------------------------------------------------------------------
         

    
# Classe per la definizione di un Problem
# inerente ad un grafo utilizzando la guida genetica
class DeapGeneticGuideGraphProblem(GeneticGuideProblem):
    
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
    
    
    # Metodo per l'inizializzazione della guida genentica
    def initializing_genetic_guide (self, population_size, 
                  generations, mutation_rate, mating_rate, 
                  selected_for_tournament, selected_best):
        
        # definisce il generatore dell'euristica di secondo livello
        self.slh_generator = self.create_second_level_heuristic(population_size, 
                generations, mutation_rate, mating_rate, 
                selected_for_tournament, selected_best)
        
    
    
    # Metodo per il calcolo del costo del percorso
    def estimate_cost (self, path):
        
        # valutazione del costo del percorso e della seconda euristica
        (g, second_level_heuristic) = self.g(path)
        
        # valutazione della prima euristica
        h = self.h(path)
        
        # ritorno del costo stimato
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
        
        # estrazione della stringa dal percorso per valutare
        # l'euristica di secondo livello
        string_path = self.stringfy_path(path)
        
        # definizione del valore dell'euristica di secondo livello.
        # Tale valutazione viene effettuata passando al generatore
        # di euristica il percorso sotto forma di stringa che verrà
        # confrontata (usando la funzione di euristica definita nel
        # costruttore, in questo caso l'algoritmi di Levenshtein)
        # con l'individuo generato dall'algoritmo genetico
        second_level_heuristic = self.slh_generator.get(string_path)
        
        # Restituisce la lunghezza del percorso insieme
        # all'euristica di secondo livello
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


    # Metodo per definire l'euristica di secondo
    # livello inerente al Problem
    # Ritorna un oggetto SecondLevelHeuristic in cui
    # sono presenti l'individuo e la funzione
    # valutatrice della seconda euristica (valutazione
    # che viene effettuata dalla funzione g)
    def create_second_level_heuristic (self, population_size, 
                  generations, mutation_rate, mating_rate, 
                  selected_for_tournament, selected_best):
        
        # creazione di una nuova istanza dell'individuo
        self.individual = Individual(len(self.state_list),
                                     population_size, 
                                     generations, 
                                     mutation_rate, 
                                     mating_rate, 
                                     selected_for_tournament, 
                                     selected_best)
        
        # definizione dell'individuo come una stringa
        # Il carattere vuoto è un inizializzatore della stringa.
        # Essa non deve contenere un elemento riconducibile
        # ad uno stato in quanto l'inizializzatore viene poi cancellato
        string_individual = self.stringfy_individual(self.individual.genome, " ")

        # definizione della secondo livello di euristica passando l'individuo
        # e l'algoritmo di Levenshtein
        second_level_heuristic = SecondLevelHeuristic(levenshtein, string_individual)
        
        # restituzione del secondo livello di euristica
        return second_level_heuristic


    # Metodo per convertire il percorso di un ramo
    # in una lista di stati inerenti al Problem.
    # Ritorna il percorso in una lista di stati
    def stringfy_path (self, path):
        
        string_path = []
        
        for state in path:
            string_path.append(state[0])
        
        return string_path
    

    # Metodo per convertire l'individuo ricavato
    # dall'algoritmo genentico in una lista di stati
    # inerenti al Problem.
    # Ritorna l'individuo in una lista di stati    
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

    