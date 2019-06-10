# -*- coding: utf-8 -*-
import sys
sys.path.append('../')

from heuristic_search.Problem import Problem
from heuristic_search.astar import astar
from GraphProblem_01 import GraphProblem_01
from GraphProblem_02 import GraphProblem_02

problem:Problem = GraphProblem_01("A", "L")
solution = astar(problem)

print(solution)
