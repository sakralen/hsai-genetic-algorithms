import sys
import os
import random
import math
import numpy as np
from itertools import product
import matplotlib.pyplot as plt

PATH = os.path.join(os.path.dirname(__file__), 'output/')

if not os.path.exists(PATH):
    os.makedirs(PATH)

X_LOW = -500
X_HIGH = 500
STEP = 25
DIM = 2

DELTA = 0.1


def target_func(x):
    return sum(x[i] ** 2 / 4000 for i in range(0, DIM)) - math.prod(np.cos(x[i] / np.sqrt(i + 1)) for i in range(0, DIM)) + 1


class MultiDimGenAlg:
    def __init__(self, population_size, genereation_cnt, crossover_prob, mutation_prob):
        self.population_size = population_size
        self.generation_cnt = genereation_cnt
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob

        self.chromosome_len = DIM
        self.population = [[random.uniform(X_LOW, X_HIGH)
                            for _ in range(DIM)] for _ in range(self.population_size)]

    def reproduce(self):
        values = np.array(
            list(map(lambda l: -target_func(l), self.population)))

        values -= min(values)
        values += 1

        sum = np.sum(values)
        values /= sum

        self.population = random.choices(
            self.population, values, k=self.population_size)

    def crossover(self):
        for i in range(0, self.population_size // 2):
            if random.random() < self.crossover_prob:
                chromosomeA = []
                chromosomeB = []
                for j in range(0, self.chromosome_len):
                    chromosomeA.append(self.crossover_prob * self.population[2 * i][j] \
                           + (1 - self.crossover_prob) * self.population[2 * i + 1][j])
                    chromosomeB.append(self.crossover_prob * self.population[2 * i + 1][j] \
                           + (1 - self.crossover_prob) * self.population[2 * i][j])
                self.population[2 * i] = chromosomeA
                self.population[2 * i + 1] = chromosomeB

    def mutate(self):
        for i in range(self.population_size):
            if random.random() < self.mutation_prob:
                self.population[i] = [random.uniform(X_LOW, X_HIGH)
                                 for _ in range(self.chromosome_len)]

    def plot(self, generation):
        values = np.arange(X_LOW, X_HIGH + STEP, STEP)
        xy = [list(pair) for pair in list(product(values,  values))]

        X = [pair[0] for pair in xy]
        Y = [pair[1] for pair in xy]
        Z = list(map(lambda l: target_func(l), xy))

        x_popul = [pair[0] for pair in self.population]
        y_popul = [pair[1] for pair in self.population]
        z_popul = list(map(lambda l: target_func(l), self.population))

        ax = plt.axes(projection='3d')
        ax.view_init(elev=55., azim=-25.)
        ax.scatter3D(X, Y, Z, marker='^', c=Z)
        ax.scatter3D(x_popul, y_popul, z_popul, marker='o', c='r', s=50)
        
        plt.savefig(
            PATH + f'{self.population_size}_{self.generation_cnt}_{self.crossover_prob}_{self.mutation_prob}_{generation}.png')
        # plt.show()
        plt.clf()

    def execute(self):
        for i in range(0, self.generation_cnt):
            self.mutate()
            self.crossover()
            self.reproduce()

            # x = list(map(lambda l:
            #              self.phenotype_func(l), self.population))
            # y = list(map(lambda l: target_func(
            #     self.phenotype_func(l)), self.population))
            # pairs = dict(zip(y, x))

            # y_std = np.std(y)
            # x_std = np.std(x)
            # y_max = np.max(y)
            # x_max = pairs.get(y_max)

            # print(
            #     f'Поколение: {i + 1:3} | Максимум: ({x_max:5.3f}; {y_max:5.3f}) | Дисперия X: {x_std:5.3f} | Дисперия Y: {y_std:5.3f}')

            self.plot(i + 1)

            # if (x_std < DELTA and y_std < DELTA):
            #     break

    def print_pop(self):
        print(self.population)


if __name__ == '__main__':
    # population_size = int(sys.argv[1])
    # genereation_cnt = int(sys.argv[2])
    # crossover_prob = float(sys.argv[3])
    # mutation_prob = float(sys.argv[4])

    mdga = MultiDimGenAlg(50, 20, 0.5, 0.01)
    mdga.execute()
    print('finished')
