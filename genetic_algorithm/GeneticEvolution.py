# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


# Classe astratta per l'algoritmo genetico
class GeneticEvolution(ABC):
    
    
    # Costruttore della classe 
    def __init__ (self):
        raise NotImplementedError("Class not instantiable (abstract class)")
        
    
    # Metodo astratto per la valutazione dell'individuo
    @abstractmethod
    def evaluate(self, individual):
        pass
    
    
    # Metodo astratto per la generazione dell'individuo
    @abstractmethod
    def generate(self):
        pass
    
    
    # Metodo astratto per la generazione e la restituzione dei migliori individui
    # secondo l'algoritmo genetico
    @abstractmethod
    def evolve(self):
        pass
    
