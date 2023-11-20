# fix_route, clean_route, concat_subroutes are for neighbour routes!

import random


def fix_route(route):
    clean_route(route)
    break_cycles(route)
    concat_subroutes(route)


def clean_route(route):
    route_len = len(route)

    for i in range(route_len):
        # breaking self-cycles:
        if route[i] == i:
            route[i] = -1

        # finding src vertices where dst is i:
        parents = [j for j in range(route_len) if route[j] == i]

        if len(parents) < 2:
            continue

        # leaving only one parent:
        parents.pop(0)
        for parent in parents:
            route[parent] = -1


def break_cycles(route):
    route_len = len(route)
    queue = [i for i in range(route_len)]

    # queue contains potential cycle's starting vertices,
    # all vertices are gone => all cycles are gone:
    while len(queue) != 0:
        first = queue.pop(0)
        last = route[first]
        if last == -1:
            continue

        # traversing to this cycle's ending vertex
        # and popping all vertices in it from the queue
        # (if cycle: cycle's starting vertex has already left the queue
        # => while loop stops when it is reached;
        # if not: last will be -1 assuming route is clean):
        while last in queue:
            queue.pop(queue.index(last))
            last = route[last]

        # if cycle, then break:
        if first == last:
            route[last] = -1


def find_parentless(route):
    route_len = len(route)
    parentless = []

    for i in range(route_len):
        parents = [j for j in range(route_len) if route[j] == i]
        if len(parents) == 0:
            parentless.append(i)

    return parentless


def concat_subroutes(route):
    parentless = find_parentless(route)
    subroutes = []

    # finding subroutes to avoid creating cycles if concatenating blindly:
    for first in parentless:
        last = first
        while route[last] != -1:
            last = route[last]
        subroutes.append([first, last])
    subroutes_len = len(subroutes)

    # concatenating:
    for i in range(subroutes_len - 1):
        current_last = subroutes[i][1]
        next_first = subroutes[i + 1][0]

        route[current_last] = next_first

    # closing route:
    first = subroutes[0][0]
    last = subroutes[subroutes_len - 1][1]
    route[last] = first


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
