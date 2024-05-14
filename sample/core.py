from itertools import product, combinations_with_replacement
from Solver import Solver

COLUMNS = 4
COLOURS = set((1, 2, 3, 4, 5, 6))
COMBINATIONS = set(product(COLOURS, repeat = COLUMNS))
HINTS = set(combinations_with_replacement(set((0, 1, 2)), COLUMNS))

solver = Solver(COLUMNS, COLOURS, COMBINATIONS, HINTS)
solver.find_best_combo()