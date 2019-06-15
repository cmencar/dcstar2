import sys
sys.path.append('../')

from heuristic_search import astar
from heuristic_search.Problem import Problem


# TEST EFFETTUATO SULL'USO DI UN PROBLEM GENERICO 
# PER L'ALGORITMO A*

states = ["Milano", "Torino", "Udine", "Treviso"]
adiacents = {
        "Torino" : [('Milano', 30)],
        "Milano" : [('Torino', 30), ('Udine', 60)],
        "Udine" : [('Milano', 60), ('Treviso', 30)],
        "Treviso" : [('Udine', 30)]
        }


problem = Problem(states, adiacents, None, "Torino", "Treviso")

solution = astar.astar(problem)

print("La soluzione del problema (tratta Torino-Treviso) è :\n")
print(solution)
