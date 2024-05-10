from itertools import product, combinations_with_replacement
from Calculator import Calculator

COLUMNS = 4
HINTS = set(combinations_with_replacement(set((0, 1, 2)), COLUMNS))
COLOURS = set((1, 2, 3, 4, 5, 6))
COMBINATIONS = set(product(COLOURS, repeat = COLUMNS))

calculator = Calculator()

for combo in COMBINATIONS:
    calculator.calculate_expected_information(combo, COMBINATIONS)