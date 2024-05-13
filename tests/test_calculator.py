import pytest
from context import Calculator

CALCULATOR = Calculator()

def test_commmon_elements_same_spot():
    # Basic Test
    assert(CALCULATOR.common_elements_same_spot((1, 2, 1, 1), (1, 2, 3, 1)) == 3)

    # None in the same spot
    assert(CALCULATOR.common_elements_same_spot((0, 3, 1, 2), (1, 2, 3, 1)) == 0)

    # None are the same
    assert(CALCULATOR.common_elements_same_spot((0, 0, 0, 0), (1, 1, 1, 1)) == 0)

    # All are the same
    assert(CALCULATOR.common_elements_same_spot((1, 2, 1, 1), (1, 2, 1, 1)) == 4)

def test_common_elements():
    # Basic Test
    assert(CALCULATOR.common_elements((1, 2, 1, 4), (1, 2, 3, 1)) == 3)
    
    # None are the same
    assert(CALCULATOR.common_elements((0, 0, 0, 0), (1, 1, 1, 1)) == 0)

    # All are the same
    assert(CALCULATOR.common_elements((1, 2, 1, 1), (1, 2, 1, 1)) == 4)

def test_calculate_all_possible_combinations():
    # One in the correct spot
    assert(CALCULATOR.calculate_possible_combinations((1, 1, 1, 1), [(1, 2, 3, 4), (1, 1, 2, 3), (2, 3, 4, 5), (1, 1, 1, 2), (1, 1, 1, 1), (2, 1, 3, 4)], (0, 0, 0, 2)) == {(1, 2, 3, 4), (2, 1, 3, 4)})

    # Two in the correct spot
    assert(CALCULATOR.calculate_possible_combinations((1, 1, 1, 1), [(1, 2, 3, 4), (1, 1, 2, 3), (2, 3, 4, 5), (1, 1, 1, 2), (1, 1, 1, 1), (2, 1, 3, 4)], (0, 0, 2, 2)) == {(1, 1, 2, 3)})

    # All correct spot
    assert(CALCULATOR.calculate_possible_combinations((1, 2, 3), [(1, 2, 3), (1, 2, 1), (3, 2, 1), (2, 3, 1)], (2, 2, 2)) == {(1, 2, 3)})

    # No possible combinations
    assert(CALCULATOR.calculate_possible_combinations((1, 1, 1, 1), [(1, 2, 3, 4), (1, 1, 2, 3), (2, 3, 4, 5), (1, 1, 1, 2), (1, 1, 1, 1)], (0, 0, 0, 1)) == set())

    # One in the correct spot, One in the wrong spot
    assert(CALCULATOR.calculate_possible_combinations((1, 2, 1, 1), [(1, 2, 3, 4), (1, 1, 2, 3), (2, 3, 4, 5), (1, 1, 1, 2), (1, 1, 1, 1), (2, 1, 3, 4), (2, 3, 1, 4)], (0, 0, 1, 2)) == {(2, 3, 1, 4)})

    # Two in the correct spot, Two in the wrong spot
    assert(CALCULATOR.calculate_possible_combinations((1, 2, 3, 4), [(1, 2, 3, 4), (1, 1, 2, 3), (2, 3, 4, 5), (1, 1, 1, 2), (1, 1, 1, 1), (2, 1, 3, 4), (2, 3, 1, 4), (1, 2, 4, 3)], (2, 1, 1, 2)) == {(1, 2, 4, 3), (2, 1, 3, 4)})

    # One in the wrong spot
    assert(CALCULATOR.calculate_possible_combinations((1, 2, 1, 1), [(1, 2, 3, 4), (1, 1, 2, 3), (2, 3, 4, 5), (1, 1, 1, 2), (1, 1, 1, 1), (2, 1, 3, 4), (2, 3, 1, 4)], (0, 0, 0, 1)) == {(2, 3, 4, 5)})

    # Three in the wrong spot
    assert(CALCULATOR.calculate_possible_combinations((1, 2, 1, 1), [(1, 2, 3, 4), (1, 1, 2, 3), (2, 3, 4, 5), (1, 1, 1, 2), (1, 1, 1, 1), (2, 1, 3, 4), (2, 3, 1, 4)], (0, 1, 1, 1)) == set())