# -*- coding: utf-8 -*-
import random
import matplotlib.pyplot as plt
from genetic_algorithm.deap_genetic_guide import DeapGeneticGuide
from cut_sequences.cuts_sequence import CutsSequence
from cut_sequences.selected_cuts_sequence import SelectedCutsSequence
from cut_sequences.dimensional_sequence_binary import DimensionalSequenceBinary
from cut_sequences.point import Point
import sys
sys.path.append('../')


# TESTING CLASS DEAPGENETICGUIDE (WITHOUT A*)

def generate(individual_class, individual_dim):
    # definizione del genoma dell'individuo
    genome = list()
    dimension_genome = list()

    # settaggio iniziale del genoma con
    # i geni tutti a zero
    for gene in range(individual_dim):
        genome.append(False)

    # definizione di un numero casuale di geni impostati
    # secondo la sequenza
    random_set_genes = random.randint(2, individual_dim)

    # per ogni elemento nella sequenza
    for sequence_number in range(random_set_genes):

        # definizione di un indice casuale dove inserire
        # il gene della sequenza
        random_index = random.randint(0, individual_dim - 1)

        # se all'indice determinato esiste gia un elemento
        # si definisce un nuovo indice
        while genome[random_index]:
            random_index = random.randint(0, individual_dim - 1)

        # definizione del valore del gene dell'individuo
        # all'indice valutato
        genome[random_index] = True

    # print("\nINDIVIDUAL GENERATED: \n", genome)

    # ritorna il genoma dal quale definire l'individuo
    return individual_class(genome)


def evaluate(individual):
    # definizione della variabile di valutazione
    valutation = 0
    total_genes = 0
    # ogni gene True aumenta la valutazione, mentre vengono contati tutti i geni esistenti
    valutation += individual.count(True)
    total_genes += len(individual)
    # restituisce la valutazione finale
    return valutation / total_genes

'''
# Funzione di generazione dell'individuo. -- LISTE MULTIDIMENSIONALI
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

# Funzione di valutazione dell'individuo -- LISTE MULTIDIMENSIONALI
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
'''
def fitness(individual):
    return (1 - evaluate(individual))*pow(pureness(individual, T_d), 5)
'''
'''
# Funzione che deifince la purezza di un dato genoma -- LISTE MULTIDIMENSIONALI
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

'''
# definizione di prototipi
print("\n----- prototypes -----\n")
points = [
    Point(coordinates=[.2354, .34, .543], label="prototype_1", name="point_A"),
    Point(coordinates=[.3345, .3421, .36897], label="prototype_1", name="point_B"),
    Point(coordinates=[.351, .3453, .6423], label="prototype_2", name="point_C"),
    Point(coordinates=[.45235, .00009, .141], label="prototype_1", name="point_D"),
    Point(coordinates=[.9, .5444, .25434], label="prototype_1", name="point_E"),
    Point(coordinates=[.999, .4, .7714], label="prototype_2", name="point_F"),
    Point(coordinates=[.799, .24, .1114], label="prototype_1", name="point_G")
]
print(points)
# definizione di un T_d
print("\n----- T_d -----\n")
T_d = CutsSequence([[.2, .36, .56, .63, .87, .88, .94], [.11, .32, .34, .36, .712, .998], [.02, .47, 0.7111, .89]])
T_d.debug_print()
'''
points1 = [
    Point(coordinates=[.2354, .34], label="prototype_1", name="point_A"),
    Point(coordinates=[.3345, .3421], label="prototype_1", name="point_B"),
    Point(coordinates=[.351, .3453], label="prototype_2", name="point_C"),
    Point(coordinates=[.45235, .00009], label="prototype_1", name="point_D"),
    Point(coordinates=[.9, .5444], label="prototype_1", name="point_E"),
    Point(coordinates=[.999, .4], label="prototype_2", name="point_F"),
    Point(coordinates=[.799, .24], label="prototype_1", name="point_G")
]
T_d_1 = CutsSequence([[.28495, .34275, .40225, .625675, .8495, .9495], [.120045, .29, .34105, .3437, .37265, .4722]])

# Memorizzazione grandezza dimensioni T_d
genes_per_dimension = list()
for dimension in range(T_d_1.get_dimensions_number()):
    genes_per_dimension.append(len(T_d_1.get_dimension(dimension)))

# Numero totale di geni dell'individuo
genes_number = 0
for num in genes_per_dimension:
    genes_number += num

# Numero di individui selezionati per la
# selezione per torneo
selected_for_tournament = 5

# Numero di individui
# N.B. Per evitare la convergenza è utile inserire
# la grandezza della popolazione maggiore del
# numero di generazioni
population_size = 2 * genes_number

# Generazioni di evoluzioni della popolazione
generations = 20

# grado di mutazione (percentuale)
mutation_rate = 1 / genes_number

# grado di accoppiamento (percentuale)
mating_rate = 0.7

# numero di individui finali acquisiti
selected_best = 10

# thing = generate(list, individual_elements_per_dimension) -- TEST DI "GENERATE"
# evaluation_thing = evaluate(thing) -- TEST DI "EVALUATE"

# definizione di un oggetto per la creazione della guida genetica con liste multidimensionali
# genetic_guide = DeapGeneticGuide(evaluate, generate, individual_elements_per_dimension, mutation_rate, mating_rate,
#                                 selected_for_tournament, T_d, points)

# definizione di un oggetto per la creazione della guida genetica con liste monolitiche
genetic_guide = DeapGeneticGuide(evaluate, generate, genes_number, mutation_rate, mating_rate, selected_for_tournament,
                                 T_d_1, points1, genes_per_dimension)

# evoluzione e acquisizione degli individui migliori dalla guida genetica con liste multidimensionali
# best_individuals = genetic_guide.evolve(population_size, generations, selected_best, T_d,
#                                        individual_elements_per_dimension)

# evoluzione e acquisizione degli individui migliori dalla guida genetica con liste monolitiche
best_individuals = genetic_guide.evolve(population_size, generations, selected_best, T_d_1,
                                        genes_per_dimension)

# riconversione da lista monolitica a "sequenza di tagli dimensionali"
list_of_sequences = list()
sequence = list()
dimension = list()
for individual in best_individuals:
    sequence.clear()
    offset = 0
    i = 0
    for num_elem in genes_per_dimension:
        dimension.clear()
        offset = offset + num_elem
        while i < offset:
            dimension.append(individual[i])
            i += 1
        sequence.append(dimension.copy())
    list_of_sequences.append(sequence.copy())

S_d = SelectedCutsSequence()
S_d_b = DimensionalSequenceBinary()

# stampa a video di ogni individuo
print("\n---------------------------------------------------------")
no_pure = True
for individual in list_of_sequences:
    S_d_b.from_binary(individual)
    S_d.from_binary(T_d_1, S_d_b)
    hyperboxes = S_d.generate_hyperboxes_set(points1, 0, 1)
    if hyperboxes.get_impure_hyperboxes_number() == 0:
        print("\nPURE INDIVIDUAL: \n", individual)

        no_pure = False

        '''
        for cut in S_d.get_dimension(0):
            plt.plot([cut, cut], [0, 1], 'k', linestyle='--', color='black')

        for cut in S_d.get_dimension(1):
            plt.plot([0, 1], [cut, cut], linestyle='--', color='black')

        for point in points1:
            if point.get_label() == "prototype_1":
                color = 'ro'
            elif point.get_label() == "prototype_2":
                color = 'bo'

            plt.plot(point.get_coordinate(0), point.get_coordinate(1), color)

        plt.show()
        '''
if no_pure:
     print("\nNONE OF THE GENERATED INDIVIDUALS HAS PURE HYPERBOXES")
