# -*- coding: utf-8 -*-
import sys
sys.path.append('../')

from abc import ABC, abstractmethod


# Abstract class of the problem to give to A* algorithm
class Problem(ABC):

    # unique_successors flag
    unique_successors = False
    
    # Class abstract constructor. It can't be instantiable.
    def __init__(self):
        raise NotImplementedError("Class not instantiable (abstract class)")
    
    
    # Method for calculating the cost of the node
    @abstractmethod
    def estimate_cost(self, path):
        pass
    
    
    # Method for acquiring the g path-cost value
    @abstractmethod
    def g(self, path):
        pass

    
    # Method for acquiring the h heuristic value
    @abstractmethod
    def h(self, path):
        pass

    
    # Method for acquiring if the node is a result of A* computation
    @abstractmethod
    def goal(self, state):
        pass
    

    # Method for acquiring the list of successors for passed state
    @abstractmethod
    def successors(self, state):
        pass
        
    