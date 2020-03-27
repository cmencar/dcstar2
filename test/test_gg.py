# -*- coding: utf-8 -*-
import random
from genetic_algorithm.genetic_evolution import GeneticEvolution
from genetic_algorithm.deap_genetic_guide import DeapGeneticGuide
import sys
sys.path.append('../')


# TEST EFFETTUATO SULL'USO DELLA CLASSE DEAPGENETICGUIDE
# NELL'USO DELLA GUIDA GENETICA (INDIPENDENTEMENTE DA A*)

# Inizializzatore dei numeri casuali
random.seed()


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

    # settaggio iniziale del genoma con
    # i geni tutti a zero
    for i in range(individual_dim):
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
        while genome[random_index] != 0:
            random_index = random.randint(0, individual_dim - 1)

        # definizione del valore del gene dell'individuo
        # all'indice valutato
        genome[random_index] = True

    print("\nINDIVIDUAL GENERATED: \n", genome)

    # ritorna il genoma dal quale definire l'individuo
    return individual_class(genome)


# Funzione di valutazione dell'individuo
def evaluate(individual):
    # definizione della variabile di valutazione
    valutation = 0

    # per ogni attributo dell'individuo
    for gene in individual:

        # se è diverso da zero aumenta la valutazione
        if not gene:
            valutation = valutation + 1

    # restituisce la valutazione finale
    return valutation / len(individual),


# Numero di attributi dell'individuo
individual_size = 20

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

# definizione di un oggetto per la creazione della guida genetica
genetic_guide: GeneticEvolution = DeapGeneticGuide(evaluate,
                                                   generate,
                                                   individual_size,
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


