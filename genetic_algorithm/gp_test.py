# -*- coding: utf-8 -*-

import random
from math import fabs
from operator import attrgetter
from genetic_algorithm.genetic_evolution import GeneticEvolution
from cut_sequences.selected_dimensional_sequence_numeric import SelectedDimensionalSequenceNumeric
from cut_sequences.dimensional_sequence_binary import DimensionalSequenceBinary
from matplotlib import pyplot as plt
import numpy as np


class Individual:
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = 0

    def set_chromosome(self, chromosome):
        self.chromosome = chromosome

    def get_chromosome(self):
        return self.chromosome

    def set_fitness(self, score):
        self.fitness = score

    def get_fitness(self):
        return self.fitness


# Class for utilization of genetic guide
class GeneticGuideSequenceProblem(GeneticEvolution):

    # Definition constructor class
    # @individual_size: number of attributes for each individual
    # @mutation_rate: percentage of mutation
    # @mating_rate: mating ratio
    # @selected_individuals: number of individuals selected in the phase of selection of the best individuals
    # (selection by tournament)
    # @cuts_sequence: sequence of cuts T_d
    # @points_list: list of prototypes
    # @elements_per_dimension: number of elements per dimension of given cuts_sequence for convertion from chromosome
    # to sequence
    # @min_cut: m_d cut that will go into S_d
    # @max_cut: M_d cut that will go into S_d
    def __init__(self, individual_size, mutation_rate, mating_rate, selected_for_tournament, cuts_sequence, points_list,
                 elements_per_dimension, min_cut, max_cut):

        # initialize the seed for random numbers
        random.seed()

        # define mutation rate of individual
        self.mut_rate = mutation_rate

        # define mating rate of individual
        self.cx_rate = mating_rate

        # define how many individuals are to be selected for tournament
        self.selected_for_tournament = selected_for_tournament

        # save cuts_sequence, points_list, individual_size and element_per_dimension, needed for convertion from
        # chromosome to sequence
        self.T_d = cuts_sequence
        self.points_list = points_list
        self.individual_size = individual_size
        self.elements_per_dimension = elements_per_dimension

        # save m_d and M_d limits to generate S_d sequence
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

    # Method that calculates the pureness of a given individual's genome
    # @individual: individual
    def pureness(self, individual):
        # initializing selected cuts and binary cuts sequences
        S_d = SelectedDimensionalSequenceNumeric()
        S_d_b = DimensionalSequenceBinary()

        # convert individual into sequence
        converted_individual = self.convert_individual_into_sequence(individual, self.elements_per_dimension)

        # create binary cuts sequence
        S_d_b.from_binary(converted_individual)
        # generate selected cuts sequence from reference T_d and binary cuts sequence
        S_d.from_binary(self.T_d, S_d_b)

        # create set of hyperboxes
        hyperboxes = S_d.generate_hyperboxes_set(self.points_list, self.m_d, self.M_d)

        # return ratio between number of pure hyperboxes and total number of hyperboxes
        return hyperboxes.get_pure_hyperboxes_number() / hyperboxes.get_hyperboxes_number()

    # Method defining the fitness value of an individual
    # @individual: individual
    def calculate_fitness(self, individual):
        # return the calculated fitness value
        return (1 - self.evaluate(individual)) * pow(self.pureness(individual), 5)

    # Method converting individual's genome from list to "multidimensional cuts sequence" (list of lists)
    # @individual: individual
    # @genes_per_dimension: numbers of genes per dimension
    def convert_individual_into_sequence(self, individual, genes_per_dimension):
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

    # Method that applies tournament selection on given population
    def tournament_selection(self, individuals, k, tournsize):
        chosen = []
        aspirants = []
        for i in range(k):
            for j in range(tournsize):
                aspirants.append(individuals[random.randint(0, k - 1)])
            chosen.append(max(aspirants, key=attrgetter("fitness")))
            aspirants.clear()
        return chosen

    # Function that generates an individual with the same number of cuts as the cuts sequence
    # @individual_class: class of the individual to create
    # @individual_dim: number of genes of the individual
    def generate(self, individual_dim):
        # definition of individual's genome
        genome = list()

        # initializing the genome with all genes to False
        for gene in range(individual_dim):
            genome.append(False)

        # return the individual with the created genome
        return Individual(genome)

    # Method that applies crossover to a couple of individuals
    def mate(self, individual_1, individual_2, cx_rate):
        chromosome1 = individual_1.get_chromosome().copy()
        chromosome2 = individual_2.get_chromosome().copy()
        for idx in range(self.individual_size):
            if random.random() <= cx_rate:
                temp = chromosome1[idx]
                chromosome1[idx] = chromosome2[idx]
                chromosome2[idx] = temp
        individual_1.set_chromosome(chromosome1)
        individual_2.set_chromosome(chromosome2)
        # return individual_1, individual_2

    # Method that mutates an individual
    def mutate(self, individual, mut_rate):
        chromosome = individual.get_chromosome().copy()
        for idx in range(self.individual_size):
            if random.random() <= mut_rate:
                chromosome[idx] = not chromosome[idx]
        individual.set_chromosome(chromosome)
        # return individual

    # Method that generates a offspring population of population_size using "mate" and "mutate" methods
    # @population: list of individuals
    # @population_size: size of population to generate
    # @toolbox: container of utility functions
    # @mating_rate: mating ratio
    # @mutation_rate: mutation_ratio
    # @elite: best individual
    def generate_offsprings(self, population, population_size, cx_rate, mut_rate, elite):
        offsprings = population.copy()
        # Apply crossover and mutation on the offsprings
        # for i in range(1, population_size):  # TODO - con elite, test
        for i in range(population_size):
            self.mate(offsprings[i - 1], offsprings[i], cx_rate)
            # if random.random() <= cx_rate:
                # offsprings[i - 1], offsprings[i] = self.mate(offsprings[i - 1], offsprings[i], cx_rate)
                # self.mate(offsprings[i - 1], offsprings[i], cx_rate)
        for i in range(population_size):
            self.mutate(offsprings[i], mut_rate)
            # if random.random() <= mut_rate:
                # offsprings[i] = self.mutate(offsprings[i], mut_rate)
                # self.mutate(offsprings[i], mut_rate)
        return offsprings

    # Method generating the best individual possible by the genetic algorithm
    # @population_size: size of population to generate
    # @generations: number of generations to create
    # @selected_best: number of best individuals to generate
    def evolve(self, population_size, generations, dataset):

        # create a population of "population_size" individuals
        population = list()
        for _ in range(population_size):
            population.append(self.generate(self.individual_size))

        fit_behave = list(tuple())  # TODO - valutazione fitness, test

        # "elite" initialization
        # TODO - con elite, test
        elite = Individual(list())
        elite.set_fitness(-1)

        epoch = 0
        stabilized_gens = 0

        # evolution
        # for epoch in range(generations - 1):
        # TODO - con criterio di stop "stabilizzazione", test
        while epoch in range(generations - 1) and stabilized_gens < 10:

            # offsprings generation
            offsprings = self.generate_offsprings(population, population_size, self.cx_rate, self.mut_rate, elite)

            # calculation of individuals "fitness"
            for son in offsprings:
                son.set_fitness(self.calculate_fitness(son.get_chromosome()))

            # TODO - valutazione fitness, da togliere
            eval_fitness = list()
            for son in offsprings:
                eval_fitness.append(son.get_fitness())
            current_max_fit = 0
            current_min_fit = 1
            temp_avg = 0
            for i in range(len(eval_fitness)):
                if eval_fitness[i] > current_max_fit:
                    current_max_fit = eval_fitness[i]
                if eval_fitness[i] < current_min_fit:
                    current_min_fit = eval_fitness[i]
                temp_avg += eval_fitness[i]
                current_avg_fit = temp_avg / population_size
            fit_behave.append((current_min_fit, current_avg_fit, current_max_fit))

            # TODO - elite, test
            # "elite" evaluation
            for _ in offsprings:
                if _.get_fitness() > elite.get_fitness():
                    print(elite.get_fitness(), " -> ", _.get_fitness())
                    # save the better individual
                    elite.set_chromosome(_.get_chromosome().copy())
                    elite.set_fitness(self.calculate_fitness(elite.get_chromosome()))
                    if elite.get_fitness() != _.get_fitness():
                        print("stronzo")

            # TODO - aggiunto altro criterio di stop "stabilizzazione", test
            # if fabs(previous_avg_fit - current_avg_fit) <= previous_avg_fit * 0.1:
            #     stabilized_gens += 1
            # else:
            #     stabilized_gens = 0
            # previous_avg_fit = current_avg_fit

            # applying tournament selection

            # TODO - con elite, test
            # elite_copy = Individual(elite.get_chromosome())
            # elite_copy.set_fitness(elite.get_fitness())
            # population.clear()
            # population.append(elite_copy)
            # not_elites = self.tournament_selection(offsprings, int(population_size - 1), self.selected_for_tournament)
            # for normie in not_elites:
            #     population.append(normie)

            # TODO - senza elite, test
            population = self.tournament_selection(offsprings, int(population_size), self.selected_for_tournament)

            epoch += 1

        # TODO - grafico valutazione fitness, da togliere
        min_ = list()
        avg_ = list()
        max_ = list()
        for fits in fit_behave:
            min_.append(fits[0])
            avg_.append(fits[1])
            max_.append(fits[2])
        x = np.linspace(0, len(fit_behave), len(fit_behave))
        plt.plot(x, min_, marker='.', color='red')
        plt.plot(x, avg_, marker='.', color='green')
        plt.plot(x, max_, marker='.', color='blue')
        plt.grid(True)
        # plt.show()
        plt.savefig(dataset + ".svg", transparent=True)
        plt.close()

        print("Best fitness: ", elite.get_fitness())  # TODO - valutazione fitness, test
        print("Best individual: ", elite.get_chromosome())  # TODO - valutazione individuo, test
        # print("Halt at generation:", epoch)  # TODO - doppio criterio di fermata "evolve", test
        # convert individual into sequence
        # best_individual = self.convert_individual_into_sequence(elite.get_chromosome(), self.elements_per_dimension)

        # return the converted best individual
        # return best_individual
        return elite.get_chromosome().count(True), self.individual_size
