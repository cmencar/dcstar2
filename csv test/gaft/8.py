from __future__ import division

import csv
import math
import random
from collections import Sequence
from functools import reduce
from itertools import repeat
from operator import mul

from gaft import GAEngine
from gaft.analysis import FitnessStore
from gaft.components import DecimalIndividual, Population
from gaft.operators import TournamentSelection, UniformCrossover
from gaft.plugin_interfaces import OnTheFlyAnalysis
from gaft.plugin_interfaces.operators.mutation import Mutation


# Built-in best fitness analysis.


# mutation
class mutGaussian(Mutation):
    def __init__(self, pm):
        if pm <= 0.0 or pm > 1.0:
            raise ValueError('Invalid mutation probability')

        self.pm = pm

    def mutate(self, individual, engine):

        ''' Mutate the individual.

        :param individual: The individual on which crossover operation occurs
        :type individual: :obj:`gaft.components.IndividualBase`

        :param engine: Current genetic algorithm engine
        :type engine: :obj:`gaft.engine.GAEngine`

        :return: A mutated individual
        :rtype: :obj:`gaft.components.IndividualBase`
        '''
        do_mutation = True if random.random() <= self.pm else False

        if do_mutation:
            size = len(individual.chromsome)
            mu = 0.1
            sigma = 1
            if not isinstance(mu, Sequence):
                mu = repeat(mu, size)
            elif len(mu) < size:
                raise IndexError("mu must be at least the size of individual: %d < %d" % (len(mu), size))
            if not isinstance(sigma, Sequence):
                sigma = repeat(sigma, size)
            elif len(sigma) < size:
                raise IndexError("sigma must be at least the size of individual: %d < %d" % (len(sigma), size))

            for i, m, s in zip(range(size), mu, sigma):
                if random.random() < self.pm:
                    individual.chromsome[i] += random.gauss(m, s)
            # Update solution.
            individual.solution = individual.decode()

        return individual


if '__main__' == __name__:

    pop = [50, 100, 150, 200, 250, 300, 350, 400]
    crossover_pb = [0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
    mut_pb = 0.05
    # fixed
    mutation = mutGaussian(pm=mut_pb)
    indv_template = DecimalIndividual(ranges=[(-600, 600)], eps=0.0000000001)
    selection = TournamentSelection()
    for i in range(8):
        list = []
        list.append('F8')
        for j in range(8):
            # changable
            population = Population(indv_template=indv_template, size=pop[i]).init()
            crossover = UniformCrossover(pc=0.8, pe=crossover_pb[j])

            # Create genetic algorithm engine.
            engine = GAEngine(population=population, selection=selection,
                              crossover=crossover, mutation=mutation, analysis=[FitnessStore])


            # fitness
            @engine.fitness_register
            def fitness(individual):
                return 1.0 / 4000.0 * sum(x**2 for x in individual.chromsome) - \
                       reduce(mul, (math.cos(x / math.sqrt(i + 1.0)) for i, x in enumerate(individual.chromsome)), 1) + 1

            @engine.analysis_register
            class ConsoleOutputAnalysis(OnTheFlyAnalysis):
                interval = 1
                master_only = True

                def register_step(self, g, population, engine):
                    best_indv = population.best_indv(engine.fitness)
                    msg = 'Generation: {}, best fitness: {:.3f}'.format(g, engine.ori_fmax)
                    self.logger.info(msg)

                def finalize(self, population, engine):
                    best_indv = population.best_indv(engine.fitness)
                    x = best_indv.solution
                    y = engine.ori_fmax
                    msg = 'Optimal solution: ({}, {})'.format(x, y)
                    list.append(str(y))
                    self.logger.info(msg)


            engine.run(ng=100)
        with open('HOF' + str(pop[i]) + '.csv', mode='a') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,
                                    dialect='excel')

            csv_writer.writerow(list)