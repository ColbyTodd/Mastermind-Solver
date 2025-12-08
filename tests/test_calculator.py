import pytest
import math
from context import Calculator

class TestCalculator:
    """Comprehensive unit tests for Calculator class."""

    @pytest.fixture
    def calculator(self):
        """Calculator instance."""
        return Calculator()

    @pytest.fixture
    def small_combinations(self):
        """Small set of combinations for testing."""
        return set([
            (1,1,1,1), (1,1,1,2), (1,1,2,1), (1,2,1,1),
            (2,1,1,1), (1,1,2,2), (1,2,1,2), (1,2,2,1)
        ])

    def test_init(self, calculator):
        """Test Calculator initialization."""
        assert calculator is not None

    def test_score_perfect_match(self, calculator):
        """Test perfect position match returns all 2s."""
        result = calculator.score((1,2,3,4), (1,2,3,4))
        assert result == (2,2,2,2)

    def test_score_no_matches(self, calculator):
        """Test no matches returns all 0s."""
        result = calculator.score((1,1,1,1), (2,2,2,2))
        assert result == (0,0,0,0)

    def test_score_all_wrong_position(self, calculator):
        """Test all colors correct, wrong positions."""
        result = calculator.score((4,3,2,1), (1,2,3,4))
        assert result == (1,1,1,1)

    def test_score_mixed_black_white(self, calculator):
        """Test mixed exact and color matches."""
        result = calculator.score((1,3,2,1), (1,1,2,2))
        assert result == (2,2,1,0)

    def test_score_duplicates(self, calculator):
        """Test duplicate color handling."""
        result = calculator.score((1,1,2,3), (1,1,1,1))
        assert result == (2,2,0,0)

    def test_score_partial_duplicates(self, calculator):
        """Test secret with duplicates, guess with fewer."""
        result = calculator.score((1,2,1,4), (1,1,2,3))
        assert result == (2,1,1,0)

    def test_score_different_lengths(self, calculator):
        """Test score works with different lengths."""
        result = calculator.score((1,2), (1,2))
        assert result == (2,2)

    def test_score_valid_pins(self, calculator):
        """Test score only returns valid pin values."""
        result = calculator.score((5,5,5,5), (1,2,3,4))
        assert all(pin in (0,1,2) for pin in result)

    def test_calculate_possible_combinations_empty(self, calculator):
        """Test empty combinations returns empty set."""
        result = calculator.calculate_possible_combinations((1,1,1,1), set(), (2,2,2,2))
        assert result == set()

    def test_calculate_possible_combinations_exact_match(self, calculator, small_combinations):
        """Test filtering finds exact match."""
        result = calculator.calculate_possible_combinations((1,1,1,1), small_combinations, (2,2,2,2))
        assert (1,1,1,1) in result

    def test_calculate_possible_combinations_no_match(self, calculator, small_combinations):
        """Test filtering with impossible hint returns empty - FIXED."""
        result = calculator.calculate_possible_combinations((9,9,9,9), small_combinations, (2,2,2,0))
        assert len(result) == 0

    def test_calculate_possible_combinations_partial_match(self, calculator, small_combinations):
        """Test filtering finds partial matches."""
        hint = calculator.score((1,1,1,1), (1,1,1,2))  # Should be (3,0)
        result = calculator.calculate_possible_combinations((1,1,1,1), small_combinations, hint)
        assert len(result) > 0

    def test_calculate_expected_information_empty(self, calculator):
        """Test entropy for empty set is 0.0."""
        result = calculator.calculate_expected_information((1,1,1,1), set())
        assert result == 0.0

    def test_calculate_expected_information_single(self, calculator):
        """Test entropy for single combination is 0.0."""
        result = calculator.calculate_expected_information((1,1,1,1), {(1,1,1,1)})
        assert result == 0.0

    def test_calculate_expected_information_multiple(self, calculator, small_combinations):
        """Test entropy > 0 for multiple combinations."""
        result = calculator.calculate_expected_information((1,1,1,1), small_combinations)
        assert result > 0.0

    def test_calculate_information_with_hint_empty(self, calculator, small_combinations):
        """Test information with empty possible set."""
        result = calculator.calculate_information_with_hint((1,1,1,1), small_combinations, (9,9,9,9))
        assert result == 0.0

    def test_calculate_information_with_hint_no_reduction(self, calculator, small_combinations):
        """Test information when hint doesn't reduce possibilities."""
        hint = calculator.score((9,9,9,9), (1,1,1,1))
        result = calculator.calculate_information_with_hint((9,9,9,9), small_combinations, hint)
        assert math.isclose(result, 0.0, abs_tol=1e-10)

    def test_calculate_information_with_hint_reduction(self, calculator, small_combinations):
        """Test information gain when possibilities reduced."""
        hint = (2,2,2,2)
        result = calculator.calculate_information_with_hint((1,1,1,1), small_combinations, hint)
        assert result > 0.0

    def test_score_consistency_with_mastermind(self, calculator):
        """Test Calculator.score matches Mastermind.hint logic."""
        from context import Mastermind
        test_cases = [
            ((1,2,3,4), (1,2,3,4), (2,2,2,2)),
            ((1,1,1,1), (2,2,2,2), (0,0,0,0)),
            ((1,2,3,4), (4,3,2,1), (1,1,1,1)),
        ]
        for secret, guess, expected in test_cases:
            mm = Mastermind(secret)
            calc_result = calculator.score(guess, secret)
            mm_result = mm.hint(guess)
            assert calc_result == mm_result == expected

    def test_all_calculator_methods(self, calculator, small_combinations):
        """Test all methods work together correctly."""
        combo = (1,1,1,1)
        hint = calculator.score(combo, (1,1,1,1))
        possibles = calculator.calculate_possible_combinations(combo, small_combinations, hint)
        info = calculator.calculate_information_with_hint(combo, small_combinations, hint)
        
        assert isinstance(possibles, set)
        assert (1,1,1,1) in possibles
        assert info > 0.0

def test_calculator_edge_cases():
    """Standalone comprehensive edge cases test."""
    calc = Calculator()
    test_cases = [
        # (guess, secret, expected_score)
        ((1,1,1,1), (1,1,1,1), (2,2,2,2)),
        ((1,2,3,4), (1,1,1,1), (2,0,0,0)),
        ((2,2,1,1), (1,1,2,2), (1,1,1,1)),
        ((1,1,2,2), (1,2,1,2), (2,2,1,1)),
        ((2,1,1,1), (1,1,1,2), (2,2,1,1)),
    ]
    
    for guess, secret, expected in test_cases:
        result = calc.score(guess, secret)
        assert result == expected, f"Failed: guess={guess}, secret={secret}, got={result}"
