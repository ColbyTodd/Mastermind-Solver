from itertools import product, combinations_with_replacement
from Solver import Solver

COLUMNS = 4
COLOURS = set((1, 2, 3, 4))
COMBINATIONS = set(product(COLOURS, repeat = COLUMNS))
HINTS = set(combinations_with_replacement(set((0, 1, 2)), COLUMNS))

solver = Solver(COLUMNS, COLOURS, COMBINATIONS, HINTS)
print(solver.calculate_number_of_guesses((1,1,1,1), (1, 1, 2, 2), COMBINATIONS))