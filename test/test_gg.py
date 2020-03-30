# -*- coding: utf-8 -*-
import random
from genetic_algorithm.genetic_evolution import GeneticEvolution
from genetic_algorithm.deap_genetic_guide import DeapGeneticGuide
from genetic_algorithm.deap_genetic_guide_graph_problem import DeapGeneticGuideGraphProblem, Individual
from cut_sequences.cuts_sequence import CutsSequence
from cut_sequences.selected_cuts_sequence import SelectedCutsSequence
from cut_sequences.dimensional_sequence_binary import DimensionalSequenceBinary
from cut_sequences.hyperboxes_set import HyperboxesSet
from cut_sequences.point import Point
import sys
sys.path.append('../')


# TEST EFFETTUATO SULL'USO DELLA CLASSE DEAPGENETICGUIDE
# NELL'USO DELLA GUIDA GENETICA (INDIPENDENTEMENTE DA A*)

# Funzione di generazione dell'individuo.
# L'individuo sarà composto da una lista di cifre di dimensione
# individual_dim in cui N elementi (dove N è scelto casualmente tra 1
# e individual_dim) seguono una sequenza ordinata. Gli elementi
# della sequenza sono posti in modo casuale all'interno della
# lista. L'individuo, pertanto, segue la forma:
# [False, True, False, True, True, False, True, False]
def generate(individual_class, individual_dim):
    # definizione del genoma dell'individuo
    genome = list()
    dimension_genome = list()

    # settaggio iniziale del genoma con
    # i geni tutti a zero
    for dimension in range(len(individual_dim)):
        dimension_genome.clear()
        for index in range(individual_dim[dimension]):
            dimension_genome.append(False)
        genome.append(dimension_genome.copy())

    # definizione di un numero casuale di geni impostati
    # secondo la sequenza
    total_genes = 0
    for num in individual_dim:
        total_genes += num
    random_set_genes = random.randint(2, total_genes)

    # per ogni elemento nella sequenza
    for sequence_number in range(random_set_genes):

        # definizione di un indice casuale dove inserire
        # il gene della sequenza
        random_dimension = random.randint(0, len(individual_dim) - 1)
        random_index = random.randint(0, individual_dim[random_dimension] - 1)

        # se all'indice determinato esiste gia un elemento
        # si definisce un nuovo indice
        while genome[random_dimension][random_index]:
            random_dimension = random.randint(0, len(individual_dim) - 1)
            random_index = random.randint(0, individual_dim[random_dimension] - 1)

        # definizione del valore del gene dell'individuo
        # all'indice valutato
        genome[random_dimension][random_index] = True

    print("\nINDIVIDUAL GENERATED: \n", genome)

    # ritorna il genoma dal quale definire l'individuo
    return individual_class(genome)

# Funzione di valutazione dell'individuo
def evaluate(individual):
    # definizione della variabile di valutazione
    valutation = 0
    total_genes = 0
    # per ogni attributo dell'individuo
    for dimension in range(len(individual)):
        # ogni gene True aumenta la valutazione, mentre vengono contati tutti i geni esistenti
        valutation += individual[dimension].count(True)
        total_genes += len(individual[dimension])
    # restituisce la valutazione finale
    return valutation / total_genes

'''
def fitness(individual):
    return (1 - evaluate(individual))*pow(pureness(individual, T_d), 5)
'''
'''
def granularity(individual):
    return individual.count(True) / len(individual) -- NON SERVE
'''
'''
# Funzione che deifince la purezza di un dato genoma
def pureness(individual, T_d, points_list, m_d=0, M_d=1):
    # inizializzazione sequenze
    S_d = SelectedCutsSequence()
    S_d_b = DimensionalSequenceBinary()

    # creazione della sequenza dimensionale binaria e relativa selezione di tagli dal genoma
    S_d_b.from_binary(individual)
    S_d.from_binary(T_d, S_d_b)

    # creazione del set di hyperboxes
    hyperboxes = S_d.generate_hyperboxes_set(points_list, m_d, M_d)

    # calcolo del rapporto tra li numero di hyperbox puri e il numero complessivo di hyperbox
    return hyperboxes.get_pure_hyperboxes_number() / hyperboxes.get_hyperboxes_number()
'''

# Inizializzatore dei numeri casuali
random.seed()

# Creazione della sequenza di tagli T_d
T_d = CutsSequence([[1, 2, 3], [4, 5], [6, 7, 8], [9, 10]])

# Creazione dei prototipi


# Memorizzazione grandezza dimensioni T_d
individual_elements_per_dimension = list()
for dimension in range(T_d.get_dimensions_number()):
    individual_elements_per_dimension.append(len(T_d.get_dimension(dimension)))

# Numero totale di geni dell'individuo
genes = 0
for num in individual_elements_per_dimension:
    genes += num

# Numero di individui selezionati per la
# selezione per torneo
selected_for_tournament = 5

# Numero di individui
# N.B. Per evitare la convergenza è utile inserire
# la grandezza della popolazione maggiore del
# numero di generazioni
population_size = 2 * genes

# Generazioni di evoluzioni della popolazione
generations = 20

# grado di mutazione (percentuale)
mutation_rate = 1 / genes

# grado di accoppiamento (percentuale)
mating_rate = 0.7

# numero di individui finali acquisiti
selected_best = 10

# thing = generate(list, individual_elements_per_dimension)
# evaluation_thing = evaluate(thing)



# definizione di un oggetto per la creazione della guida genetica
genetic_guide = DeapGeneticGuide(evaluate, generate, individual_elements_per_dimension, mutation_rate, mating_rate,
                                 selected_for_tournament, T_d, points)
'''
# evoluzione e acquisizione degli individui
# migliori dalla guida genetica
best_individuals = genetic_guide.evolve(population_size,
                                        generations,
                                        selected_best)
'''

'''
# riconversione da lista monolitica a "sequenza di tagli dimensionali"
list_of_sequences = list()
sequence = list()
dimension = list()
for individual in best_individuals:
    sequence.clear()
    offset = 0
    i = 0
    for num_elem in individual_elements_per_dimension:
        dimension.clear()
        offset = offset + num_elem
        while i < offset:
            dimension.append(individual[i])
            i += 1
        sequence.append(dimension.copy())
    list_of_sequences.append(sequence.copy())
'''
'''
# stampa a video di ogni individuo
print("\n---------------------------------------------------------")
for individual in list_of_sequences:
    print("\nFINAL INDIVIDUAL: \n", individual)
'''