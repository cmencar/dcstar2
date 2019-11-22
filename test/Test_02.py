# -*- coding: utf-8 -*-
import sys
sys.path.append('../')

from heuristic_search.Problem import Problem
from heuristic_search.astar import astar
from GraphProblem import GraphProblem


# TEST EFFETTUATO SULL'USO DEL GRAPHPROBLEM 
# PER L'ALGORITMO A*

problem:Problem = GraphProblem("A", "L")
solution = astar(problem)

print(solution)
