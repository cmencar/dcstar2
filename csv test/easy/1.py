import csv
import random

import numpy as numpy
from pyeasyga import pyeasyga

pop = [50, 100, 150, 200, 250, 300, 350, 400]
crossover_pb = [0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
mut_pb = 0.25
cr_csv = ['', '0.6', '0.65', '0.7', '0.75', '0.8', '0.85', '0.9', '0.95']


# define and set function to create a candidate solution representation
def create_individual(data):
    individual = data[:]
    random.shuffle(individual)
    return individual


# define a fitness function
def fitness(individual, seed_data):
    return sum(gene * gene for gene in individual)


for i in range(8):
    list = []
    list.append('F1')
    for j in range(8):
        # setup seed data
        seed_data = numpy.random.uniform(-5.12, 5.12, size=2)
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
        print("run")
        fit, gene = ga.best_individual()
        print(fit)
        list.append(str(fit))

    with open('HOF' + str(pop[i]) + '.csv', mode='a') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,
                                dialect='excel')
        csv_writer.writerow(cr_csv)
        csv_writer.writerow(list)
