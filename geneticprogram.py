import random
import numpy as np
from tree import Tree


def given_function(x):
    return sum(x[i] ** (i - 1) for i in range(len(x)))


def mse(function, tree, points):
    with_function = [function(point) for point in points]
    with_tree = [tree.compute(point, tree) for point in points]

    return np.square(np.subtract(with_function, with_tree)).mean()


class GeneticProgram:
    def __init__(
        self,
        population_size,
        generation_max,
        crossover_prob,
        mutation_prob,
        max_height,
        points,
    ):
        self.population_size = population_size
        self.generation_max = generation_max
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob

        self.max_height = max_height
        self.points = points
        self.dim = len(points[0])

        self.population = self.generate_population()
        self.children = []

    def generate_population(self):
        population = []
        for _ in range(self.population_size):
            tree = Tree.generate(self.max_height, self.dim)
            while not tree.is_good(self.points):
                tree = Tree.generate(self.max_height, self.dim)
            population.append(tree)
        return population

    def execute(self):
        for i in range(self.generation_max):
            self.mutate()
            self.crossover()
            self.reproduce()

    def mutate(self):
        for tree in self.population:
            if random.random() < self.mutation_prob:
                pass

    def crossover(self):
        for i in range(self.population_size // 2):
            if random.random() < self.crossover_prob:
                pass

    def reproduce(self):
        self.population += self.children
        values = np.array(
            list(
                map(lambda tree: -self.target_func(tree, self.points), self.population)
            )
        )

        values -= min(values)
        values += 1

        sum = np.sum(values)
        values /= sum

        self.population = random.choices(
            self.population, values, k=self.population_size
        )

    def target_func(self, tree, data_range):
        return mse(given_function, tree, data_range)


points = [[x, 1] for x in np.arange(-1, 1.1, 0.1)]
gp = GeneticProgram(1, 1000, 0.35, 1, 4, points)

population = gp.population
for tree in population:
    tree.print()
    print("\n")
    print(tree.compute(points[0]))
