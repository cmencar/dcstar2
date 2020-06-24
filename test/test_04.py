# -*- coding: utf-8 -*-
import sys
sys.path.append('../')

from heuristic_search.problem import Problem
from heuristic_search.astar import astar
from DeapGeneticGuideGraphProblem import DeapGeneticGuideGraphProblem


# TEST EFFETTUATO SULL'USO DEL GRAPHPROBLEM 
# PER L'ALGORITMO A*

state_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]

adiacent_list = {
            "A" : [('B', 1), ('D', 1)],
            "B" : [('A', 1), ('C', 1)],
            "C" : [('B', 1), ('D', 1), ('E', 1)],
            "D" : [('A', 1), ('C', 1), ('F', 1)],
            "E" : [('C', 1), ('F', 1), ('H', 1)],
            "F" : [('D', 1), ('E', 1), ('H', 1), ('G', 1)],
            "G" : [('F', 1)],
            "H" : [('E', 1), ('F', 1), ('I', 1), ('J', 1), ('K', 1)],
            "I" : [('H', 1), ('J', 1)],
            "J" : [('H', 1), ('I', 1), ('L', 1)],
            "K" : [('H', 1), ('L', 1)],
            "L" : [('K', 1), ('J', 1)],
            "M" : [] # nodo irraggiungibile
            }

distance_list = [
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],  
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        ]


problem:Problem = DeapGeneticGuideGraphProblem(state_list, adiacent_list, distance_list, "A", "L")
problem.initializing_genetic_guide(100, 10, 0.2, 0.5, 5, 1)
solution = astar(problem)

print(solution)
