import sys
import time

from fileutils import parse_csv
from salesmangenetic import SalesmanGeneticAlgoritm


if __name__ == "__main__":
    population_size = int(sys.argv[1])
    genereation_max = int(sys.argv[2])
    crossover_prob = float(sys.argv[3])
    mutation_prob = float(sys.argv[4])

    locations = parse_csv('csv/eil76.csv')
    # optimal_route = [int(item) - 1 for row in parse_csv(
    #     'csv/eil76-best-route.csv') for item in row]

    start_time = time.time()

    SalesmanGeneticAlgoritm(locations, population_size,
                            genereation_max, crossover_prob, mutation_prob).execute()

    finish_time = time.time() - start_time
    print(f'elapsed time: {finish_time:0.2f}')
