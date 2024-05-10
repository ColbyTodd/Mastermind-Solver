from itertools import product, combinations_with_replacement

COLUMNS = 4
HINTS = set(combinations_with_replacement(set((0, 1, 2)), COLUMNS))
COLOURS = set((1, 2, 3, 4, 5, 6))
COMBINATIONS = set(product(COLOURS, repeat = COLUMNS))

# for combo in COMBINATIONS:
#     calculate_expected_information(combo, COMBINATIONS)