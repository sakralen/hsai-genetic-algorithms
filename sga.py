import sys
import os
import math
import random
import numpy as np
import matplotlib.pyplot as plt

PATH = os.path.join(os.path.dirname(__file__), 'output/')

if not os.path.exists(PATH):
    os.makedirs(PATH)

X_LOW = -10.
X_HIGH = 10.
STEP = 0.1

DELTA = 0.1
CHROMOSOME_LEN = 15


def target_func(x):
    if (x >= -0.3 and x <= 0.3):
        return 0
    return math.cos(3 * x - 15) / math.fabs(x)


class SimpleGeneticAlgorithm:
    def __init__(self, population_size, genereation_cnt, crossover_prob, mutation_prob):
        self.population_size = population_size
        self.generation_cnt = genereation_cnt
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob

        self.chromosome_len = CHROMOSOME_LEN
        self.alleles = ['0', '1']
        self.population = [''.join(random.choice(self.alleles) for _ in range(
            self.chromosome_len)) for _ in range(self.population_size)]

    def phenotype_func(self, chromosome):
        return (X_LOW + (int(chromosome, 2) * (X_HIGH - X_LOW) / (2 ** self.chromosome_len - 1)))

    def reproduce(self):
        values = np.array(
            list(map(lambda l: target_func(self.phenotype_func(l)), self.population)))

        values -= min(values)
        values += 1

        sum = np.sum(values)
        values /= sum

        self.population = random.choices(
            self.population, values, k=self.population_size)

    def crossover(self):
        for i in range(0, self.population_size // 2):
            if random.random() < self.crossover_prob:
                chromosome_a = self.population[2 * i]
                chromosome_b = self.population[2 * i + 1]
                crossover_point = random.randint(1, self.chromosome_len - 2)

                self.population[2 * i] = chromosome_a[:crossover_point] + \
                    chromosome_b[crossover_point:]
                self.population[2 * i + 1] = chromosome_b[:crossover_point] + \
                    chromosome_a[crossover_point:]

    def mutate(self):
        for i in range(self.population_size):
            if random.random() < self.mutation_prob:
                chromosome = self.population[i]
                gene_to_flip = random.randint(0, self.chromosome_len - 1)

                mutated_chromosome = list(chromosome)
                mutated_chromosome[gene_to_flip] = '1' if chromosome[gene_to_flip] == '0' else '0'

                self.population[i] = ''.join(mutated_chromosome)

    def plot(self, generation):
        x_target = np.arange(X_LOW, X_HIGH, STEP)
        y_target = list(map(lambda l: target_func(l), x_target))

        x_population = list(map(lambda l:
                                self.phenotype_func(l), self.population))
        y_population = list(map(lambda l: target_func(
            self.phenotype_func(l)), self.population))

        plt.xlabel('x')
        plt.ylabel('y')
        plt.title(f'Generation № {generation}')

        plt.plot(x_target, y_target, 'r')
        plt.scatter(x_population, y_population)

        plt.savefig(
            PATH + f'{self.population_size}_{self.generation_cnt}_{self.crossover_prob}_{self.mutation_prob}_{generation}.png')
        plt.clf()

    def execute(self):
        for i in range(0, self.generation_cnt):
            self.mutate()
            self.crossover()
            self.reproduce()

            x = list(map(lambda l:
                         self.phenotype_func(l), self.population))
            y = list(map(lambda l: target_func(
                self.phenotype_func(l)), self.population))
            pairs = dict(zip(y, x))

            y_std = np.std(y)
            x_std = np.std(x)
            y_max = np.max(y)
            x_max = pairs.get(y_max)

            print(
                f'Поколение: {i + 1:3} | Максимум: ({x_max:5.3f}; {y_max:5.3f}) | Дисперия X: {x_std:5.3f} | Дисперия Y: {y_std:5.3f}')

            self.plot(i + 1)

            if (x_std < DELTA and y_std < DELTA):
                break


if __name__ == '__main__':
    population_size = int(sys.argv[1])
    genereation_cnt = int(sys.argv[2])
    crossover_prob = float(sys.argv[3])
    mutation_prob = float(sys.argv[4])

    sga = SimpleGeneticAlgorithm(
        population_size, genereation_cnt, crossover_prob, mutation_prob)
    sga.execute()
