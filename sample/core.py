from itertools import product, combinations_with_replacement
from Calculator import Calculator

COLUMNS = 4
HINTS = set(combinations_with_replacement(set((0, 1, 2)), COLUMNS))
COLOURS = set((1, 2, 3, 4, 5, 6))
COMBINATIONS = set(product(COLOURS, repeat = COLUMNS))

calculator = Calculator()
best_combo = ()
max_expected_information = 0

for combo in COMBINATIONS:
    expected_information = calculator.calculate_expected_information(combo, COMBINATIONS, HINTS)
    
    if expected_information > max_expected_information:
        best_combo = combo
        max_expected_information = expected_information

print("Best combo = " + str(combo) + "\n Expected information = " + str(max_expected_information))