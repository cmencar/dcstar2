# -*- coding: utf-8 -*-


# Classe per la definizione dell'euristica
# di secondo livello
class SecondLevelHeuristic():

    # Costruttore della classe.
    # Vengono passati l'individuo atto alla valutazione e
    # la funzione euristica di valutazione del percorso con
    # l'individuo
    def __init__(self, heuristic_function, individual):
        # individuo da valutare per l'euristica di secondo livello
        self.individual = individual

        # metodo di valutazione per l'euristica di secondo livello
        self.heuristic_function = heuristic_function

    # Metodo per l'acquisizione del valore del
    # secondo livello di euristica
    def get(self, path):
        # valutazione dell'euristica di secondo livello passando alla funzione
        # fornita nel costruttore il percorso da valutare e l'individuo
        # gia fornito dal costruttore
        second_level_heuristic = self.heuristic_function(self.individual, path)

        # restituzione del secondo livello di euristica
        return second_level_heuristic
