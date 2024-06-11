from context import mastermind

MASTERMIND = mastermind((1, 1, 1, 1))

def test_hint():
    assert(MASTERMIND.hint((1, 2, 3, 1)) == (2, 2))