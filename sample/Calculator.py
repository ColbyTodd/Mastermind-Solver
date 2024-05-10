from collections import Counter

class Calculator:

    def __init__(self):
        return

    def calculate_expected_information(self, combo: tuple, combinations: set):
        """Calculates the expected amount of information gained from a 
        given guess.""" 

        # for hint in HINTS:
        #     calculate_information(combo, hint, combinations)

        self.calculate_information(combo, [2, 2, 0, 0], combinations)

    def calculate_information(self, combo: tuple, hint: tuple, combinations: set):
        """Calculates the information gained from a guess with a specific
        hint."""
        self.calculate_possible_combinations(combo, hint, combinations)

    def calculate_possible_combinations(self, combo: tuple, hint: tuple, 
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
                if self.common_elements(combo, combination) == colours_wrong_spot and flag:
                    combinations_remaining.add(combination)

        # Rest of the possibilities
        else:
            for combination in combinations:
                if self.common_elements_same_spot(combo, combination) == colours_correct_spot and self.common_elements(combo, combination) == colours_correct_spot + colours_wrong_spot:
                    combinations_remaining.add(combination)

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