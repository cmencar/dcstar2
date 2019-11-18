import csv

import numpy

from pyevolve import Consts
from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import Mutators, Initializators, Crossovers

POPULATION = [50, 100, 150, 200, 250, 300, 350, 400]
CROSSOVER_PROB = [0.6, 0.65, 0.70, 0.75, 0.80, 0.85, 0.9, 0.95]
MUTATION_PROB = 0.02
MAX_GEN = 100

NUMMAX = 5
A = numpy.random.rand(NUMMAX, 2)
C = numpy.random.rand(NUMMAX)


def shekelf(xlist):
    a = A
    c = C
    return sum((1. / (c[i] + sum((xlist[j] - aij) ** 2 for j, aij in enumerate(a[i])))) for i in range(len(c)))



def main():
    for i in range(8):
        list =[]
        list.append('F5')
        for j in range(8):
            genome = G1DList.G1DList(size=25)
            genome.setParams(rangemin=-6.5336, rangemax=6.5336)
            genome.initializator.set(Initializators.G1DListInitializatorReal)
            genome.mutator.set(Mutators.G1DListMutatorRealGaussian)
            genome.evaluator.set(shekelf)
            genome.crossover.set(Crossovers.G1DListCrossoverUniform)

            ga = GSimpleGA.GSimpleGA(genome, seed=64)
            ga.setMinimax(Consts.minimaxType["minimize"])
            ga.setGenerations(MAX_GEN)
            ga.setCrossoverRate(CROSSOVER_PROB[j])
            ga.setMutationRate(MUTATION_PROB)
            ga.setPopulationSize(POPULATION[i])
            ga.evolve(freq_stats=20)
            best = ga.bestIndividual()
            list.append(str(best.fitness))

        with open('HOF' + str(POPULATION[i]) + '.csv', mode='a') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,
                                    dialect='excel')

            csv_writer.writerow(list)

if __name__ == "__main__":
    main()