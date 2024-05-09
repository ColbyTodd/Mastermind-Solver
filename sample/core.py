from itertools import product, combinations_with_replacement
from collections import Counter

COLUMNS = 4
HINTS = set(combinations_with_replacement(set((0, 1, 2)), COLUMNS))
COLOURS = set((1, 2, 3, 4, 5, 6))
COMBINATIONS = set(product(COLOURS, repeat = COLUMNS))

def calculate_expected_information(combo: tuple, combinations: set):
    """Calculates the expected amount of information gained from a 
    given guess.""" 

    # for hint in HINTS:
    #     calculate_information(combo, hint, combinations)

    calculate_information(combo, [2, 2, 0, 0], combinations)

def calculate_information(combo: tuple, hint: tuple, combinations: set):
    """Calculates the information gained from a guess with a specific
    hint."""
    calculate_possible_combinations(combo, hint, combinations)

def calculate_possible_combinations(combo: tuple, hint: tuple, 
                                        combinations: set):
    """Calculate combinations that are still possible."""
    combinations_remaining = set()
    colours_wrong_spot = hint.count(1)
    colours_correct_spot = hint.count(2)
    
    # No colours are correct
    if not colours_wrong_spot and not colours_correct_spot:
        for combination in combinations:
            if len(set(combo).intersection(combination)) == 0:
                combinations_remaining.add(combination)

    # No colours are in the correct spot
    elif not colours_correct_spot:
        # This needs to find combinations that contain exactly the same
        # number of common colours as colours_wrong_spot, with neither
        # of the two common colours being in the same spot and the
        # other two colours being unique from the the other two colours
        # of the combo
        for combination in combinations:
            i = 0
            flag = True
            while i < len(combo):
                if combo[i] == combination[i]:
                    flag = False
                i = i + 1
            if common_elements(combo, combination) == colours_wrong_spot and flag:
                combinations_remaining.add(combination)


    # Colours are only in the correct spot
    elif not colours_wrong_spot:
        for combination in combinations:
            if common_elements_same_spot(combo, combination) == colours_correct_spot and common_elements(combo, combination) == colours_correct_spot:
                combinations_remaining.add(combination)

    # Some colours are in the correct spot
    else:
        return

    print(combinations_remaining)
    return combinations_remaining

def common_elements(arr1, arr2):
    # Count occurrences of each element in both arrays
    counter1 = Counter(arr1)
    counter2 = Counter(arr2)
    
    # Calculate the intersection of keys (common elements)
    common_keys = counter1.keys() & counter2.keys()
    
    # Calculate the minimum occurrence of each common element
    common_counts = {key: min(counter1[key], counter2[key])
                        for key in common_keys}
    
    # Sum up the counts of common elements
    total_common_count = sum(common_counts.values())
    
    return total_common_count

def common_elements_same_spot(arr1, arr2):
    total_common_count = sum(x == y for x, y in zip(arr1, arr2))
    return total_common_count

# for combo in COMBINATIONS:
#     calculate_expected_information(combo, COMBINATIONS)

calculate_expected_information((1, 2, 3, 4), COMBINATIONS)