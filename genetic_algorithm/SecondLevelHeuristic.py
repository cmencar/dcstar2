# -*- coding: utf-8 -*-

class SecondLevelHeuristic():
    
    def __init__ (self, heuristic_function, individual):
        
        self.individual = individual
        self.heuristic_function = heuristic_function
        
    
    def get (self, path):
        
        second_level_heuristic = self.heuristic_function(self.individual, path)
        return second_level_heuristic
