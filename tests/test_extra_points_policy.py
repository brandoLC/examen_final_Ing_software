"""
Unit tests for the ExtraPointsPolicy class.
"""

import pytest

from src.extra_points_policy import ExtraPointsPolicy


class TestExtraPointsPolicy:
    """Test cases for ExtraPointsPolicy class."""

    def test_should_create_policy_with_empty_list(self):
        """Test creating policy with empty consensus history."""
        policy = ExtraPointsPolicy([])
        assert policy.consensus_history == []

    def test_should_create_policy_with_single_year(self):
        """Test creating policy with single year consensus."""
        policy = ExtraPointsPolicy([True])
        assert policy.consensus_history == [True]

    def test_should_create_policy_with_multiple_years(self):
        """Test creating policy with multiple years."""
        consensus = [True, False, True, True]
        policy = ExtraPointsPolicy(consensus)
        assert policy.consensus_history == consensus

    def test_should_raise_error_when_input_is_not_list(self):
        """Test that non-list input raises ValueError."""
        with pytest.raises(ValueError, match="must be a list"):
            ExtraPointsPolicy("not a list")

    def test_should_raise_error_when_list_contains_non_boolean(self):
        """Test that list with non-boolean values raises ValueError."""
        with pytest.raises(ValueError, match="must be boolean"):
            ExtraPointsPolicy([True, "yes", False])

    def test_should_raise_error_when_list_contains_integer(self):
        """Test that list with integers raises ValueError."""
        with pytest.raises(ValueError, match="must be boolean"):
            ExtraPointsPolicy([True, 1, False])

    def test_should_calculate_extra_points_when_consensus_is_true(self):
        """Test extra points calculation when consensus is True."""
        policy = ExtraPointsPolicy([True, False, True])
        result = policy.calculate_extra_points(0)
        assert result == 1.0

    def test_should_return_zero_when_consensus_is_false(self):
        """Test zero extra points when consensus is False."""
        policy = ExtraPointsPolicy([True, False, True])
        result = policy.calculate_extra_points(1)
        assert result == 0.0

    def test_should_calculate_extra_points_for_last_year(self):
        """Test extra points calculation for last year in list."""
        policy = ExtraPointsPolicy([False, False, True])
        result = policy.calculate_extra_points(2)
        assert result == 1.0

    def test_should_raise_error_when_year_index_is_negative(self):
        """Test that negative year index raises ValueError."""
        policy = ExtraPointsPolicy([True, False])
        with pytest.raises(ValueError, match="Year index must be"):
            policy.calculate_extra_points(-1)

    def test_should_raise_error_when_year_index_exceeds_range(self):
        """Test that out of range year index raises ValueError."""
        policy = ExtraPointsPolicy([True, False])
        with pytest.raises(ValueError, match="Year index must be"):
            policy.calculate_extra_points(2)

    def test_should_check_consensus_for_specific_year(self):
        """Test checking consensus for a specific year."""
        policy = ExtraPointsPolicy([True, False, True])
        assert policy.has_consensus_for_year(0) is True
        assert policy.has_consensus_for_year(1) is False
        assert policy.has_consensus_for_year(2) is True

    def test_should_return_false_for_invalid_year_index(self):
        """Test that invalid year index returns False."""
        policy = ExtraPointsPolicy([True, False])
        assert policy.has_consensus_for_year(-1) is False
        assert policy.has_consensus_for_year(5) is False

    def test_should_return_copy_of_consensus_history(self):
        """Test that consensus_history returns a copy."""
        original = [True, False, True]
        policy = ExtraPointsPolicy(original)
        history = policy.consensus_history
        history[0] = False
        assert policy.consensus_history[0] is True

    def test_should_have_correct_string_representation(self):
        """Test string representation of policy."""
        policy = ExtraPointsPolicy([True, False])
        representation = str(policy)
        assert "True" in representation
        assert "False" in representation

    def test_should_be_deterministic_with_same_inputs(self):
        """Test that policy is deterministic."""
        policy1 = ExtraPointsPolicy([True, False, True])
        policy2 = ExtraPointsPolicy([True, False, True])

        result1 = policy1.calculate_extra_points(0)
        result2 = policy2.calculate_extra_points(0)

        assert result1 == result2
