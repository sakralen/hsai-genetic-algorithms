import random
import numpy as np
import math

from routeutils import (
    generate_neighbour_route,
    calc_route_length,
    restore_route,
    traverse,
)
from plotutils import (
    prep_plot,
    plot_locations,
    plot_restored_route,
    save_plot,
    clear_plot,
)


class SalesmanGeneticAlgoritm:
    def __init__(
        self, locations, population_size, generation_max, crossover_prob, mutation_prob
    ):
        self.locations = locations
        self.population_size = population_size
        self.generation_max = generation_max
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob
        self.cities_cnt = len(locations)

        self.population = [
            generate_neighbour_route(self.cities_cnt)
            for _ in range(self.population_size)
        ]

    def execute(self):
        best_overall = {"route": None, "length": float("inf"), "generation": 0}
        for i in range(0, self.generation_max):
            self.mutate()
            children = self.crossover()
            self.reproduce(children)

            best_route = min(self.population, key=self.target_func)
            best_length = self.target_func(best_route)
            print(f"{i}: {best_length:0.0f}")

            if best_length < best_overall["length"]:
                best_overall["route"] = best_route
                best_overall["length"] = best_length
                best_overall["generation"] = i

        prep_plot(best_overall["generation"], best_overall["length"])
        plot_locations(self.locations)
        plot_restored_route(restore_route(best_overall["route"]), self.locations)
        save_plot(
            self.population_size,
            self.generation_max,
            self.crossover_prob,
            self.mutation_prob,
            best_overall["generation"],
        )
        clear_plot()

    # swaps two vertices
    def mutate(self):
        for route in self.population:
            if random.random() < self.mutation_prob:
                max_distance = self.cities_cnt // 10
                a = random.randint(0, self.cities_cnt - 1)
                b = traverse(a, random.randint(1, max_distance), route)
                while a == b:
                    b = traverse(a, random.randint(1, max_distance), route)

                if route[b] == a:
                    a, b = b, a

                a_parent = route.index(a)
                a_child = route[a]
                b_parent = route.index(b)
                b_child = route[b]

                if route[a] == b:
                    route[a_parent] = b
                    route[a] = b_child
                    route[b] = a
                else:
                    route[a] = b_child
                    route[b_parent] = a
                    route[b] = a_child
                    route[a_parent] = b

    # heuristic crossover
    def crossover(self):
        children = []
        for i in range(0, self.population_size // 2):
            if random.random() < self.crossover_prob:
                route_a = self.population[2 * i]
                route_b = self.population[2 * i + 1]

                new_route = [-1] * self.cities_cnt
                not_visited = [i for i in range(self.cities_cnt)]
                first = random.randint(0, self.cities_cnt - 1)
                not_visited.pop(first)

                current = first
                while len(not_visited) != 0:
                    a_dist = math.dist(
                        self.locations[current], self.locations[route_a[current]]
                    )
                    b_dist = math.dist(
                        self.locations[current], self.locations[route_b[current]]
                    )

                    next = route_a[current] if a_dist < b_dist else route_b[current]

                    if next in not_visited:
                        new_route[current] = next
                        not_visited.pop(not_visited.index(next))
                    else:
                        new_route[current] = not_visited.pop(
                            random.randint(0, len(not_visited) - 1)
                        )

                    current = new_route[current]

                new_route[current] = first
                children.append(new_route)
        return children

    def reproduce(self, children):
        self.population += children
        values = np.array(list(map(lambda r: -self.target_func(r), self.population)))

        values -= min(values)
        values += 1

        sum = np.sum(values)
        values /= sum

        self.population = random.choices(
            self.population, values, k=self.population_size
        )

    def target_func(self, route):
        return calc_route_length(route, self.locations)
