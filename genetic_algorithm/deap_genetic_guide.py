# -*- coding: utf-8 -*-

from deap import creator, base, tools, algorithms
from genetic_algorithm.genetic_evolution import GeneticEvolution
from cut_sequences.cuts_sequence import CutsSequence
from cut_sequences.selected_cuts_sequence import SelectedCutsSequence
from cut_sequences.dimensional_sequence_binary import DimensionalSequenceBinary


# Class for utilization of genetic guide using DEAP
class DeapGeneticGuide(GeneticEvolution):

    # Definition constructor class
    # @evaluate_fun: passed function that evaluates the individual
    # @generate_fun: passed function that generates the individual
    # @individual_size: number of attributes for each individual
    # @mutation_rate: percentage of mutation
    # @mating_rate: mating ratio
    # @selected_individuals: number of individuals selected in the phase of selection of the best individuals
    # (selection by tournament)
    # @cuts_sequence: sequence of cuts T_d
    # @points_list: list of prototypes
    # @elements_per_dimension: number of elements per dimension of given cuts_sequence for convertion from list
    # to sequence
    def __init__(self, evaluate_fun, generate_fun, individual_size,
                 mutation_rate, mating_rate, selected_individuals, cuts_sequence, points_list, elements_per_dimension):

        # define mutation rate of individual
        self.mutation_rate = mutation_rate

        # define mating rate of individual
        self.mating_rate = mating_rate

        # create object defining max fitness value
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))

        # create object defining individual
        creator.create("Individual", list, fitness=creator.FitnessMax)

        # define toolbox for needed methods
        self.toolbox = base.Toolbox()

        # define individual, which will be generated by a given "generate_fun" function
        self.toolbox.register("individual", generate_fun, creator.Individual, individual_size)

        # define data structure "population" containing all individuals
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        # define mating method between individuals using uniform partially matched crossover
        self.toolbox.register("mate", tools.cxUniformPartialyMatched, indpb=0)

        # define mutation method of individuals' son shuffling genes with "mutation_rate" percentage
        self.toolbox.register("mutate", tools.mutShuffleIndexes, indpb=mutation_rate)

        # define selection method using selection for tournament between "selected_individuals" individuals
        self.toolbox.register("select", tools.selTournament, tournsize=selected_individuals)

        # define evaluation method with given "evaluate_fun" function
        self.toolbox.register("evaluate", evaluate_fun)

        # save cuts_sequence, points_list, individual_size and element_per_dimension, needed for convertion from
        # monodimensional list to sequence in "pureness" function
        self.T_d = cuts_sequence
        self.points_list = points_list
        self.individual_size = individual_size
        self.elements_per_dimension = elements_per_dimension

    # Individual evaluation method
    def evaluate(self, individual):
        pass

    # Individual generator method
    def generate(self):
        pass

    # Method generating best individuals by the genetic algorithm
    # @population_size: number of individuals to generate
    # @generations: number of generations to create
    # @selected_best: list of best individuals generated
    def evolve(self, population_size, generations, selected_best):

        # create a population of "population_size" individuals using the given "generate_fun" function
        population = self.toolbox.population(n=population_size)

        # for each generation
        for epoch in range(generations):

            # offsprings are generated using the varAnd algorithm, in which are passed the population, mating rate and
            # mutation rate
            # in this are used the previous defined methods in the toolbox, such as mutation, crossover, evaluation and
            # selection
            offsprings = algorithms.varAnd(population, self.toolbox, self.mating_rate, self.mutation_rate)

            # create a list of fitness values of the offsprings
            son_fitness = list()
            for son in offsprings:
                son_fitness.append(self.fitness(son, self.T_d, self.points_list))

            # map each fitness value to the corresponding offspring
            for fit, ind in zip(son_fitness, offsprings):
                ind.fitness.value = fit

            # select a number of offsprings equal to the number of individuals in the population
            # the selection is defined on a "selected_individual" number of offsprings
            population = self.toolbox.select(offsprings, k=len(population))

        # return a selection of "selected_best" number of individuals with the highest fitness value
        return tools.selBest(population, selected_best, fit_attr="fitness.value")

    # Method defining the fitness value of an individual
    # @individual: individual's genome
    # @T_d: reference cuts sequence
    # @points_list: list of prototypes
    def fitness(self, individual, T_d, points_list):
        # return the calculated fitness value
        return (1 - self.toolbox.evaluate(individual)) * pow(self.pureness(individual, T_d, points_list,
                                                                           self.elements_per_dimension), 5)

    # Method that calculates the pureness of a given individual's genome
    # @individual: individual's genome
    # @T_d: reference cuts sequence
    # @points_list: list of prototypes
    # @elements_per_dimension: number of elements in each dimension of reference T_d
    # @m_d: minimum cut for each dimension
    # @M_d: maximum cut for each dimension
    def pureness(self, individual, T_d, points_list, elements_per_dimension, m_d=0, M_d=1):
        # initializing selected cuts and binary cuts sequences
        S_d = SelectedCutsSequence()
        S_d_b = DimensionalSequenceBinary()

        # convert individual from monodimensional list to "multidimensional cut sequence"
        converted_individual = self.from_monodim_ind_to_multidim_ind(individual, elements_per_dimension)

        # create binary cuts sequence
        S_d_b.from_binary(converted_individual)
        # generate selected cuts sequence from reference T_d and binary cuts sequence
        S_d.from_binary(T_d, S_d_b)

        # create set of hyperboxes
        hyperboxes = S_d.generate_hyperboxes_set(points_list, m_d, M_d)

        # return ratio between number of pure hyperboxes and total number of hyperboxes
        return hyperboxes.get_pure_hyperboxes_number() / hyperboxes.get_hyperboxes_number()

    # Method converting individual's genome from list to "multidimensional cuts sequence"
    # @individual: individual's genome
    # @genes_per_dimension: numbers of genes per dimension
    def from_monodim_ind_to_multidim_ind(self, individual, genes_per_dimension):
        sequence = list()
        dimension = list()
        offset = 0
        i = 0
        for num_elem in genes_per_dimension:
            dimension.clear()
            offset = offset + num_elem
            while i < offset:
                dimension.append(individual[i])
                i += 1
            sequence.append(dimension.copy())
        return sequence
