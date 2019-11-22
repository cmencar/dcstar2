import csv

from pyevolve import G1DList, GSimpleGA, Crossovers, Scaling
from pyevolve import Initializators, Mutators, Consts

POPULATION = [50, 100, 150, 200, 250, 300, 350, 400]
CROSSOVER_PROB = [0.6, 0.65, 0.70, 0.75, 0.80, 0.85, 0.9, 0.95]
MUTATION_PROB = 0.01
MAX_GEN = 100


def ste_f(xlist):
    sum_var = 0
    for x in xrange(1, len(xlist)):
        sum_var += int(xlist[x])
    return sum_var


def main():
    for i in range(8):
        list =[]
        list.append('F3')
        for j in range(8):
            genome = G1DList.G1DList(size=5)
            genome.setParams(rangemin=-5.12, rangemax=5.12)
            genome.initializator.set(Initializators.G1DListInitializatorReal)
            genome.mutator.set(Mutators.G1DListMutatorRealGaussian)
            genome.evaluator.set(ste_f)
            genome.crossover.set(Crossovers.G1DListCrossoverUniform)

            ga = GSimpleGA.GSimpleGA(genome, seed=64)
            ga.setMinimax(Consts.minimaxType["minimize"])
            ga.setGenerations(MAX_GEN)
            ga.setCrossoverRate(CROSSOVER_PROB[j])
            ga.setPopulationSize(POPULATION[i])
            ga.setMutationRate(MUTATION_PROB)
            pop = ga.getPopulation()
            pop.scaleMethod.set(Scaling.SigmaTruncScaling)
            ga.evolve(freq_stats=20)
            best = ga.bestIndividual()
            list.append(str(best.fitness))

        with open('HOF' + str(POPULATION[i]) + '.csv', mode='a') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,
                                    dialect='excel')

            csv_writer.writerow(list)

if __name__ == "__main__":
    main()
