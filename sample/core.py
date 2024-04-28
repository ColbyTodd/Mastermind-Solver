from itertools import product, combinations_with_replacement
COLUMNS = 4
HINTS = set(combinations_with_replacement(set((0, 1, 2)), COLUMNS))
COLOURS = set((1, 2, 3, 4, 5, 6))
COMBINATIONS = set(product(COLOURS, repeat = COLUMNS))

def calculate_expected_information(combo: tuple):
    """Calculates the expected amount of information gained from a 
    given guess.""" 

    for hint in HINTS:
        calculate_information(combo, hint)

def calculate_information(combo: tuple, hint: tuple):
    """Calculates the information gained from a guess with a specific
    hint."""
    calculate_possible_combinations(combo, hint)

def calculate_possible_combinations(combo: tuple, hint: tuple):
    """Calculate combinations that are still possible."""

for combo in COMBINATIONS:
    calculate_expected_information(combo)