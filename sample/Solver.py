from itertools import product
from Calculator import Calculator

class Solver:

    def __init__(self, columns: int, colours: set[int], combinations: set[tuple[int]], hints: set[tuple[int]]) -> None:
        self.columns = columns
        self.colours = colours
        self.combinations = combinations
        self.hints = hints
    
    def find_best_combo(self) -> tuple[int]:
        calculator = Calculator()
        colours = set()
        for i in range (1, self.columns + 1):
            colours.add(i)
        combinations = set(product(colours, repeat = self.columns))
        best_combo = ()
        max_expected_information = 0

        for combo in combinations:
            expected_information = calculator.calculate_expected_information(combo, self.combinations, self.hints)
            
            if expected_information > max_expected_information:
                best_combo = combo
                max_expected_information = expected_information

        print("Best combo = " + str(best_combo) + "\nExpected information = " + str(max_expected_information))

        return best_combo

    def find_best_combo_with_lookahead(self) -> tuple[int]:
        calculator = Calculator()
        colours = set()
        for i in range (1, self.columns + 1):
            colours.add(i)
        combinations = set(product(colours, repeat = self.columns))
        best_combo = ()
        max_expected_information = 0

        for combo in combinations:
            expected_information = calculator.calculate_expected_information(combo, self.combinations, self.hints)
            
            if expected_information > max_expected_information:
                best_combo = combo
                max_expected_information = expected_information

        print("Best combo = " + str(best_combo) + "\nExpected information = " + str(max_expected_information))

        return best_combo