import os
import random
import numpy as np

from routeutils import generate_neighbour_route, calc_route_length, restore_route, fix_route
from plotutils import prep_plot, plot_locations, plot_restored_route, save_plot, clear_plot


class SalesmanGeneticAlgoritm:
    def __init__(self, locations, population_size, generation_max, crossover_prob, mutation_prob):
        self.locations = locations
        self.population_size = population_size
        self.generation_max = generation_max
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob
        self.cities_cnt = len(locations)

        self.population = [generate_neighbour_route(
            self.cities_cnt) for _ in range(self.population_size)]

    def execute(self):
        for i in range(0, self.generation_max):
            self.mutate()
            self.crossover()
            self.reproduce()

            best_route = min(self.population, key=self.target_func)
            print(f'{i}: {self.target_func(best_route):0.0f}')

            if (i == 0) or (i == self.generation_max - 1):
                prep_plot(i + 1, self.target_func(best_route))
                plot_locations(self.locations)
                plot_restored_route(restore_route(best_route), self.locations)
                save_plot(self.population_size, self.generation_max,
                          self.crossover_prob, self.mutation_prob, i + 1)
                clear_plot()

    # swaps two inner vertices in a random subroute of length 4
    def mutate(self):
        for route in self.population:
            if random.random() < self.mutation_prob:
                b = random.randint(0, self.cities_cnt - 1)
                c = route[b]
                d = route[c]
                a = route.index(b)

                route[a] = c
                route[c] = b
                route[b] = d

    def crossover(self):
        for i in range(0, self.population_size // 2):
            if random.random() < self.crossover_prob:
                route_a = self.population[2 * i]
                route_b = self.population[2 * i + 1]
                crossover_point = random.randint(1, self.cities_cnt - 2)

                self.population[2 * i] = route_a[:crossover_point] + \
                    route_b[crossover_point:]
                self.population[2 * i + 1] = route_b[:crossover_point] + \
                    route_a[crossover_point:]

                fix_route(self.population[2 * i])
                fix_route(self.population[2 * i + 1])

    def reproduce(self):
        values = np.array(
            list(map(lambda r: -self.target_func(r), self.population)))

        values -= min(values)
        values += 1

        sum = np.sum(values)
        values /= sum

        self.population = random.choices(
            self.population, values, k=self.population_size)

    def target_func(self, route):
        return calc_route_length(route, self.locations)
