from context import mastermind

def test_hint():
    game = mastermind((1, 2, 3, 4))
    assert(game.hint((1, 2, 3, 1)) == (2, 2, 2))

    assert(game.hint((1, 2, 3, 4)) == (3))

    assert(game.hint((1, 2, 5, 3)) == (2, 2, 1))

    assert(game.hint((1, 1, 5, 3)) == (2, 1))

    assert(game.hint((5, 5, 5, 5)) == ())

    assert(game.hint((2, 3, 4, 1)) == (1, 1, 1, 1))