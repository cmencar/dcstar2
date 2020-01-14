import array
import csv
import pickle
import random

import numpy
from deap import base, algorithms
from deap import benchmarks
from deap import creator
from deap import tools

# Problem dimension
NDIM = 10

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", array.array, typecode='f', fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attr_float", random.uniform, -2.048, 2.048)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, NDIM)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("mutate", tools.mutGaussian, mu=0.1, sigma=1, indpb=0.05)
toolbox.register("mate", tools.cxUniform, indpb=0.6)
toolbox.register("select", tools.selTournament, tournsize=20)
toolbox.register("evaluate", benchmarks.rosenbrock)


def evalue(i):
    j = 0
    test = []
    test.append('F2')
    NGEN = 100
    CR = [0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
    while j in range(8):
        pop = toolbox.population(n=i)
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", numpy.mean)
        stats.register("std", numpy.std)
        stats.register("min", numpy.min)
        stats.register("max", numpy.max)
        algorithms.eaSimple(pop, toolbox, cxpb=CR[j], mutpb=0.05, ngen=NGEN, stats=stats,
                                         halloffame=hof)
        fits = [ind.fitness.values[0] for ind in pop]
        test.append(str(max(fits)))
        j = j + 1
    return test


def main():
    # Differential evolution parameters
    test = []
    MU = [50, 100, 150, 200, 250, 300, 350, 400]

    for i in range(8):
        test = evalue(MU[i])
        with open('HOF' + str(MU[i]) + '.csv', mode='a') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, dialect='excel')

            csv_writer.writerow(test)


"""
 logbook = tools.Logbook()
    logbook.header = "gen", "evals", "std", "min", "avg", "max"

    # Evaluate the individuals
    fitnesses = toolbox.map(toolbox.evaluate, pop)
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    record = stats.compile(pop)
    logbook.record(gen=0, evals=len(pop), **record)
    print(logbook.stream)

    for g in range(1, NGEN):
        for k, agent in enumerate(pop):
            a, b, c = toolbox.select(pop)
            y = toolbox.clone(agent)
            index = random.randrange(NDIM)
            for i, value in enumerate(agent):
                if i == index or random.random() < CR:
                    y[i] = a[i] + F * (b[i] - c[i])
            y.fitness.values = toolbox.evaluate(y)
            if y.fitness > agent.fitness:
                pop[k] = y
        hof.update(pop)
        record = stats.compile(pop)
        logbook.record(gen=g, evals=len(pop), **record)
        print(logbook.stream)

    print("Best individual is ", hof[0], hof[0].fitness.values[0])

"""

if __name__ == "__main__":
    main()
