import math

class Calculator:
    def __init__(self):
        pass

    def score(self, guess: tuple[int, ...], secret: tuple[int, ...]) -> tuple[int, ...]:
        """Compute exact Mastermind feedback matching Mastermind.hint logic."""
        n = len(guess)
        guess_list = list(guess)
        secret_list = list(secret)
        
        # First pass: exact position matches (black pins = 2s)
        hint = []
        for i in range(n):
            if guess_list[i] == secret_list[i]:
                hint.append(2)
                guess_list[i] = -1
                secret_list[i] = -1
        
        # Second pass: color matches in wrong position (white pins = 1s)
        for i in range(n):
            if guess_list[i] != -1 and guess_list[i] in secret_list:
                secret_list.remove(guess_list[i])
                hint.append(1)
        
        # Fill remaining with 0s
        hint.extend([0] * (n - len(hint)))
        return tuple(hint)

    def calculate_possible_combinations(self, combo: tuple[int, ...], 
                                      combinations: set[tuple[int, ...]], 
                                      hint: tuple[int, ...]) -> set[tuple[int, ...]]:
        """Filter using exact score match."""
        return {c for c in combinations if self.score(combo, c) == hint}

    def calculate_expected_information(self, combo: tuple[int, ...], 
                                     combinations: set[tuple[int, ...]]) -> float:
        """True entropy over actual feedback distribution."""
        feedback_counts = {}
        for secret in combinations:
            fb = self.score(combo, secret)
            feedback_counts[fb] = feedback_counts.get(fb, 0) + 1
        
        total = len(combinations)
        if total == 0 or total == 1:
            return 0.0
        entropy = 0.0
        for count in feedback_counts.values():
            p = count / total
            entropy -= p * math.log2(p)
        return entropy

    def calculate_information_with_hint(self, combo: tuple[int, ...], 
                                      combinations: set[tuple[int, ...]], 
                                      hint: tuple[int, ...]) -> float:
        """Information given this specific hint occurred."""
        possible = self.calculate_possible_combinations(combo, combinations, hint)
        total = len(combinations)
        if len(possible) == 0 or total == 0:
            return 0.0
        return math.log2(total / len(possible))
