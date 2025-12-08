from typing import Set, Tuple, Dict
from Calculator import Calculator
from Mastermind import Mastermind
import math

class Solver:
    def __init__(self, columns: int, colours: set[int], combinations: set[tuple[int]], 
                 hints: set[tuple[int]], ans: tuple[int]) -> None:
        self.columns = columns
        self.colours = colours
        self.combinations_set = combinations
        self.combinations_list = list(combinations)
        self.hints = hints
        self.ans = ans
        self.mastermind = Mastermind(ans)
        self.calculator = Calculator()
        
        print("Precomputing score matrix...")
        self.score_matrix: Dict[Tuple[int, ...], Dict[Tuple[int, ...], Tuple[int, ...]]] = {}
        for guess in self.combinations_list:
            self.score_matrix[guess] = {}
            for secret in self.combinations_list:
                self.score_matrix[guess][secret] = self.calculator.score(guess, secret)
        print("Score matrix ready.")

    def expected_information(self, guess: tuple[int, ...], 
                                combinations_left: set[tuple[int, ...]]) -> float:
        """Entropy using precomputed matrix."""
        S = list(combinations_left)
        if len(S) <= 1:
            return 0.0
        
        feedback_counts = {}
        for secret in S:
            fb = self.score_matrix[guess][secret]
            feedback_counts[fb] = feedback_counts.get(fb, 0) + 1
        
        total = len(S)
        entropy = 0.0
        for count in feedback_counts.values():
            p = count / total
            entropy -= p * math.log2(p)
        return entropy

    
    def get_best_guess(self, current_combinations: Set[Tuple[int, ...]]) -> Tuple[int, ...]:
        """Best guess for game state."""
        if len(current_combinations) == 0:
            raise ValueError("No possible combinations left")
        if len(current_combinations) == 1:
            return current_combinations.pop()
        
        S = list(current_combinations)
        best_guess = S[0]
        max_entropy = -1.0
        
        for candidate in S:
            entropy = self.expected_information(candidate, current_combinations)
            if entropy > max_entropy:
                max_entropy = entropy
                best_guess = candidate
        return best_guess
    
    def solve_for_secret(self, secret: Tuple[int, ...], first_guess: Tuple[int, ...]) -> int:
        """Solve for secret using given first guess."""
        original_ans = self.mastermind.ans
        self.mastermind.ans = secret
        
        current = set(self.combinations_set)
        guesses = 0

        guess = first_guess
        hint = self.mastermind.hint(guess)
        current = self.calculator.calculate_possible_combinations(guess, current, hint)
        guesses += 1

        while len(current) > 1:
            guess = self.get_best_guess(current)
            hint = self.mastermind.hint(guess)
            current = self.calculator.calculate_possible_combinations(guess, current, hint)
            guesses += 1

        self.mastermind.ans = original_ans
        return guesses


    def analyze_average_guesses_for_first_guess(self, first_guess: Tuple[int, ...], 
                                              max_secrets: int = None) -> dict:
        """
        Test first guess against ALL 1296 secrets and compute average guesses needed.
        """
        print(f"\n=== Testing first guess {first_guess} across {len(self.combinations_list)} secrets ===")
        
        total_guesses = 0
        guess_distribution = {}
        secrets_tested = 0
        
        for secret_idx, secret in enumerate(self.combinations_list):
            if max_secrets and secrets_tested >= max_secrets:
                break
                
            guesses_needed = self.solve_for_secret(secret, first_guess)
            total_guesses += guesses_needed
            guess_distribution[guesses_needed] = guess_distribution.get(guesses_needed, 0) + 1
            secrets_tested += 1
            
            if secrets_tested % 100 == 0:
                print(f"Progress: {secrets_tested}/1296 secrets tested...")
        
        avg_guesses = total_guesses / secrets_tested
        
        print(f"\nResults for first guess {first_guess}:")
        print(f"Secrets tested: {secrets_tested}/1296")
        print(f"Average guesses: {avg_guesses:.3f}")
        print("Distribution:")
        for guesses, count in sorted(guess_distribution.items()):
            pct = (count / secrets_tested) * 100
            print(f"  {guesses} guesses: {count} cases ({pct:.1f}%)")
        
        return {
            'first_guess': first_guess,
            'secrets_tested': secrets_tested,
            'total_guesses': total_guesses,
            'average_guesses': avg_guesses,
            'worst_case': max(guess_distribution.keys()),
            'distribution': guess_distribution
        }

    def find_best_first_guess_by_average_guesses(self, candidate_first_guesses: list = None, 
                                            max_secrets: int = 500) -> dict:
        """Find best first guess by solving all secrets!"""
        if candidate_first_guesses is None:
            candidate_first_guesses = [
                (1,1,2,2), (1,2,1,2), (1,2,2,1), (1,1,1,2),
                (1,2,3,4), (1,1,1,1), (1,2,3,3)
            ]
        
        print(f"\n=== Finding best first guess by full simulation (max {max_secrets} secrets) ===\n")
        
        results = []
        for first_guess in candidate_first_guesses:
            stats = self.analyze_average_guesses_for_first_guess(first_guess, max_secrets)
            results.append(stats)

        results.sort(key=lambda x: x['average_guesses'])

        print(f"\nRANKING BY AVERAGE GUESSES:")
        print("First Guess  | Avg Guesses | Worst Case | Secrets Tested")
        print("-" * 50)
        for r in results:
            guess_str = str(r['first_guess'])
            print(f"{guess_str:10s} | {r['average_guesses']:10.3f} | {r['worst_case']:9d} | {r['secrets_tested']:12d}")
        
        return results


    def solve_step(self, current_combinations: Set[Tuple[int, ...]]) -> Tuple[Tuple[int, ...], Set[Tuple[int, ...]]]:
        """One complete solving step"""
        guess = self.get_best_guess(current_combinations)
        hint = self.mastermind.hint(guess)
        new_combinations = self.calculator.calculate_possible_combinations(guess, current_combinations, hint)
        return guess, new_combinations


    def interactive_solve(self):
        """Solves complete game."""
        current = set(self.combinations_set)
        guess_num = 1
        
        print(f"Starting with {len(current)} possible codes...")

        while len(current) > 1:
            print(f"\n--- Guess #{guess_num} ---")
            print(f"Remaining possibilities: {len(current)}")

            guess = self.get_best_guess(current)
            print(f"Suggested guess: {guess}")

            hint = self.mastermind.hint(guess)
            print(f"Hint received: {hint}")

            current = self.calculator.calculate_possible_combinations(guess, current, hint)
            guess_num += 1

        solution = current.pop()
        print(f"\nSolved in {guess_num-1} guesses!")
        print(f"Solution: {solution}")
        return solution


    def calculate_number_of_guesses(self, start_combinations: Set[Tuple[int, ...]]) -> int:
        """Simulate complete solving process."""
        current = set(start_combinations)
        guesses = 0
        
        while len(current) > 1:
            guess = self.get_best_guess(current)
            hint = self.mastermind.hint(guess)
            current = self.calculator.calculate_possible_combinations(guess, current, hint)
            guesses += 1
        
        print(f"Solved in {guesses} guesses")
        return guesses

    
    def get_best_first_guess(self) -> Tuple[int, ...]:
        """Best first guess maximizing initial entropy."""
        best_guess = self.combinations_list[0]
        max_entropy = -1.0
        
        for candidate in self.combinations_list:
            feedback_counts = {}
            for secret in self.combinations_list:
                fb = self.score_matrix[candidate][secret]
                feedback_counts[fb] = feedback_counts.get(fb, 0) + 1
            
            total = len(self.combinations_list)
            entropy = 0.0
            for count in feedback_counts.values():
                if count > 0:
                    p = count / total
                    entropy -= p * math.log2(p)
            
            if entropy > max_entropy:
                max_entropy = entropy
                best_guess = candidate
        
        print(f"Best first guess: {best_guess} (entropy: {max_entropy:.3f} bits)")
        return best_guess

    
    def evaluate_first_guess_performance(self, first_guess: Tuple[int, ...]) -> dict:
        """Detailed first guess analysis."""
        feedback_stats = {}
        total = len(self.combinations_list)
        
        for secret in self.combinations_list:
            fb = self.score_matrix[first_guess][secret]
            feedback_stats[fb] = feedback_stats.get(fb, 0) + 1
        
        entropy = 0.0
        for count in feedback_stats.values():
            p = count / total
            if p > 0:
                entropy -= p * math.log2(p)
        
        return {
            'first_guess': first_guess,
            'avg_remaining': sum(feedback_stats.values()) / total,
            'entropy': entropy,
            'feedback_distribution': feedback_stats
        }
