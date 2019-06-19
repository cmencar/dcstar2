# -*- coding: utf-8 -*-

# Classe per la definizione dell'euristica
# di secondo livello
class SecondLevelHeuristic():
    
    # Costruttore della classe.
    # Vengono passati l'individuo atto alla valutazione e
    # la funzione euristica di valutazione del percorso con
    # l'individuo
    def __init__ (self, heuristic_function, individual):
        
        self.individual = individual
        self.heuristic_function = heuristic_function
        
    
    # Metodo per l'acquisizione del valore del
    # secondo livello di euristica
    def get (self, path):
        
        second_level_heuristic = self.heuristic_function(self.individual, path)
        return second_level_heuristic
