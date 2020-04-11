# -*- coding: utf-8 -*-
import random
from genetic_algorithm.deap_genetic_guide import DeapGeneticGuide
from cut_sequences.cuts_sequence import CutsSequence
from cut_sequences.dimensional_sequence_binary import DimensionalSequenceBinary
from cut_sequences.selected_cuts_sequence import SelectedCutsSequence
from cut_sequences.point import Point
from matplotlib import pyplot as plt
import sys
sys.path.append('../')


# TESTING CLASS DEAPGENETICGUIDE (WITHOUT A*)

# Function that generates an individual with the same number of cuts as the cuts sequence
# @individual_class: class of the individual to create
# @individual_dim: number of genes of the individual
def generate(individual_class, individual_dim):
    # definition of individual's genome
    genome = list()

    # initializing the genome with all genes to False
    for gene in range(individual_dim):
        genome.append(False)

    # definition of a random number of genes to be modified
    random_set_genes = random.randint(2, individual_dim)

    # for "random_set_genes" times
    for i in range(random_set_genes):

        # definition of a random index where to change the gene
        random_index = random.randint(0, individual_dim - 1)

        # if in the given index there's a gene already changed, define a new index
        while genome[random_index]:
            random_index = random.randint(0, individual_dim - 1)

        # change the value of the evaluated gene with the defined index
        genome[random_index] = True

    # print("\nINDIVIDUAL GENERATED: \n", genome)

    # return the individual with the created genome
    return individual_class(genome)

# Function that evaluates the ratio between the "true" genes (considered cuts) and the whole number of them
# (considered cuts and not)
# @individual: object that contains the genome
def evaluate(individual):
    # initializing evaluation variables
    valutation = 0
    total_genes = 0
    # every "true" gene increments the valutation while the total number of genes is calculated
    valutation += individual.count(True)
    total_genes += len(individual)
    # returns the ratio
    return valutation / total_genes


# initialize the seed for random numbers
random.seed()

# define of example prototypes and cuts
points_example = [
    Point(coordinates=[.2354, .34], label="prototype_1", name="point_A"),
    Point(coordinates=[.3345, .3421], label="prototype_1", name="point_B"),
    Point(coordinates=[.351, .3453], label="prototype_2", name="point_C"),
    Point(coordinates=[.45235, .00009], label="prototype_1", name="point_D"),
    Point(coordinates=[.9, .5444], label="prototype_1", name="point_E"),
    Point(coordinates=[.999, .4], label="prototype_2", name="point_F"),
    Point(coordinates=[.799, .24], label="prototype_1", name="point_G")
]
T_d_example = CutsSequence([[.28495, .34275, .40225, .625675, .8495, .9495], [.120045, .29, .34105, .3437, .37265,
                                                                              .4722]])
print("------------------------Prototypes------------------------")
for point in points_example:
    print("Point coordinates: ", point.get_coordinates(),
          "\nPoint label: ", point.get_label(),
          "\nPoint name: ", point.get_name())
print("---------------------Cuts sequence T_d--------------------")
T_d_example.debug_print()

# calculate the size of each dimension of cuts sequence
genes_per_dimension = list()
for dimension in range(T_d_example.get_dimensions_number()):
    genes_per_dimension.append(len(T_d_example.get_dimension(dimension)))
    print("Cuts in dimension ", dimension + 1, ":", len(T_d_example.get_dimension(dimension)))

# set m_d and M_d limits
m_d = 0
M_d = 1
print("----------------------Limits in S_d-----------------------",
      "\nm_d: ", m_d, "   M_d: ", M_d)
# calculate the total number of genes that the genome will have
genes_number = 0
for num in genes_per_dimension:
    genes_number += num

# set number of individuals for tournament selection
selected_for_tournament = 5

# calculate population
# N.B.: population is given by duplicating the number of genes in the genome
population_size = 2 * genes_number

# set number of generations
generations = 20

# calculate mutation rate
# N.B.: mutation rate is calculated by reciprocating the number of genes
mutation_rate = 1 / genes_number

# set mating rate
mating_rate = 0.7

# set number of best individuals to retrieve
selected_best = 10

print("------------------------Parameters------------------------",
      "\nIndividual dimension: ", genes_number,
      "\nNumber of individuals for tournament selection: ", selected_for_tournament,
      "\nPopulation size: ", population_size,
      "\nGenerations to create: ", generations,
      "\nMutation rate: ", mutation_rate,
      "\nMating rate: ", mating_rate,
      "\nNumber of best individuals to choose from: ", selected_best)

# define DGG object to create the genetic guide with monodimensional lists
genetic_guide = DeapGeneticGuide(evaluate, generate, genes_number, mutation_rate, mating_rate, selected_for_tournament,
                                 T_d_example, points_example, genes_per_dimension, m_d, M_d)

# evolution and acquisition of the best individual from genetic guide with monodimensional lists
best_individual = genetic_guide.evolve(population_size, generations, selected_best)

# print the best possible individual
print("\nBEST POSSIBLE PURE INDIVIDUAL: \n", best_individual)

# best_case_scenario_example = [[False, False, False, False, False, False], [False, False, False, True, False, True]]

# create selected sequence with generated dimensional sequence
S_d_bin_example = DimensionalSequenceBinary()
S_d_bin_example.from_binary(best_individual)
S_d_example = SelectedCutsSequence()
S_d_example.from_binary(T_d_example, S_d_bin_example)

# create the plot
for cut in S_d_example.get_dimension(0):
    plt.plot([cut, cut], [0, 1], 'k', linestyle='--', color='black')

for cut in S_d_example.get_dimension(1):
    plt.plot([0, 1], [cut, cut], linestyle='--', color='black')

for point in points_example:
    color = 'ko'

    if point.get_label() == "prototype_1":
        color = 'ro'
    elif point.get_label() == "prototype_2":
        color = 'bo'

    plt.plot(point.get_coordinate(0), point.get_coordinate(1), color)

# show the plot
plt.show()

# get the average number of cuts in 100 individual
print("\nCalculating average of active cuts in 100 individuals")
generated_individuals = list()
cuts_generated = 0
for i in range(100):
    generated_individuals.append(genetic_guide.evolve(population_size, generations, selected_best))
    print("N°", i, "individual: ", generated_individuals[i])
    active_cuts_ind = 0
    for dimension in generated_individuals[i]:
        for gene in dimension:
            if gene:
                active_cuts_ind += 1
    print("Active cuts into individual: ", active_cuts_ind)
    cuts_generated += active_cuts_ind
avg_cuts_generated = cuts_generated / 100
print("\nAVERAGE ACTIVE CUTS: ", avg_cuts_generated)
