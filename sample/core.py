from itertools import product, combinations_with_replacement
COLUMNS = 4
HINTS = set(combinations_with_replacement(set((0, 1, 2)), COLUMNS))
COLOURS = set((1, 2, 3, 4, 5, 6))
COMBINATIONS = set(product(COLOURS, repeat = COLUMNS))

def calculate_expected_information(combo: tuple, combinations: set):
    """Calculates the expected amount of information gained from a 
    given guess.""" 

    for hint in HINTS:
        calculate_information(combo, hint, combinations)

    # calculate_information(combo, [0, 0, 0, 0], combinations)

def calculate_information(combo: tuple, hint: tuple, combinations: set):
    """Calculates the information gained from a guess with a specific
    hint."""
    calculate_possible_combinations(combo, hint, combinations)

def calculate_possible_combinations(combo: tuple, hint: tuple, combinations: set):
    """Calculate combinations that are still possible."""
    combinations_remaining = set()
    
    # No colours are correct
    if 1 not in hint and 2 not in hint:
        for combination in combinations:
            if len(set(combo).intersection(combination)) == 0:
                combinations_remaining.add(combination)

    # No colours are in the correct spot
    elif 2 not in hint:
        return
    # Colours are only in the correct spot
    elif 1 not in hint:
        return
    # Some colours are in the correct spot
    else:
        return

    return combinations_remaining


for combo in COMBINATIONS:
    calculate_expected_information(combo, COMBINATIONS)

# calculate_expected_information((1, 2, 3, 4), COMBINATIONS)