import numpy as np
import random

np.seterr(all="raise")


class Tree:
    UNARY = "unary"
    BINARY = "binary"
    ARG = "arg"

    terminals = [UNARY, BINARY, ARG]
    weights = {UNARY: 0.33, BINARY: 0.33, ARG: 0.33}

    # commented out functions cause cancer. my visit to oncologist was yesterday. bye.
    functions = {
        UNARY: [np.fabs, np.sin, np.cos],  # , np.exp],
        BINARY: [np.add, np.subtract, np.multiply],  # , np.true_divide, np.power],
        ARG: [],
    }

    productions = {
        UNARY: [[UNARY, BINARY, ARG]],
        BINARY: [[UNARY, BINARY, ARG], [UNARY, BINARY, ARG]],
        ARG: [],
    }

    class Node:
        def __init__(self, type, parent=None):
            self.type = type
            self.parent = parent
            self.children = []

        def __str__(self):
            return self.type

        def set_parent(self, parent):
            self.parent = parent

    class FunctionNode(Node):
        def __init__(self, type, function=None, parent=None):
            super().__init__(type, parent)
            self.function = function

        def __str__(self):
            return super().__str__() + " " + self.function.__name__

        def add_child(self, child):
            self.children.append(child)

    class ArgNode(Node):
        def __init__(self, i=0, parent=None):
            super().__init__(Tree.ARG, parent)
            self.i = i

        def __str__(self):
            return super().__str__() + "_" + str(self.i)

    class Generator:
        def __init__(self, max_height, dim=2, starting_height=1):
            self.max_height = max_height
            self.dim = dim
            self.height = starting_height

        def generate(self):
            root = self.make_random_node()
            queue = [root]

            while len(queue) > 0:
                # looping through nodes on the same level:
                for _ in range(len(queue)):
                    current = queue.pop(0)
                    # generating children of current:
                    for _ in Tree.productions[current.type]:
                        child = None
                        if self.height < self.max_height - 2:
                            child = self.make_random_node(current)
                            queue.append(child)
                        else:
                            child = Tree.ArgNode(
                                random.randint(0, self.dim - 1), current
                            )
                        current.add_child(child)
                self.height += 1

            return Tree(root)

        def make_random_node(self, parent=None):
            type = self.choose_rand_terminal()

            if type == Tree.ARG:
                return Tree.ArgNode(random.randint(0, self.dim - 1), parent)

            function = random.choice(Tree.functions[type])
            return Tree.FunctionNode(type, function, parent)

        @staticmethod
        def choose_rand_terminal():
            weights = Tree.weights.values()
            return random.choices(Tree.terminals, weights=weights, k=1)[0]

    def __init__(self, root):
        self.root = root

    @staticmethod
    def generate(max_height, dim=2, starting_height=1):
        return Tree.Generator(max_height, dim, starting_height).generate()

    def get_height(self):
        return Tree.get_subtree_height(self.root)

    @staticmethod
    def get_subtree_height(from_node):
        def calc_height(node):
            if len(node.children) == 0:
                return 1
            return 1 + max(calc_height(child) for child in node.children)

        return calc_height(from_node)

    def print(self):
        def print_node(node, height):
            print("    " * (height - 1) + str(height) + ": " + node.__str__())

            for child in node.children:
                print_node(child, height + 1)

        print_node(self.root, 1)

    # without true_divide(), pow() and exp() there is no exception:
    def compute(self, point):
        def compute_node(node, point):
            if node.type == Tree.ARG:
                return point[node.i]
            return node.function(
                *[compute_node(child, point) for child in node.children]
            )

        try:
            return compute_node(self.root, point)
        except FloatingPointError:
            return None

    # # without true_divide(), pow() and exp() this is not needed:
    # def is_good(self, points):
    #     for point in points:
    #         if self.compute(point) is None:
    #             return False
    #     return True

    def get_nodes(self):
        queue = [self.root]
        height = 1
        nodes = {self.root: height}

        while len(queue) > 0:
            for _ in range(len(queue)):
                current = queue.pop(0)
                for child in current.children:
                    queue.append(child)
                    nodes[child] = height + 1
            height += 1

        return nodes
