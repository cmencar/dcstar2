# -*- coding: utf-8 -*-
import sys
sys.path.append('../')

from abc import ABC, abstractmethod


# Classe astratta del problema
class Problem(ABC):
  
    unique_successors = False
    
    # Costruttore della classe Problem
    def __init__(self):
        raise NotImplementedError("Class not instantiable (abstract class)")
    
    
    # Method for calculating the cost of the node
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
        
    