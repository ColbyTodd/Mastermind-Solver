import pytest
from context import Calculator

CALCULATOR = Calculator()

def test_commmon_elements_same_spot():
    assert(CALCULATOR.common_elements_same_spot((1, 2, 1, 1), (1, 2, 3, 1)) == 3)