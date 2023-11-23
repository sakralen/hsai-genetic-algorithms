import random
import math


def generate_neighbour_route(length):
    return to_neighbour_route(generate_restored_route(length))


def generate_restored_route(length):
    route = [i for i in range(1, length)]
    random.shuffle(route)
    route.insert(0, 0)
    route.append(0)
    return route


def to_neighbour_route(route):
    route_len = len(route)
    neighbour_route = [-1] * (route_len - 1)

    for i in range(route_len - 1):
        neighbour_route[route[i]] = route[i + 1]

    return neighbour_route


def restore_route(route):
    current_vertex = route[0]
    restored_route = [0, current_vertex]

    while current_vertex != 0:
        restored_route.append(route[current_vertex])
        current_vertex = route[current_vertex]

    return restored_route


# it is for neighbour routes!
def calc_route_length(route, locations):
    current_vertex = route[0]
    route_length = math.dist(locations[0], locations[current_vertex])

    while current_vertex != 0:
        route_length += math.dist(
            locations[current_vertex], locations[route[current_vertex]]
        )
        current_vertex = route[current_vertex]

    return route_length


def traverse(start, steps, route):
    current_vertex = start

    for _ in range(steps):
        current_vertex = route[current_vertex]

    return current_vertex
