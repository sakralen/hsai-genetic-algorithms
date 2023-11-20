import matplotlib.pyplot as plt

from routeutils import restore_route


def show_plot():
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()


def plot_locations(locations):
    for i, (x, y) in enumerate(locations):
        plt.scatter(x, y, color="blue")
        plt.text(x, y, f"{i}", ha="center", va="bottom")


def restore_and_plot_route(route, locations):
    restored_route = restore_route(route)

    for i in range(len(restored_route) - 1):
        plot_line(locations[restored_route[i]], locations[restored_route[i + 1]])


def plot_line(source, dest):
    x_values, y_values = zip(source, dest)
    plt.plot(x_values, y_values, color="r")
