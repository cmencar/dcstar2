# -*- coding: utf-8 -*-

import random
from deap import creator, base, tools, algorithms
from genetic_algorithm.genetic_evolution import GeneticEvolution
from cut_sequences.selected_dimensional_sequence_numeric import SelectedDimensionalSequenceNumeric
from cut_sequences.dimensional_sequence_binary import DimensionalSequenceBinary


# Class for utilization of genetic guide using DEAP
class DeapGeneticGuideSequenceProblem(GeneticEvolution):

    # Definition constructor class
    # @individual_size: number of attributes for each individual
    # @mutation_rate: percentage of mutation
    # @mating_rate: mating ratio
    # @selected_individuals: number of individuals selected in the phase of selection of the best individuals
    # (selection by tournament)
    # @cuts_sequence: sequence of cuts T_d
    # @points_list: list of prototypes
    # @elements_per_dimension: number of elements per dimension of given cuts_sequence for convertion from list
    # to sequence
    # @min_cut: m_d cut that will go into S_d
    # @max_cut: M_d cut that will go into S_d
    def __init__(self, individual_size, mutation_rate, mating_rate, selected_individuals, cuts_sequence, points_list,
                 elements_per_dimension, min_cut, max_cut):

        # initialize the seed for random numbers
        random.seed()

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
        self.toolbox.register("individual", self.generate, creator.Individual, individual_size)

        # define data structure "population" containing all individuals
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        # define mating method between individuals using uniform partially matched crossover
        self.toolbox.register("mate", tools.cxUniformPartialyMatched, indpb=mating_rate)

        # define mutation method of individuals' son shuffling genes with "mutation_rate" percentage
        self.toolbox.register("mutate", tools.mutShuffleIndexes, indpb=mutation_rate)

        # define selection method using selection for tournament between "selected_individuals" individuals
        self.toolbox.register("select", tools.selTournament, tournsize=selected_individuals)

        # define evaluation method with given "evaluate_fun" function
        self.toolbox.register("evaluate", self.evaluate)

        # save cuts_sequence, points_list, individual_size and element_per_dimension, needed for convertion from
        # monodimensional list to sequence in "pureness" function
        self.T_d = cuts_sequence
        self.points_list = points_list
        self.individual_size = individual_size
        self.elements_per_dimension = elements_per_dimension
        # save m_d and M_d limits to generate S_d sequence in "pureness" function
        self.m_d = min_cut
        self.M_d = max_cut

    # Function that evaluates the ratio between the "true" genes (considered cuts) and the whole number of them
    # (considered cuts and not)
    # @individual: object that contains the genome
    def evaluate(self, individual):
        # initializing evaluation variables
        valutation = 0
        total_genes = 0
        # every "true" gene increments the valutation while the total number of genes is calculated
        valutation += individual.count(True)
        total_genes += len(individual)
        # returns the ratio
        return valutation / total_genes

    # Function that generates an individual with the same number of cuts as the cuts sequence
    # @individual_class: class of the individual to create
    # @individual_dim: number of genes of the individual
    def generate(self, individual_class, individual_dim):
        # definition of individual's genome
        genome = list()

        # initializing the genome with all genes to False
        for gene in range(individual_dim):
            genome.append(False)
        '''
        # for every element into genome
        for index in range(individual_dim):
            # if generated float is bigger than 0.5
            if random.random() > 0.5:
                # set gene with evaluated index to True
                genome[index] = True
        '''
        for _ in range(int(individual_dim / 2)):
            genome[random.randint(0, individual_dim - 1)] = True
        # return the individual with the created genome
        return individual_class(genome)

    # Method generating best individuals by the genetic algorithm with <worst_case_scenario>
    # @population_size: size fo population to generate
    # @generations: number of generations to create
    # @selected_best: number of best individuals to generate
    def evolve(self, population_size, generations, selected_best):

        # create a population of "population_size" individuals
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
                son_fitness.append(self.fitness(son))

            # map each fitness value to the corresponding offspring
            for fit, ind in zip(son_fitness, offsprings):
                ind.fitness.value = fit

            # select a number of offsprings equal to the number of individuals in the population
            # the selection is defined on a "selected_individual" number of offsprings
            population = self.toolbox.select(offsprings, k=len(population))

        # select the "selected_best" number of best individuals with the highest fitness value
        best_individuals = tools.selBest(population, selected_best, fit_attr="fitness.value")

        # initialize list of sequences (multidimensional individuals)
        converted_best_individuals = list()

        # for each individual in the selected best
        for individual in best_individuals:
            # convert individual from monodimensional list to "binary cuts sequence"
            converted_best_individuals.append(self.from_list_to_sequence(individual,
                                                                         self.elements_per_dimension))
        # create selected cuts sequence and binary dimensional sequence objects
        S_d = SelectedDimensionalSequenceNumeric()
        S_d_b = DimensionalSequenceBinary()

        # for each individual in the best individuals generated
        for individual in converted_best_individuals:
            found = False

            # generate binary sequence from the individual
            S_d_b.from_binary(individual)

            # generate selected cuts sequence from cuts sequence and newly generated binary sequence
            S_d.from_binary(self.T_d, S_d_b)

            # create set of hyperboxes from selected cuts sequence, points list, m_d and M_d
            hyperboxes = S_d.generate_hyperboxes_set(self.points_list, self.m_d, self.M_d)

            # if all of the hyperboxes generated are pure
            if hyperboxes.get_impure_hyperboxes_number() == 0:
                # pick it as "best of the best"
                best_of_the_best = individual
                found = True

        # if is found a pure individual at least
        if found:
            # return the "best of the best"
            return best_of_the_best
        else:
            # return the "worst case scenario"
            return self.worst_case_scenario(self.elements_per_dimension)

    # Method generating best individuals by the genetic algorithm without <worst_case_scenario>
    # @population_size: size fo population to generate
    # @generations: number of generations to create
    # @selected_best: number of best individuals to generate
    def evolve_without_wsc(self, population_size, generations, selected_best):

        # create a population of "population_size" individuals
        population = self.toolbox.population(n=population_size)

        # TODO - valutazione fitness, da togliere
        fit_behave = list(tuple())

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
                son_fitness.append(self.fitness(son))

            # TODO - valutazione fitness, da togliere
            temp_max = 0
            temp_min = 2
            temp_avg = 0
            for i in range(len(son_fitness)):
                if son_fitness[i] > temp_max:
                    temp_max = son_fitness[i]
                if son_fitness[i] < temp_min:
                    temp_min = son_fitness[i]
                temp_avg += son_fitness[i]
            fit_behave.append((temp_min, temp_avg / len(son_fitness), temp_max))

            # map each fitness value to the corresponding offspring
            for fit, ind in zip(son_fitness, offsprings):
                ind.fitness.value = fit

            # select a number of offsprings equal to the number of individuals in the population
            # the selection is defined on a "selected_individual" number of offsprings
            population = self.toolbox.select(offsprings, k=len(population))

        # select the "selected_best" number of best individuals with the highest fitness value
        best_individuals = tools.selBest(population, selected_best, fit_attr="fitness.value")

        # convert individual from monodimensional list to "binary cuts sequence"
        converted_best_individual = self.from_list_to_sequence(best_individuals[0],
                                                               self.elements_per_dimension)

        # TODO - valutazione fitness, da togliere
        print(fit_behave)

        # return converted best individual
        return converted_best_individual

    # Method defining the fitness value of an individual
    # @individual: individual's genome
    def fitness(self, individual):
        # return the calculated fitness value
        return (1 - self.toolbox.evaluate(individual)) * pow(self.pureness(individual), 5)

    # Method that calculates the pureness of a given individual's genome
    # @individual: individual's genome
    def pureness(self, individual):
        # initializing selected cuts and binary cuts sequences
        S_d = SelectedDimensionalSequenceNumeric()
        S_d_b = DimensionalSequenceBinary()

        # convert individual from monodimensional list to "multidimensional cut sequence"
        converted_individual = self.from_list_to_sequence(individual, self.elements_per_dimension)

        # create binary cuts sequence
        S_d_b.from_binary(converted_individual)
        # generate selected cuts sequence from reference T_d and binary cuts sequence
        S_d.from_binary(self.T_d, S_d_b)

        # create set of hyperboxes
        hyperboxes = S_d.generate_hyperboxes_set(self.points_list, self.m_d, self.M_d)

        # return ratio between number of pure hyperboxes and total number of hyperboxes
        return hyperboxes.get_pure_hyperboxes_number() / hyperboxes.get_hyperboxes_number()

    # Method converting individual's genome from list to "multidimensional cuts sequence" (list of lists)
    # @individual: individual's genome
    # @genes_per_dimension: numbers of genes per dimension
    def from_list_to_sequence(self, individual, genes_per_dimension):
        # create support lists
        sequence = list()
        dimension = list()

        # initialize index and offset variables
        offset = 0
        i = 0
        # for each dimension
        for num_elem in genes_per_dimension:
            # clear the "dimension" support list
            dimension.clear()
            # increment the offset that limits how many genes are copied into given dimension
            offset = offset + num_elem

            # while index doesn't reach the max elements in given dimension
            while i < offset:
                # append into given dimension the gene with given index from individual
                dimension.append(individual[i])
                # increment index
                i += 1
            # append a copy of the newly created dimension into sequence
            sequence.append(dimension.copy())
        return sequence

    # Method for the worst case scenario, generates a sequence with all the possible cuts active
    # @elements_per_dimension: number of cuts per dimension
    def worst_case_scenario(self, elements_per_dimension):
        # create support lists
        sequence = list()
        dimension = list()

        # for each dimension
        for dim in range(len(elements_per_dimension)):
            # clear the "dimension" support list
            dimension.clear()

            # for each element in given dimension
            for num in range(elements_per_dimension[dim]):
                # append True into dimension
                dimension.append(True)
            # append a copy of the newly created dimension into sequence
            sequence.append(dimension.copy())
        return sequence
