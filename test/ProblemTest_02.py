import sys
sys.path.append('../')

from heuristic_search import astar
from heuristic_search.Problem import Problem

states = ["Torino", "Milano", "Bergamo", "Udine", "Treviso"]
adiacents = {
        "Torino" : [('Milano', 30)],
        "Milano" : [('Torino', 30), ('Bergamo', 15), ('Udine', 60)],
        "Bergamo" : [('Milano', 15), ('Udine', 70), ('Treviso', 50)],
        "Udine" : [('Milano', 60), ('Bergamo', 70), ('Treviso', 30)],
        "Treviso" : [('Udine', 30), ('Bergamo', 50)]
        }
distances = [
        [0, 30, 45, 90, 135],
        [30, 0, 15, 60, 100],
        [45, 15, 0, 70, 50],
        [90, 60, 70, 0, 30],
        [135, 100, 50, 30, 0]
        ]


problem = Problem(states, adiacents, distances, "Torino", "Treviso")

solution = astar.astar(problem)

print("La soluzione del problema (tratta Torino-Treviso) è :\n")
print(solution)
