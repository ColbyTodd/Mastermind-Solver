from itertools import product, combinations_with_replacement
from Calculator import Calculator

COLUMNS = 4
HINTS = set(combinations_with_replacement(set((0, 1, 2)), COLUMNS))
COLOURS = set((1, 2, 3, 4, 5, 6))
COMBINATIONS = set(product(COLOURS, repeat = COLUMNS))

def find_best_combo():
    calculator = Calculator()
    colours = set()
    for i in range (1, COLUMNS + 1):
        colours.add(i)
    combinations = set(product(colours, repeat = COLUMNS))
    best_combo = ()
    max_expected_information = 0

    for combo in combinations:
        expected_information = calculator.calculate_expected_information(combo, COMBINATIONS, HINTS)
        
        if expected_information > max_expected_information:
            best_combo = combo
            max_expected_information = expected_information

    print("Best combo = " + str(best_combo) + "\nExpected information = " + str(max_expected_information))

find_best_combo()