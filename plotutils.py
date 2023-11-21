import os
import matplotlib.pyplot as plt


DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'output/')


def save_plot(population_size, generation_max, crossover_prob, mutation_prob, generation, path=DEFAULT_PATH):
    if not os.path.exists(path):
        os.makedirs(path)

    plt.savefig(
        path + f'{population_size}_{generation_max}_{crossover_prob}_{mutation_prob}_{generation}.png')


def prep_plot(generation, route_length=0):
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(f'Generation № {generation}, best length: {route_length:0.0f}')


def show_plot():
    plt.show()


def clear_plot():
    plt.clf()


def plot_locations(locations):
    for i, (x, y) in enumerate(locations):
        plt.scatter(x, y, color="C0")
        plt.text(x, y, f"{i}", ha="center", va="bottom")


def plot_restored_route(route, locations):
    for i in range(len(route) - 1):
        plot_line(locations[route[i]], locations[route[i + 1]])


def plot_line(source, dest):
    x_values, y_values = zip(source, dest)
    plt.plot(x_values, y_values, color="C0")
