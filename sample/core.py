from itertools import product, combinations_with_replacement
from Solver import Solver

COLUMNS = 4
COLOURS = set((1, 2, 3, 4, 5, 6))
COMBINATIONS = set(product(COLOURS, repeat = COLUMNS))
HINTS = set(combinations_with_replacement(set((0, 1, 2)), COLUMNS))
ANSWER = (1, 2, 5, 6)

solver = Solver(COLUMNS, COLOURS, COMBINATIONS, HINTS, ANSWER)
print(solver.calculate_number_of_guesses(COMBINATIONS))