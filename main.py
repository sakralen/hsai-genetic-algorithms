import random

from fileutils import parse_csv
from plotutils import plot_locations, plot_restored_route, show_plot
from routeutils import fix_route, restore_route

if __name__ == "__main__":
    locations = parse_csv('csv/eil76.csv')
    best_route = [int(item) - 1 for row in parse_csv(
        'csv/eil76-best-route.csv') for item in row]
    plot_locations(locations)
    plot_restored_route(best_route, locations)
    show_plot()

    # locations = parse_csv("csv/eil76.csv")[:10]
    # plot_locations(locations)
    # route = [random.randint(0, len(locations) - 1) for _ in range(len(locations))]
    # # route = [4, 2, 1, 0, 3]
    # print(route)
    # fix_route(route)
    # print(route)
    # plot_restored_route(restore_route(route), locations)
    # show_plot()
