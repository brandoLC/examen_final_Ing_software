"""
Unit tests for the AttendancePolicy class.
"""

import pytest

from src.attendance_policy import AttendancePolicy


class TestAttendancePolicy:
    """Test cases for AttendancePolicy class."""

    def test_should_create_policy_with_minimum_attendance_met(self):
        """Test creating policy when minimum attendance is met."""
        policy = AttendancePolicy(True)
        assert policy.has_reached_minimum is True

    def test_should_create_policy_with_minimum_attendance_not_met(self):
        """Test creating policy when minimum attendance is not met."""
        policy = AttendancePolicy(False)
        assert policy.has_reached_minimum is False

    def test_should_raise_error_when_attendance_is_not_boolean(self):
        """Test that non-boolean attendance raises ValueError."""
        with pytest.raises(ValueError, match="must be a boolean"):
            AttendancePolicy("yes")

    def test_should_raise_error_when_attendance_is_none(self):
        """Test that None attendance raises ValueError."""
        with pytest.raises(ValueError, match="must be a boolean"):
            AttendancePolicy(None)

    def test_should_not_apply_penalty_when_attendance_is_met(self):
        """Test no penalty applied when attendance requirement is met."""
        policy = AttendancePolicy(True)
        base_grade = 15.5
        result = policy.apply_penalty(base_grade)
        assert result == base_grade

    def test_should_apply_penalty_when_attendance_is_not_met(self):
        """Test penalty applied when attendance requirement is not met."""
        policy = AttendancePolicy(False)
        base_grade = 15.5
        result = policy.apply_penalty(base_grade)
        assert result == 0.0

    def test_should_return_zero_for_high_grade_when_attendance_not_met(self):
        """Test that even high grades become zero without attendance."""
        policy = AttendancePolicy(False)
        base_grade = 20.0
        result = policy.apply_penalty(base_grade)
        assert result == 0.0

    def test_should_preserve_zero_grade_when_attendance_met(self):
        """Test that zero grade stays zero even with attendance."""
        policy = AttendancePolicy(True)
        base_grade = 0.0
        result = policy.apply_penalty(base_grade)
        assert result == 0.0

    def test_should_preserve_zero_grade_when_attendance_not_met(self):
        """Test that zero grade stays zero without attendance."""
        policy = AttendancePolicy(False)
        base_grade = 0.0
        result = policy.apply_penalty(base_grade)
        assert result == 0.0

    def test_should_have_correct_string_representation_when_met(self):
        """Test string representation when attendance is met."""
        policy = AttendancePolicy(True)
        representation = str(policy)
        assert "Met" in representation

    def test_should_have_correct_string_representation_when_not_met(self):
        """Test string representation when attendance is not met."""
        policy = AttendancePolicy(False)
        representation = str(policy)
        assert "Not met" in representation

    def test_should_be_deterministic_with_same_inputs(self):
        """Test that policy application is deterministic."""
        policy1 = AttendancePolicy(True)
        policy2 = AttendancePolicy(True)
        base_grade = 16.7

        result1 = policy1.apply_penalty(base_grade)
        result2 = policy2.apply_penalty(base_grade)

        assert result1 == result2
