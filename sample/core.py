from itertools import product
COLUMNS = 4
colours = set((1, 2, 3, 4, 5, 6))
combinations = set(product(colours, repeat = COLUMNS))