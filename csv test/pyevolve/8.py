import csv
from math import pi
from operator import mul

from numpy.ma import sin, sqrt, cos

from pyevolve import G1DList, GSimpleGA, Crossovers
from pyevolve import Initializators, Mutators, Consts

POPULATION = [50, 100, 150, 200, 250, 300, 350, 400]
CROSSOVER_PROB = [0.6, 0.65, 0.70, 0.75, 0.80, 0.85, 0.9, 0.95]
MUTATION_PROB = 0.05
MAX_GEN = 100


def griewank(individual):
    """Griewank test objective function.

    .. list-table::
       :widths: 10 50
       :stub-columns: 1

       * - Type
         - minimization
       * - Range
         - :math:`x_i \in [-600, 600]`
       * - Global optima
         - :math:`x_i = 0, \\forall i \in \\lbrace 1 \\ldots N\\rbrace`, :math:`f(\mathbf{x}) = 0`
       * - Function
         - :math:`f(\\mathbf{x}) = \\frac{1}{4000}\\sum_{i=1}^N\,x_i^2 - \
                  \prod_{i=1}^N\\cos\\left(\\frac{x_i}{\sqrt{i}}\\right) + 1`

    .. plot:: code/benchmarks/griewank.py
       :width: 67 %
    """
    return 1.0 / 4000.0 * sum(x ** 2 for x in individual) - \
           reduce(mul, (cos(x / sqrt(i + 1.0)) for i, x in enumerate(individual)), 1) + 1


def main():
    for i in range(8):
        list =[]
        list.append('F8')
        for j in range(8):
            genome = G1DList.G1DList(size=10)
            genome.setParams(rangemin=-600, rangemax=600)
            genome.initializator.set(Initializators.G1DListInitializatorReal)
            genome.mutator.set(Mutators.G1DListMutatorRealGaussian)
            genome.evaluator.set(griewank)
            genome.crossover.set(Crossovers.G1DListCrossoverUniform)

            ga = GSimpleGA.GSimpleGA(genome, seed=64)
            ga.setMinimax(Consts.minimaxType["minimize"])
            ga.setGenerations(MAX_GEN)
            ga.setPopulationSize(POPULATION[i])
            ga.setCrossoverRate(CROSSOVER_PROB[j])
            ga.setMutationRate(MUTATION_PROB)

            ga.evolve(freq_stats=20)
            best = ga.bestIndividual()
            list.append(str(best.fitness))

        with open('HOF' + str(POPULATION[i]) + '.csv', mode='a') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,
                                    dialect='excel')

            csv_writer.writerow(list)


if __name__ == "__main__":
    main()
