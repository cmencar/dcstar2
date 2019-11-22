import csv
from random import Random
from time import time

import inspyred

pop = [50, 100, 150, 200, 250, 300, 350, 400]
crossover = [0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
mut = 0.25
cr_csv = ['', '0.6', '0.65', '0.7', '0.75', '0.8', '0.85', '0.9', '0.95']

def main(prng=None, display=False):
    if prng is None:
        prng = Random()
        prng.seed(time())

    problem = inspyred.benchmarks.Sphere(2)
    ea = inspyred.ec.GA(prng)
    ea.terminator = inspyred.ec.terminators.evaluation_termination
    for i in range(8):
        list = []
        list.append('F1')
        for j in range(8):
            final_pop = ea.evolve(evaluator=problem.evaluator,
                                  pop_size=pop[i],
                                  crossover_rate=crossover[j],
                                  mutation_rate=mut,
                                  generator=problem.generator,
                                  maximize=problem.maximize,
                                  bounder=problem.bounder,
                                  max_evaluations=30000)

            if display:
                best = max(final_pop)
                print(len(final_pop))
                print('Best Solution: \n{0}'.format(str(best)))
                list.append(str(best.fitness))
        with open('HOF' + str(pop[i]) + '.csv', mode='a') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, dialect='excel')
            csv_writer.writerow(cr_csv)
            csv_writer.writerow(list)
    return ea


if __name__ == '__main__':
    main(display=True)
