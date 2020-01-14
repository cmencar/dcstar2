import csv

from pyevolve import G1DList, GSimpleGA, Crossovers
from pyevolve import Initializators, Mutators, Consts

POPULATION = [50, 100, 150, 200, 250, 300, 350, 400]
CROSSOVER_PROB = [0.6, 0.65, 0.70, 0.75, 0.80, 0.85, 0.9, 0.95]
MUTATION_PROB = 0.01
MAX_GEN = 100


def rosenbrock(xlist):
    sum_var = 0
    for x in xrange(1, len(xlist)):
        sum_var += 100.0 * (xlist[x] - xlist[x - 1] ** 2) ** 2 + (1 - xlist[x - 1]) ** 2
    return sum_var


def main():
        for i in range(8):
            list = []
            list.append('F2')
            for j in range(8):
                genome = G1DList.G1DList()
                genome.setParams(rangemin=-2.048, rangemax=2.048)
                genome.initializator.set(Initializators.G1DListInitializatorReal)
                genome.mutator.set(Mutators.G1DListMutatorRealGaussian)
                genome.evaluator.set(rosenbrock)
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
