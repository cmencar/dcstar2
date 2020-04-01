# -*- coding: utf-8 -*-
import random
# import matplotlib.pyplot as plt
from genetic_algorithm.deap_genetic_guide import DeapGeneticGuide
from cut_sequences.cuts_sequence import CutsSequence
from cut_sequences.selected_cuts_sequence import SelectedCutsSequence
from cut_sequences.dimensional_sequence_binary import DimensionalSequenceBinary
from cut_sequences.point import Point
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
T_d_example = CutsSequence([[.28495, .34275, .40225, .625675, .8495, .9495], [.120045, .29, .34105, .3437, .37265, .4722]])

# calculate the size of each dimension of cuts sequence
genes_per_dimension = list()
for dimension in range(T_d_example.get_dimensions_number()):
    genes_per_dimension.append(len(T_d_example.get_dimension(dimension)))

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

# define DGG object to create the genetic guide with monodimensional lists
genetic_guide = DeapGeneticGuide(evaluate, generate, genes_number, mutation_rate, mating_rate, selected_for_tournament,
                                 T_d_example, points_example, genes_per_dimension)

# evolution and acquisition of best individuals from genetic guide with monodimensional lists
best_individuals = genetic_guide.evolve(population_size, generations, selected_best)

# convert from monodimensional list to binary cuts sequence
# initialize list of sequences (multidimensional individuals) and other support lists
list_of_sequences = list()
sequence = list()
dimension = list()
# for each individual in the best's list
for individual in best_individuals:
    # initialize index, offset for keeping track of the dimensions to create and clear support sequence list
    sequence.clear()
    offset = 0
    i = 0
    # for each number of genes of the dimension that is going to be created
    for num_elem in genes_per_dimension:
        # clear "dimension" support list
        dimension.clear()
        # increment offset by the number of elements that are going into the evaluated dimension
        offset = offset + num_elem
        # while there are genes
        while i < offset:
            # append into "dimension" support list the evaluated gene and increment index
            dimension.append(individual[i])
            i += 1
        # append a copy of created "dimension" into "sequence" support list
        sequence.append(dimension.copy())
    # append a copy of created "sequence" into the list of sequences
    list_of_sequences.append(sequence.copy())

# create selected cuts sequence and binary dimensional sequence objects
S_d = SelectedCutsSequence()
S_d_b = DimensionalSequenceBinary()

# show every "pure" individual or a "not found" message
print("\n---------------------------------------------------------")
# set flag to "pure individual not found"
no_pure = True
# for each individual in the list of sequences
for individual in list_of_sequences:
    # generate binary sequence from the individual
    S_d_b.from_binary(individual)
    # generate selected cuts sequence from cuts sequence and newly generated binary sequence
    S_d.from_binary(T_d_example, S_d_b)
    # create set of hyperboxes from selected cuts sequence, points list, m_d and M_d
    hyperboxes = S_d.generate_hyperboxes_set(points_example, 0, 1)
    # if all of the hyperboxes generated are pure
    if hyperboxes.get_impure_hyperboxes_number() == 0:
        # print the pure individual and set flag to False
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
# if none of the individuals generated has all pure hyperboxes show a message
if no_pure:
    print("\nNONE OF THE GENERATED INDIVIDUALS HAS PURE HYPERBOXES")
