from itertools import product
from Calculator import Calculator
from Mastermind import Mastermind

class Solver:

    def __init__(self, columns: int, colours: set[int], combinations: set[tuple[int]], hints: set[tuple[int]]) -> None:
        self.columns = columns
        self.colours = colours
        self.combinations = combinations
        self.hints = hints
    
    def find_best_combo(self) -> tuple[int]:
        calculator = Calculator()
        combinations = set()
        combination = [1 for i in range(self.columns)]
        for i in range(min(self.columns, len(self.colours))):
            combination[i] += i
            combinations.add(tuple(combination))
        best_combo = ()
        max_expected_information = 0

        for combo in combinations:
            expected_information = calculator.calculate_expected_information(combo, self.combinations, self.hints)
            
            if expected_information > max_expected_information:
                best_combo = combo
                max_expected_information = expected_information

        return best_combo
    
    def find_best_combo_with_hint(self, ans: tuple[int], combinations_left: set[tuple[int]]) -> tuple[int]:
        mastermind = Mastermind(ans)
        calculator = Calculator()
        best_combo = ()
        max_expected_information = 0

        for combo in self.combinations:
            expected_information = calculator.calculate_information_with_hint(combo, combinations_left, mastermind.hint(combo))
            
            if expected_information > max_expected_information:
                best_combo = combo
                max_expected_information = expected_information

        return best_combo
    
    def find_best_overall_combo_with_hint(self, ans: tuple[int], information) -> tuple[int]:
        mastermind = Mastermind(ans)
        calculator = Calculator()
        # combinations = set()
        # combination = [1 for i in range(self.columns)]
        # for i in range(min(self.columns, len(self.colours))):
        #     combination[i] += i
        #     combinations.add(tuple(combination))
        # best_combo = ()
        # max_expected_information = 0

        for combo in self.combinations:
            information[combo] += calculator.calculate_information_with_hint(combo, self.combinations, mastermind.hint(combo))

        return information
    
    def calculate_number_of_guesses(self, ans: tuple[int], combo: tuple[int], combinations: set[tuple[int]]) -> int:
        mastermind = Mastermind(ans)
        calculator = Calculator()
        guesses = 0
        while combo != ans:
            combo = self.find_best_combo_with_hint(ans, combinations)
            combinations = calculator.calculate_possible_combinations(combo, combinations, mastermind.hint(combo))
            guesses += 1

        return guesses

    def find_best_expected_combo(self):
        information = {combo: 0 for combo in self.combinations}
        for combo in self.combinations:
            information += self.calculate_number_of_guesses((1, 1, 1, 1), combo, self.combinations)

        return max(information, key=information.get)

    # def find_best_combo_with_lookahead(self, lookahead: int) -> tuple[int]:
    #     calculator = Calculator()
    #     combinations = set()
    #     combination = [1 for i in range(self.columns)]
    #     for i in range(min(self.columns, len(self.colours))):
    #         combination[i] += i
    #         combinations.add(tuple(combination))
    #     best_combo = ()
    #     max_expected_information = 0

    #     for combo in combinations:
    #         expected_information = calculator.calculate_expected_information_with_lookahead(combo, self.combinations, self.hints, lookahead)
            
    #         if expected_information > max_expected_information:
    #             best_combo = combo
    #             max_expected_information = expected_information

    #     print("Best combo = " + str(best_combo) + "\nExpected information = " + str(max_expected_information))

    #     return best_combo