import sys
sys.path.append('../')

from heuristic_search import astar
from heuristic_search.Problem import Problem


# PER ULTERIORI INFORMAZIONI GUARDARE L'IMMAGINE ProblemTest_03_graph

states = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]
adiacents = {
        "A" : [('B', 9), ('D', 6)],
        "B" : [('A', 9), ('C', 4)],
        "C" : [('B', 4), ('D', 7), ('E', 6)],
        "D" : [('A', 6), ('C', 7), ('F', 5)],
        "E" : [('C', 6), ('F', 7), ('H', 11)],
        "F" : [('D', 5), ('E', 7), ('H', 12), ('G', 3)],
        "G" : [('F', 3)],
        "H" : [('E', 11), ('F', 12), ('I', 2), ('J', 5), ('K', 3)],
        "I" : [('H', 2), ('J', 3)],
        "J" : [('H', 5), ('I', 3), ('L', 4)],
        "K" : [('H', 3), ('L', 2)],
        "L" : [('K', 2), ('J', 4)],
        "M" : [] # nodo irraggiungibile (ipotetico per test, non visibile dall'immagine)
        }
distances = [
        [0, 9, 5, 6, 7, 10, 12, 14, 12, 16, 17, 17, 23],
        [9, 0, 4, 6, 8, 10, 11, 9, 11, 13, 16, 17, 18],
        [5, 4, 0, 7, 6, 6, 8, 10, 11, 13, 15, 16, 19],
        [6, 6, 7, 0, 5, 5, 8, 9, 11, 14, 14, 18, 17],
        [7, 8, 6, 5, 0, 7, 5, 11, 13, 15, 18, 21, 21],
        [10, 10, 6, 5, 7, 0, 3, 12, 12, 13, 14, 14, 13],
        [12, 11, 8, 8, 5, 3, 0, 2, 4, 6, 7, 9, 14],
        [14, 9, 10, 9, 11, 12, 2, 0, 2, 5, 3, 5, 13],
        [12, 11, 11, 11, 13, 12, 4, 2, 0, 3, 4, 5, 8],
        [16, 13, 13, 14, 15, 13, 6, 5, 3, 0, 1, 4, 10],
        [17, 16, 15, 14, 18, 14, 7, 3, 4, 1, 0, 2, 7],
        [17, 17, 16, 18, 21, 14, 9, 5, 5, 4, 2, 0, 7],
        [23, 18, 19, 17, 21, 13, 14, 13, 8, 10, 7, 7, 0],
        ]



problem = Problem(states, adiacents, distances, "A", "G")

solution = astar.astar(problem)

stamp = "\nLa soluzione del problema (tratta A-G) è :\n"
if solution is not None:
    for (node, cost) in solution:
        stamp = stamp + " " + node
else:
    stamp = stamp + " NESSUNA SOLUZIONE TROVATA"
print(stamp)


problem = Problem(states, adiacents, distances, "B", "G")

solution = astar.astar(problem)

stamp = "\nLa soluzione del problema (tratta B-G) è :\n"
if solution is not None:
    for (node, cost) in solution:
        stamp = stamp + " " + node
else:
    stamp = stamp + " NESSUNA SOLUZIONE TROVATA"
print(stamp)



problem = Problem(states, adiacents, distances, "A", "J")

solution = astar.astar(problem)

stamp = "\nLa soluzione del problema (tratta A-J) è :\n"
if solution is not None:
    for (node, cost) in solution:
        stamp = stamp + " " + node
else:
    stamp = stamp + " NESSUNA SOLUZIONE TROVATA"
print(stamp)



problem = Problem(states, adiacents, distances, "A", "M")

solution = astar.astar(problem)

stamp = "\nLa soluzione del problema (tratta A-M) è :\n"
if solution is not None:
    for (node, cost) in solution:
        stamp = stamp + " " + node 
else:
    stamp = stamp + " NESSUNA SOLUZIONE TROVATA"
print(stamp)
