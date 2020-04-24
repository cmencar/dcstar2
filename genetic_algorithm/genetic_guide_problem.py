# -*- coding: utf-8 -*-
import sys
sys.path.append('../')

from abc import abstractmethod
from heuristic_search.problem import Problem


# Classe astratta del problema in GG
class GeneticGuideProblem (Problem):
  
    unique_successors = False
    
    # Costruttore della classe Problem
    def __init__ (self):
        raise NotImplementedError("Class not instantiable (abstract class)")
    
    
    # Metodo astratto per il calcolo del costo del percorso
    @abstractmethod
    def estimate_cost(self, path):
        pass
    
    
    # Metodo astratto per la restituzione della lunghezza del percorso
    @abstractmethod
    def g(self, path):
        pass

    
    # Metodo astratto per la restituzione dell'euristica del percorso.
    # L'euristica è una tupla, composta dall'euristica di primo
    # livello e dall'euristica di secondo livello.
    # Nella definizione dell'istanza di GeneticGuideProblem
    # si implementeranno esclusivamente le due euristiche
    def h(self, path):
        return (self.h1(path), self.h2(path))

    
    # Metodo astratto per la definizione dell'euristica di
    # primo livello
    @abstractmethod
    def h1(self, path):
        pass
    
    
    # Metodo astratto per la definizione dell'euristica di
    # secondo livello
    @abstractmethod
    def h2(self, path):
        pass
    
    
    # Metodo astratto per definire se lo stato analizzato è
    # quello definito come obiettivo finale
    @abstractmethod
    def goal(self, state):
        pass
    

    # Metodo astratto per definire la lista di successori
    # di un determinato stato
    # Ritorna la lista degli elementi adiacenti al nodo    
    @abstractmethod
    def successors(self, state):
        pass
        
    
    # Metodo astratto per convertire il percorso di un ramo
    # in una lista di stati inerenti al Problem.
    # Ritorna il percorso in una lista di stati
    @abstractmethod
    def stringfy_path (self, path):
        pass
    
    
    # Metodo astratto per convertire l'individuo ricavato
    # dall'algoritmo genentico in una lista di stati
    # inerenti al Problem.
    # Ritorna l'individuo in una lista di stati
    @abstractmethod
    def stringfy_individual (self, individual):
        pass
    
    
    # Metodo astratto per definire l'euristica di secondo
    # livello inerente al Problem
    # Ritorna un oggetto SecondLevelHeuristic in cui
    # sono presenti l'individuo e la funzione
    # valutatrice della seconda euristica (valutazione
    # che viene effettuata dalla funzione g)
    @abstractmethod
    def create_second_level_heuristic (self):
        pass


    # Metodo astratto per l'inizializzazione della guida genentica
    # Vengono passati in input valori utili all'inizializzazione
    # della guida genetica, quali le generazioni totali di esecuzione,
    # la dimensione della popolazione, il grado di mutazione, ecc
    @abstractmethod
    def initializing_genetic_guide (self):
        pass
