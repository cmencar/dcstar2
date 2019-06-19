# -*- coding: utf-8 -*-
import sys
sys.path.append('../')

from heuristic_search.Problem import Problem
from heuristic_search.astar import astar
from genetic_algorithm.DeapGeneticGuideGraphProblem import DeapGeneticGuideGraphProblem
from GraphProblem import GraphProblem

state_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"]

adiacent_list = {
            "A" : [('B', 2), ('C', 2)],
            "B" : [('A', 2), ('D', 1), ('F', 2), ('G', 2)],
            "C" : [('A', 2), ('E', 1), ('F', 1), ('H', 2)],
            "D" : [('B', 1), ('G', 1)],
            "E" : [('C', 1), ('H', 1)],
            "F" : [('B', 2), ('C', 2), ('J', 2), ('K', 2), ('I', 2)],
            "G" : [('B', 2), ('D', 1), ('J', 2)],
            "H" : [('E', 1), ('C', 2), ('K', 2)],
            "I" : [('F', 2), ('L', 2)],
            "J" : [('F', 2), ('G', 2), ('M', 1), ('L', 2), ('O', 2)],
            "K" : [('F', 2), ('H', 2), ('L', 2), ('N', 1)],
            "L" : [('I', 2), ('J', 2), ('K', 2), ('M', 1), ('N', 1)],
            "M" : [('J', 1), ('L', 1)], 
            "N" : [('K', 1), ('L', 1), ('P', 2)],
            "O" : [('J', 2), ('M', 1)],
            "P" : [('N', 2)]
            }


# Si è deciso di impostare questi valori per metter maggiormente 
# in difficolta l'algoritmo astar con una valutazione euristica
# di primo livello di scarsa qualità
distance_list = [
        [0, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
        [10, 0, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
        [10, 10, 0, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
        [10, 10, 10, 0, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
        [10, 10, 10, 10, 0, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
        [10, 10, 10, 10, 10, 0, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
        [10, 10, 10, 10, 10, 10, 0, 10, 10, 10, 10, 10, 10, 10, 10, 10],
        [10, 10, 10, 10, 10, 10, 10, 0, 10, 10, 10, 10, 10, 10, 10, 10],  
        [10, 10, 10, 10, 10, 10, 10, 10, 0, 10, 10, 10, 10, 10, 10, 10],
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 0, 10, 10, 10, 10, 10, 10],
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 0, 10, 10, 10, 10, 10],
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 0, 10, 10, 10, 10],
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 0, 10, 10, 10],
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 0, 10, 10],
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 0, 10],
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 0]
        ]


problem:Problem = GraphProblem(state_list, adiacent_list, distance_list, "A", "L")
solution = astar(problem)


print("La soluzione del percorso corrente")
for state in solution[0]:
    print(state[0])

print("Numero di rami valutati per raggiungere la soluzione")
print(solution[1])

population_size = 100
generations = 50 
mutation_rate = 0.1
mating_rate = 0.5
selected_for_tournament = 10
selected_best = 1

ideal = not_ideal = total = average = 0

valutations = 50

for i in range(valutations):
    GGproblem:Problem = DeapGeneticGuideGraphProblem(state_list, adiacent_list, distance_list, "A", "L")
    GGproblem.initializing_genetic_guide(population_size, 
                                         generations, 
                                         mutation_rate, 
                                         mating_rate, 
                                         selected_for_tournament, 
                                         selected_best)
    GGsolution = astar(GGproblem)   

    print("\n\n----------------------------------------------------\n")
    print("Numero di rami valutati per raggiungere la soluzione tramite GG")
    print(GGsolution[1])
    
    if(GGsolution[1] <= solution[1]):
        ideal += 1
    else:
        not_ideal += 1
        
    total = total + GGsolution[1] 

average = total / valutations
print("\nSU", valutations, "PROVE LA VALUTAZIONE FINALE E': ")
print("CASO IDEALE: ", ideal, "  CASO NON IDEALE: ", not_ideal)
print("LA MEDIA DEI RAMI PERCORSI DA A*+GG E' DI ", average, 
      " CONTRO I ", solution[1], "RAMI PERCORSI DA A* PURO")


