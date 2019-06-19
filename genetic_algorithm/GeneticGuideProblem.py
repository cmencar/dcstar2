# -*- coding: utf-8 -*-
import sys
sys.path.append('../')

from abc import ABC, abstractmethod
from heuristic_search.Problem import Problem


# Classe astratta del problema
class GeneticGuideProblem (Problem):
  
    unique_successors = False
    
    # Costruttore della classe Problem
    def __init__ (self):
        raise NotImplementedError("Class not instantiable (abstract class)")
    
    
    # Metodo per il calcolo del costo del percorso
    @abstractmethod
    def estimate_cost(self, path):
        pass
    
    
    # Metodo per la restituzione della lunghezza del percorso
    @abstractmethod
    def g(self, path):
        pass

    
    # Metodo per la restituzione dell'euristica del percorso
    @abstractmethod
    def h(self, path):
        pass

    
    # Metodo per definire se lo stato analizzato è
    # quello definito come obiettivo finale
    @abstractmethod
    def goal(self, state):
        pass
    

    # Metodo per definire la lista di successori
    # di un determinato stato
    # Ritorna la lista degli elementi adiacenti al nodo    
    @abstractmethod
    def successors(self, state):
        pass
        
    
    # Metodo per convertire il percorso di un ramo
    # in una lista di stati inerenti al Problem.
    # Ritorna il percorso in una lista di stati
    @abstractmethod
    def stringfy_path (self, path):
        pass
    
    
    # Metodo per convertire l'individuo ricavato
    # dall'algoritmo genentico in una lista di stati
    # inerenti al Problem.
    # Ritorna l'individuo in una lista di stati
    @abstractmethod
    def stringfy_individual (self, individual):
        pass
    
    
    # Metodo per definire l'euristica di secondo
    # livello inerente al Problem
    # Ritorna un oggetto SecondLevelHeuristic in cui
    # sono presenti l'individuo e la funzione
    # valutatrice della seconda euristica (valutazione
    # che viene effettuata dalla funzione g)
    @abstractmethod
    def create_second_level_heuristic (self):
        pass


    # Metodo per l'inizializzazione della guida genentica
    # Vengono passati in input valori utili all'inizializzazione
    # della guida genetica, quali le generazioni totali di esecuzione,
    # la dimensione della popolazione, il grado di mutazione, ecc
    @abstractmethod
    def initializing_genetic_guide (self, population_size, generations, 
                mutation_rate, mating_rate, selected_for_tournament, selected_best):
        pass
