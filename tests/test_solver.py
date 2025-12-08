import pytest
from context import Solver, Calculator, Mastermind
import math

@pytest.fixture
def small_combinations():
    """Small set of 4-color combinations for fast testing."""
    return set([
        (1,1,1,1), (1,1,1,2), (1,1,2,1), (1,2,1,1),
        (2,1,1,1), (1,1,2,2), (1,2,1,2), (1,2,2,1)
    ])

@pytest.fixture
def small_hints():
    """Possible hints for 4 positions."""
    return set([
        (4,0), (3,0), (2,0), (1,0), (0,0),
        (0,1), (0,2), (0,3), (0,4), (2,1), (1,1), (1,2)
    ])

@pytest.fixture
def solver_small(small_combinations, small_hints):
    """Solver with small combinations for fast testing."""
    columns = 4
    colours = {1, 2}
    ans = (1,1,1,1)
    solver = Solver(columns, colours, small_combinations, small_hints, ans)
    return solver

def test_solver_init(solver_small):
    """Test Solver initialization with real Calculator and Mastermind."""
    assert solver_small.columns == 4
    assert solver_small.colours == {1, 2}
    assert len(solver_small.combinations_set) == 8
    assert isinstance(solver_small.calculator, Calculator)
    assert isinstance(solver_small.mastermind, Mastermind)
    assert isinstance(solver_small.score_matrix, dict)
    assert len(solver_small.score_matrix) == 8

def test_expected_information_single(solver_small):
    """Test expected_information returns 0.0 for single combination."""
    combinations_left = {(1,1,1,1)}
    result = solver_small.expected_information((1,1,1,1), combinations_left)
    assert result == 0.0

def test_expected_information_multiple(solver_small):
    """Test expected_information calculates entropy > 0 for multiple combinations."""
    combinations_left = {(1,1,1,1), (2,1,1,1)}
    result = solver_small.expected_information((1,1,1,2), combinations_left)
    assert result > 0.0

def test_get_best_guess_single(solver_small):
    """Test get_best_guess returns only combination when one left."""
    combinations = {(1,2,1,2)}
    result = solver_small.get_best_guess(combinations)
    assert result == (1,2,1,2)

def test_get_best_guess_multiple(solver_small):
    """Test get_best_guess selects from multiple combinations."""
    combinations = {(1,1,1,1), (1,1,1,2), (2,1,1,1)}
    result = solver_small.get_best_guess(combinations)
    assert result in combinations

def test_solve_step(solver_small):
    """Test solve_step returns guess and filtered combinations."""
    current = {(1,1,1,1), (1,1,1,2)}
    guess, new_combinations = solver_small.solve_step(current)
    
    assert guess in current
    assert isinstance(new_combinations, set)
    assert len(new_combinations) <= len(current)

def test_solve_for_secret_complete_match(solver_small):
    """Test solve_for_secret when first guess matches secret."""
    secret = (1,1,1,1)
    first_guess = (1,1,1,1)
    guesses = solver_small.solve_for_secret(secret, first_guess)
    assert guesses == 1

def test_solve_for_secret_multiple_guesses(solver_small):
    """Test solve_for_secret requires multiple guesses."""
    secret = (1,2,1,2)
    first_guess = (1,1,1,1)
    guesses = solver_small.solve_for_secret(secret, first_guess)
    assert guesses >= 2

def test_calculate_number_of_guesses_single(solver_small):
    """Test calculate_number_of_guesses with single combination."""
    start_combinations = {(1,1,1,1)}
    guesses = solver_small.calculate_number_of_guesses(start_combinations)
    assert guesses == 0

def test_calculate_number_of_guesses_multiple(solver_small):
    """Test calculate_number_of_guesses with multiple combinations."""
    start_combinations = {(1,1,1,1), (1,1,1,2)}
    guesses = solver_small.calculate_number_of_guesses(start_combinations)
    assert guesses >= 1

def test_interactive_solve(solver_small):
    """Test interactive_solve completes successfully."""
    result = solver_small.interactive_solve()
    assert isinstance(result, tuple)
    assert len(result) == 4

def test_get_best_first_guess(solver_small):
    """Test get_best_first_guess returns valid combination."""
    result = solver_small.get_best_first_guess()
    assert result in solver_small.combinations_set

def test_evaluate_first_guess_performance(solver_small):
    """Test evaluate_first_guess_performance returns expected structure."""
    first_guess = (1,1,1,1)
    result = solver_small.evaluate_first_guess_performance(first_guess)
    
    assert 'first_guess' in result
    assert 'entropy' in result
    assert result['entropy'] >= 0.0
    assert 'feedback_distribution' in result

def test_analyze_average_guesses_structure(solver_small):
    """Test analyze_average_guesses_for_first_guess returns dict with expected keys."""
    first_guess = (1,1,1,1)
    result = solver_small.analyze_average_guesses_for_first_guess(first_guess, max_secrets=3)
    
    expected_keys = ['first_guess', 'secrets_tested', 'total_guesses', 
                    'average_guesses', 'worst_case', 'distribution']
    for key in expected_keys:
        assert key in result

def test_find_best_first_guess(solver_small):
    """Test find_best_first_guess_by_average_guesses returns sorted results."""
    candidates = [(1,1,1,1), (1,1,1,2)]
    results = solver_small.find_best_first_guess_by_average_guesses(candidates, max_secrets=3)
    
    assert len(results) == 2
    assert results[0]['average_guesses'] <= results[1]['average_guesses']

def test_score_matrix_consistency(solver_small):
    """Test score_matrix produces same results as real Calculator.score."""
    calc = Calculator()
    guess = (1,1,1,1)
    secret = (1,1,1,2)
    
    matrix_score = solver_small.score_matrix[guess][secret]
    real_score = calc.score(guess, secret)
    
    assert matrix_score == real_score
