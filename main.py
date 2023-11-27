import numpy as np
from geneticprogram import GeneticProgram

if __name__ == "__main__":
    points = [[x, x] for x in np.arange(-1, 1.1, 0.01)]
    GeneticProgram(10, 1000, 0.25, 0.01, 6, points).execute()
