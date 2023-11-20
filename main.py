import sys

from fileutils import parse_csv
from salesmangenetic import SalesmanGeneticAlgoritm

from plotutils import plot_locations, plot_restored_route, show_plot

if __name__ == "__main__":
    # locations = parse_csv('csv/eil76.csv')
    # best_route = [int(item) - 1 for row in parse_csv(
    #     'csv/eil76-best-route.csv') for item in row]
    # plot_locations(locations)
    # plot_restored_route(best_route, locations)
    # show_plot()

    population_size = int(sys.argv[1])
    genereation_max = int(sys.argv[2])
    crossover_prob = float(sys.argv[3])
    mutation_prob = float(sys.argv[4])

    locations = parse_csv('csv/eil76.csv')[:30]
    SalesmanGeneticAlgoritm(locations, population_size, genereation_max, crossover_prob, mutation_prob).execute()
