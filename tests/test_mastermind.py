import pytest
from context import Mastermind

class TestMastermind:
    """Comprehensive unit tests for Mastermind class."""

    @pytest.fixture
    def mastermind_1111(self):
        """Mastermind with secret (1,1,1,1)."""
        return Mastermind((1,1,1,1))

    @pytest.fixture
    def mastermind_1234(self):
        """Mastermind with secret (1,2,3,4)."""
        return Mastermind((1,2,3,4))

    @pytest.fixture
    def mastermind_1122(self):
        """Mastermind with secret (1,1,2,2)."""
        return Mastermind((1,1,2,2))

    def test_init_sets_answer(self):
        """Test Mastermind initialization stores answer correctly."""
        mm = Mastermind((1,2,3,4))
        assert mm.ans == (1,2,3,4)

    def test_hint_exact_match_all_positions(self, mastermind_1111):
        """Test perfect guess returns all 2s."""
        result = mastermind_1111.hint((1,1,1,1))
        assert result == (2,2,2,2)

    def test_hint_all_correct_position(self, mastermind_1234):
        """Test all positions correct returns all 2s."""
        result = mastermind_1234.hint((1,2,3,4))
        assert result == (2,2,2,2)

    def test_hint_no_matches(self, mastermind_1111):
        """Test guess with no matching colors returns all 0s."""
        result = mastermind_1111.hint((2,2,2,2))
        assert result == (0,0,0,0)

    def test_hint_all_wrong_position(self, mastermind_1234):
        """Test all colors correct but wrong positions."""
        result = mastermind_1234.hint((4,3,2,1))
        assert result == (1,1,1,1)

    def test_hint_mixed_positions(self, mastermind_1122):
        """Test two correct positions, two wrong."""
        result = mastermind_1122.hint((2,1,1,2))
        assert result == (2,2,1,1)

    def test_hint_all_white_pins(self, mastermind_1122):
        """Test all colors present but wrong positions."""
        result = mastermind_1122.hint((2,2,1,1))
        assert result == (1,1,1,1)

    def test_hint_three_correct_one_wrong(self, mastermind_1234):
        """Test three exact matches, one wrong."""
        result = mastermind_1234.hint((1,2,3,5))
        assert result == (2,2,2,0)

    def test_hint_two_exact_two_color_match(self, mastermind_1122):
        """Test two exact positions, one color match."""
        result = mastermind_1122.hint((1,3,2,1))
        assert result == (2,2,1,0)

    def test_hint_duplicates_handling(self, mastermind_1111):
        """Test handling of duplicate colors correctly."""
        result = mastermind_1111.hint((1,1,2,3))
        assert result == (2,2,0,0)

    def test_hint_partial_duplicates(self):
        """Test secret with duplicates, guess with fewer."""
        mm = Mastermind((1,1,2,3))
        result = mm.hint((1,2,1,4))
        assert result == (2,1,1,0)

    def test_hint_longer_shorter_no(self):
        """Test hint works with different lengths (though not expected)."""
        mm = Mastermind((1,2))
        result = mm.hint((1,2))
        assert result == (2,2)

    def test_hint_same_length_always(self, mastermind_1234):
        """Test hint always returns tuple same length as guess."""
        result = mastermind_1234.hint((1,2,3,4))
        assert len(result) == 4

    def test_hint_valid_pin_values(self, mastermind_1234):
        """Test hint only contains valid pin values (0,1,2)."""
        result = mastermind_1234.hint((4,4,4,4))
        assert all(pin in (0,1,2) for pin in result)

    def test_hint_internal_consistency(self):
        """Test hint logic doesn't modify original ans."""
        original_ans = (1,2,3,4)
        mm = Mastermind(original_ans)
        mm.hint((4,4,4,4))
        assert mm.ans == original_ans

    def test_hint_repeated_calls_same_result(self, mastermind_1111):
        """Test hint is deterministic for same guess."""
        guess = (1,1,1,2)
        result1 = mastermind_1111.hint(guess)
        result2 = mastermind_1111.hint(guess)
        assert result1 == result2

    def test_mastermind_edge_cases(self):
        """Test various edge case combinations - FIXED as standalone method."""
        test_cases = [
            # (secret, guess, expected_hint)
            ((1,1,1,1), (1,1,1,1), (2,2,2,2)),
            ((1,2,3,4), (1,1,1,1), (2,0,0,0)),
            ((1,1,2,2), (2,2,1,1), (1,1,1,1)),
            ((1,2,1,2), (1,1,2,2), (2,2,1,1)),
            ((1,1,1,2), (2,1,1,1), (2,2,1,1)),
        ]
        
        for secret, guess, expected in test_cases:
            mm = Mastermind(secret)
            result = mm.hint(guess)
            assert result == expected, f"Failed: secret={secret}, guess={guess}, got={result}, expected={expected}"
