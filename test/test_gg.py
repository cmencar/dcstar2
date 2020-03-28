# -*- coding: utf-8 -*-
import random
from genetic_algorithm.genetic_evolution import GeneticEvolution
from genetic_algorithm.deap_genetic_guide import DeapGeneticGuide
from genetic_algorithm.deap_genetic_guide_graph_problem import DeapGeneticGuideGraphProblem, Individual
from cut_sequences.cuts_sequence import CutsSequence
from cut_sequences.dimensional_sequence_binary import DimensionalSequenceBinary
import sys
sys.path.append('../')


# TEST EFFETTUATO SULL'USO DELLA CLASSE DEAPGENETICGUIDE
# NELL'USO DELLA GUIDA GENETICA (INDIPENDENTEMENTE DA A*)

# Inizializzatore dei numeri casuali
random.seed()

# Creazione della sequenza di tagli T_d
T_d = CutsSequence([[1, 2, 3], [4, 5], [6, 7, 8], [9, 10]])
T_d.debug_print()
S_d_b = T_d.generate_starting_binary()
S_d_b.debug_print()
# Memorizzazione grandezza dimensioni T_d
individual_dims = list()
for dimension in range(T_d.get_dimensions_number()):
    individual_dims.append(len(T_d.get_dimension(dimension)))

'''
# Classe per la definizione di un individuo utilizzato per il confronto
# e la valutazione della euristica di secondo livello.
# L'individuo viene creato utilizzando la classe
# DeapGeneticGuide
class Individual():

    # costruttore della classe
    def __init__(self, individual_dim, population_size,
                 generations, mutation_rate, mating_rate,
                 selected_for_tournament, selected_best):

        # definizione del genoma (l'individuo vero e proprio)
        self.genome = None

        # inizializzazione dei numeri pseudocasuali
        random.seed()

        # creazione dell'individuo
        self.create(individual_dim,
                    population_size,
                    generations,
                    mutation_rate,
                    mating_rate,
                    selected_for_tournament,
                    selected_best)

    # Funzione di generazione dell'individuo.
    # L'individuo sarà composto da una lista di cifre di dimensione
    # individual_dim in cui N elementi (dove N è scelto casualmente tra 1
    # e individual_dim) seguono una sequenza ordinata. Gli elementi
    # della sequenza sono posti in modo casuale all'interno della
    # lista. L'individuo, pertanto, segue la forma:
    # [False, True, False, True, True, False, True, False]
    def generate(self, individual_dim):
        # definizione del genoma dell'individuo
        genome = list()

        # settaggio iniziale del genoma con
        # i geni tutti a False per ogni dimensione
        for i in range(len(individual_dim)):
            dimension = list()
            for j in range(0, individual_dim[i]):
                dimension.append(False)
            genome.append(dimension)

        # definizione di un numero casuale di geni impostati
        # secondo la sequenza
        max_genes = 0
        for num_elements in individual_dim:
            max_genes += num_elements
        random_set_genes = random.randint(1, max_genes - 1)

        # per ogni elemento nella sequenza
        for sequence_number in range(random_set_genes):

            # definizione di un indice casuale dove inserire
            # il gene della sequenza
            random_dimension = random.randint(0, len(individual_dim) - 1)
            random_index = random.randint(0, individual_dim[random_dimension] - 1)

            # se all'indice e dimensione determinate esiste gia un elemento
            # si definisce un nuovo indice e/o una nuova dimesnione
            while genome[random_dimension][random_index]:
                random_dimension = random.randint(0, len(individual_dim) - 1)
                random_index = random.randint(0, individual_dim[random_dimension] - 1)

            # definizione del valore del gene dell'individuo
            # all'indice valutato
            genome[random_dimension][random_index] = True

        print("\nINDIVIDUAL GENERATED: \n", genome)

        # ritorna il genoma dal quale definire l'individuo
        return genome

    # Funzione di valutazione dell'individuo
    def evaluate(self, individual):
        # definizione della variabile di valutazione
        valutation = 0

        # per ogni attributo dell'individuo
        for dimension_index in range(individual.get_dimensions_number()):
            for gene_index in range(individual.get_dimension_size(dimension_index)):
                # se è diverso da False aumenta la valutazione
                if individual.get_cut(dimension_index, gene_index):
                    valutation = valutation + 1

        # calcolo del numero di attributi dell'individuo
        mass = 0
        for dimension_index in range(individual.get_dimensions_number()):
            mass += individual.get_dimension_size(dimension_index)

        # restituisce la valutazione finale
        return valutation / mass

    # Funzione per la creazione degli individui
    # Restituisce il genome dell'individuo ottimali
    def create(self, individual_dim, population_size, generations,
               mutation_rate, mating_rate, selected_for_tournament,
               selected_best):

        # definizione di un oggetto per la creazione della guida genetica
        genetic_guide: GeneticEvolution = DeapGeneticGuide(self.evaluate,
                                                           self.generate,
                                                           individual_dim,
                                                           mutation_rate,
                                                           mating_rate,
                                                           selected_for_tournament)

        # evoluzione e acquisizione dell'individuo migliore dalla guida genetica
        self.genome = genetic_guide.evolve(population_size,
                                           generations,
                                           selected_best)[0]






S_d_b.from_binary(generate(individual_dims))
value = evaluate(S_d_b)
print(value)
# print("ok")
'''

# Numero di attributi dell'individuo
individual_size = 0
for i in individual_dims:
    individual_size += i

# Numero di individui selezionati per la
# selezione per torneo
selected_for_tournament = 5

# Numero di individui
# N.B. Per evitare la convergenza è utile inserire
# la grandezza della popolazione maggiore del
# numero di generazioni
population_size = 200

# Generazioni di evoluzioni della popolazione
generations = 50

# grado di mutazione (percentuale)
mutation_rate = 0.2

# grado di accoppiamento (percentuale)
mating_rate = 0.5

# numero di individui finali acquisiti
selected_best = 10

individual = Individual(individual_size, population_size, generations, mutation_rate, mating_rate,
                        selected_for_tournament, selected_best)
print("ok")

'''
# definizione di un oggetto per la creazione della guida genetica
genetic_guide: GeneticEvolution = DeapGeneticGuide(evaluate, generate, individual_size,
                                                   mutation_rate,
                                                   mating_rate,
                                                   selected_for_tournament)

# evoluzione e acquisizione degli individui
# migliori dalla guida genetica
best_individuals = genetic_guide.evolve(population_size,
                                        generations,
                                        selected_best)

# stampa a video di ogni individuo
print("\n---------------------------------------------------------")
for individual in best_individuals:
    print("\nFINAL INDIVIDUAL: \n", individual)
'''
