import csv
from math import pi

from numpy.ma import sin, sqrt, cos

from pyevolve import G1DList, GSimpleGA, Crossovers
from pyevolve import Initializators, Mutators, Consts

POPULATION = [50, 100, 150, 200, 250, 300, 350, 400]
CROSSOVER_PROB = [0.6, 0.65, 0.70, 0.75, 0.80, 0.85, 0.9, 0.95]
MUTATION_PROB = 0.025
MAX_GEN = 100


def rastrigin(individual):
    """Rastrigin test objective function.

    .. list-table::
       :widths: 10 50
       :stub-columns: 1

       * - Type
         - minimization
       * - Range
         - :math:`x_i \in [-5.12, 5.12]`
       * - Global optima
         - :math:`x_i = 0, \\forall i \in \\lbrace 1 \\ldots N\\rbrace`, :math:`f(\mathbf{x}) = 0`
       * - Function
         - :math:`f(\\mathbf{x}) = 10N + \sum_{i=1}^N x_i^2 - 10 \\cos(2\\pi x_i)`

    .. plot:: code/benchmarks/rastrigin.py
       :width: 67 %
    """
    return 10 * len(individual) + sum(gene * gene - 10 * \
                        cos(2 * pi * gene) for gene in individual)


def main():
    for i in range(8):
        list =[]
        list.append('F7')
        for j in range(8):
            genome = G1DList.G1DList(size=20)
            genome.setParams(rangemin=-5.12, rangemax=5.12)
            genome.initializator.set(Initializators.G1DListInitializatorReal)
            genome.mutator.set(Mutators.G1DListMutatorRealGaussian)
            genome.evaluator.set(rastrigin)
            genome.crossover.set(Crossovers.G1DListCrossoverUniform)

            ga = GSimpleGA.GSimpleGA(genome, seed=64)
            ga.setMinimax(Consts.minimaxType["minimize"])
            ga.setGenerations(MAX_GEN)
            ga.setPopulationSize(POPULATION[i])
            ga.setCrossoverRate(CROSSOVER_PROB[j])
            ga.setMutationRate(MUTATION_PROB)

            ga.evolve(freq_stats=20)
            best = ga.bestIndividual()
            list.append(round(best.fitness, 2))

        with open('HOF' + str(POPULATION[i]) + '.csv', mode='a') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,
                                    dialect='excel')

            csv_writer.writerow(list)


if __name__ == "__main__":
    main()
