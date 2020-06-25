import csv

from pyevolve import Consts
from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import Mutators, Initializators, Crossovers

POPULATION = [50, 100, 150, 200, 250, 300, 350, 400]
CROSSOVER_PROB = [0.6, 0.65, 0.70, 0.75, 0.80, 0.85, 0.9, 0.95]
MUTATION_PROB = 0.25
MAX_GEN = 100
cr_csv = ['', '0.6', '0.65', '0.7', '0.75', '0.8', '0.85', '0.9', '0.95']

def sphere(xlist):
    total = 0
    for i in xlist:
        total += i ** 2
    return total


def main():
    for i in range(8):
        list =[]
        list.append('F1')
        for j in range(8):
            genome = G1DList.G1DList(size=2)
            genome.setParams(rangemin=-5.12, rangemax=5.12)
            genome.initializator.set(Initializators.G1DListInitializatorReal)
            genome.mutator.set(Mutators.G1DListMutatorRealGaussian)
            genome.evaluator.set(sphere)
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
            csv_writer.writerow(cr_csv)
            csv_writer.writerow(list)




if __name__ == "__main__":
    main()
