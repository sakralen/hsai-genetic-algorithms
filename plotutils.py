import matplotlib.pyplot as plt


def show_plot():
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()


def plot_locations(locations):
    for i, (x, y) in enumerate(locations):
        plt.scatter(x, y, color="blue")
        plt.text(x, y, f"{i}", ha="center", va="bottom")


def plot_restored_route(route, locations):
    for i in range(len(route) - 1):
        plot_line(locations[route[i]], locations[route[i + 1]])


def plot_line(source, dest):
    x_values, y_values = zip(source, dest)
    plt.plot(x_values, y_values, color="r")
