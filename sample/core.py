from itertools import product, combinations_with_replacement
from Solver import Solver

COLUMNS = 4
COLOURS = set((1, 2, 3, 4, 5, 6))
COMBINATIONS = set(product(COLOURS, repeat=COLUMNS))
HINTS = set(combinations_with_replacement(set((0, 1, 2)), COLUMNS))
ANSWER = (1, 4, 5, 6)

solver = Solver(COLUMNS, COLOURS, COMBINATIONS, HINTS, ANSWER)

best_entropy = solver.get_best_first_guess()

full_stats = solver.analyze_average_guesses_for_first_guess(best_entropy)

ranking = solver.find_best_first_guess_by_average_guesses(max_secrets=None)
