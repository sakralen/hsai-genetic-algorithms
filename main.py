import numpy as np
from geneticprogram import GeneticProgram

points = [[x, 1] for x in np.arange(-1, 1.1, 0.1)]
GeneticProgram(10, 100, 0.35, 0.1, 5, points).execute()
