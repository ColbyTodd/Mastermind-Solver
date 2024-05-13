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