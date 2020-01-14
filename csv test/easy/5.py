import csv
import random

import numpy as numpy
from pyeasyga import pyeasyga

pop = [50, 100, 150, 200, 250, 300, 350, 400]
crossover_pb = [0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
mut_pb = 0.02


# define and set function to create a candidate solution representation
def create_individual(data):
    return [random.randint(0, 1) for _ in range(len(data))]


NUMMAX = 5
a = numpy.random.rand(NUMMAX, 2)
c = numpy.random.rand(NUMMAX)


# define a fitness function
def fitness(individual, seed_data):
    return sum((1. / (c[i] + sum((individual - aij) ** 2 for j, aij in enumerate(a[i])))) for i in range(len(c))),


for i in range(8):
    list = []
    list.append('F5')
    for j in range(8):
        # setup seed data
        seed_data = [numpy.random.uniform(-6.5336, 6.5336, size=25)]
        # initialise the GA
        ga = pyeasyga.GeneticAlgorithm(seed_data,
                                       population_size=pop[i],
                                       generations=100,
                                       crossover_probability=crossover_pb[j],
                                       mutation_probability=mut_pb,
                                       maximise_fitness=False)

        ga.fitness_function = fitness

        ga.create_individual = create_individual

        ga.run()  # run the GA
        fit, gene = ga.best_individual()
        print(fit)

        list.append(str(fit))

    with open('HOF' + str(pop[i]) + '.csv', mode='a') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,
                                dialect='excel')

        csv_writer.writerow(list)
