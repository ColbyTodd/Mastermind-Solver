from collections import Counter
import math

class Calculator:

    def __init__(self):
        return
    
    def calculate_expected_information_with_lookahead(self, combo: tuple[int], combinations: set[tuple[int]], hints: set[int],  lookahead: int) -> float:
        """Calculates the expected amount of information gained from a 
        given guess.""" 
        sum = 0
        if not lookahead:
            return sum

        for hint in hints:
            sum += self.calculate_information_with_lookahead(combo, combinations, hint, hints, lookahead)
        
        return sum


    def calculate_information_with_lookahead(self, combo: tuple[int], combinations: set[tuple[int]], hint: tuple[int], hints: set[int], lookahead: int) -> float:
        """Calculates the information gained from a guess with a specific
        hint."""
        possible_combinations = self.calculate_possible_combinations(combo, combinations, hint)

        if len(possible_combinations) == 1:
            return 0

        if len(possible_combinations) / len(combinations) > 0:
            sum = 0
            for combo in possible_combinations: 
                sum += self.calculate_expected_information_with_lookahead(combo, possible_combinations, hints, lookahead - 1)
            return len(possible_combinations) / len(combinations) * (math.log2(len(combinations) / len(possible_combinations)) + sum)
        
        return 0

    def calculate_expected_information(self, combo: tuple[int], combinations: set[tuple[int]], hints: set[int]) -> float:
        """Calculates the expected amount of information gained from a 
        given guess.""" 
        sum = 0
        for hint in hints:
            sum += self.calculate_information(combo, combinations, hint)
        
        return sum


    def calculate_information(self, combo: tuple[int], combinations: set[tuple[int]], hint: tuple[int]) -> float:
        """Calculates the information gained from a guess with a specific
        hint."""
        possible_combinations = self.calculate_possible_combinations(combo, combinations, hint)
        if len(possible_combinations) / len(combinations) > 0:
            return len(possible_combinations) / len(combinations) * math.log2(len(combinations) / len(possible_combinations))
        
        return 0

    def calculate_possible_combinations(self, combo: tuple[int], combinations: set[tuple[int]], hint: tuple[int]) -> set[tuple[int]]:
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

        return combinations_remaining

    def common_elements(self, arr1: list, arr2: list) -> int:
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

    def common_elements_same_spot(self, arr1: list, arr2: list) -> int:
        total_common_count = sum(x == y for x, y in zip(arr1, arr2))
        return total_common_count