import numpy as np
from geneticprogram import GeneticProgram

if __name__ == "__main__":
    points = [[x, 1] for x in np.arange(-1, 1.1, 0.1)]
    GeneticProgram(1000, 1000, 1, 0, 2, points).execute()
