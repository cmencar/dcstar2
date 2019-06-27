# -*- coding: utf-8 -*-
import sys
sys.path.append('../')

from heuristic_search.Problem import Problem
from heuristic_search.astar import astar
from genetic_algorithm.DeapGeneticGuideGraphProblem import DeapGeneticGuideGraphProblem
from genetic_algorithm.UGPGeneticGuideGraphProblem import UGPGeneticGuideGraphProblem
from GraphProblem import GraphProblem

# lista degli stati del grafo
state_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"]

# lista delle adiacenze degli stati del grafo
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

# lista delle distanze tra gli stati del grafo
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


# definizione di un GraphProblem, non usando la guida genetica
problem:Problem = GraphProblem(state_list, adiacent_list, distance_list, "A", "L")

# acquisizione della soluzione valutando A*
(solution, n_branches) = astar(problem)


# stampa della soluzione e delle altre informazioni
# sull'esecuzione effettuata
print("Current path solution: ")
for state in solution:
    print(state[0])

print("Evaluated branches during solution definition: ")
print(n_branches)


# definizione della dimensione iniziale della popolazione
population_size = 100

# definizione delle generazioni di individui creati
generations = 50 

# definizione della percentuale di mutazione
mutation_rate = 0.1

# definizione della percentuale di accoppiamento
mating_rate = 0.5

# definizione del numero di individui soggetti alla 
# selezione per torneo per ogni torneo
selected_for_tournament = 10

# definizione dell'acquisizione del miglior individuo
selected_best = 1

# definizione delle variabili per le informazioni sulle valutazioni
ideal_deap = not_ideal_deap = ideal_ugp = not_ideal_ugp = 0
total_eval_branches = average_deap = average_ugp = 0

# definizione delle valutazioni su A*+GG
valutations = 100

# effettuando un insieme di valutazioni in DEAP
for i in range(valutations):
    
    # deifnizione di una istanza di DeapGeneticGuideGraphProblem,
    # problema utilizzante un grafo e associato alla guida genetica
    problem_gg_deap:Problem = DeapGeneticGuideGraphProblem(state_list, adiacent_list, distance_list, "A", "L")
    
    # inizializzazione della guida genetica con i parametri 
    # dapprima definiti    
    problem_gg_deap.initializing_genetic_guide(population_size, 
                                         generations, 
                                         mutation_rate, 
                                         mating_rate, 
                                         selected_for_tournament, 
                                         selected_best)

    # acquisizione della soluzione dell'A* utilizzando la guida genetica
    (solution_gg, n_branches_gg) = astar(problem_gg_deap)   


    # stampa della soluzione e delle altre informazioni
    # sull'esecuzione effettuata
    print("\n\n----------------------------------------------------\n")
    print("Evaluated branches during solution definition with Genetic Guide in DEAP: ")
    print(n_branches_gg)
    
    if(n_branches_gg <= n_branches):
        ideal_deap += 1
    else:
        not_ideal_deap += 1
        
    total_eval_branches = total_eval_branches + n_branches_gg

average_deap = total_eval_branches / valutations
print("\nON", valutations, "TESTS WITH INDIVIDUAL CREATED BY UGP, THE FINAL EVALUATION IS: ")
print("-- IDEAL SITUATION: ", ideal_deap, "%  NOT IDEAL SITUATION: ", not_ideal_deap, "% --")
print("AVERAGE EVALUATED BRANCHES WITH A*+GG ARE ", average_deap, 
      " AGAINST ", n_branches, " EVALUATED BRANCHES TAKEN BY A* ALONE.\n\n")

# reset del contatore
total_eval_branches = 0


# effettuando un insieme di valutazioni in UGP
for i in range(valutations):
    
    # deifnizione di una istanza di UGPGeneticGuideGraphProblem,
    # problema utilizzante un grafo e associato alla guida genetica
    problem_gg_ugp:Problem = UGPGeneticGuideGraphProblem(state_list, adiacent_list, distance_list, "A", "L")
    
    file_dir = "UGP/BEST_P" + str(i + 1) + ".in"
    
    # inizializzazione della guida genetica con i parametri 
    # dapprima definiti    
    problem_gg_ugp.initializing_genetic_guide(file_dir)

    # acquisizione della soluzione dell'A* utilizzando la guida genetica
    (solution_gg, n_branches_gg) = astar(problem_gg_ugp)   


    # stampa della soluzione e delle altre informazioni
    # sull'esecuzione effettuata
    print("\n\n----------------------------------------------------\n")
    print("Evaluated branches during solution definition with Genetic Guide in UGP: ")
    print(n_branches_gg)
    
    if(n_branches_gg <= n_branches):
        ideal_ugp += 1
    else:
        not_ideal_ugp += 1
        
    total_eval_branches = total_eval_branches + n_branches_gg

average_ugp = total_eval_branches / valutations

print("\nON", valutations, "TESTS WITH INDIVIDUAL CREATED BY UGP, THE FINAL EVALUATION IS: ")
print("-- IDEAL SITUATION: ", ideal_ugp, "%  NOT IDEAL SITUATION: ", not_ideal_ugp, "% --")
print("AVERAGE EVALUATED BRANCHES WITH A*+GG ARE ", average_ugp, 
      " AGAINST ", n_branches, " EVALUATED BRANCHES TAKEN BY A* ALONE.\n\n")

# valutazione finale: confronto tra DEAP e UGP
print("\nON", valutations, "TEST WITH THE TWO GG METHODS, THE FINAL EVALUATION,"
      "CONFRONTING EACH OTHER, IS: ")
print("---------- DEAP -----------")
print("-- IDEAL SITUATION: ", ideal_deap, "%  NOT IDEAL SITUATION: ", not_ideal_deap, "% --")
print("---------- UGP -----------")
print("-- IDEAL SITUATION: ", ideal_ugp, "%  NOT IDEAL SITUATION: ", not_ideal_ugp, "% --")
print("AVERAGE EVALUATED BRANCHES WITH DEAP ARE ", average_deap, 
      " AGAINST ", average_ugp, " EVALUATED BRANCHES WITH UGP.\n\n")

