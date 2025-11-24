"""
Unit tests for the Evaluation class.
"""

import pytest

from src.evaluation import Evaluation


class TestEvaluation:
    """Test cases for Evaluation class."""

    def test_should_create_evaluation_with_valid_data(self):
        """Test creating an evaluation with valid grade and weight."""
        evaluation = Evaluation(15.5, 30.0)
        assert evaluation.grade == 15.5
        assert evaluation.weight == 30.0

    def test_should_create_evaluation_with_zero_grade(self):
        """Test creating an evaluation with zero grade."""
        evaluation = Evaluation(0.0, 20.0)
        assert evaluation.grade == 0.0
        assert evaluation.weight == 20.0

    def test_should_create_evaluation_with_maximum_grade(self):
        """Test creating an evaluation with maximum grade (20)."""
        evaluation = Evaluation(20.0, 40.0)
        assert evaluation.grade == 20.0
        assert evaluation.weight == 40.0

    def test_should_raise_error_when_grade_below_minimum(self):
        """Test that grade below 0 raises ValueError."""
        with pytest.raises(ValueError, match="Grade must be between"):
            Evaluation(-1.0, 30.0)

    def test_should_raise_error_when_grade_above_maximum(self):
        """Test that grade above 20 raises ValueError."""
        with pytest.raises(ValueError, match="Grade must be between"):
            Evaluation(21.0, 30.0)

    def test_should_raise_error_when_weight_below_minimum(self):
        """Test that weight below 0 raises ValueError."""
        with pytest.raises(ValueError, match="Weight must be between"):
            Evaluation(15.0, -5.0)

    def test_should_raise_error_when_weight_above_maximum(self):
        """Test that weight above 100 raises ValueError."""
        with pytest.raises(ValueError, match="Weight must be between"):
            Evaluation(15.0, 105.0)

    def test_should_raise_error_when_grade_is_not_numeric(self):
        """Test that non-numeric grade raises ValueError."""
        with pytest.raises(ValueError, match="Grade must be a number"):
            Evaluation("invalid", 30.0)

    def test_should_raise_error_when_weight_is_not_numeric(self):
        """Test that non-numeric weight raises ValueError."""
        with pytest.raises(ValueError, match="Weight must be a number"):
            Evaluation(15.0, "invalid")

    def test_should_calculate_weighted_grade_correctly(self):
        """Test weighted grade calculation."""
        evaluation = Evaluation(16.0, 25.0)
        expected = 16.0 * 0.25
        assert evaluation.calculate_weighted_grade() == expected

    def test_should_calculate_weighted_grade_with_zero_grade(self):
        """Test weighted grade calculation with zero grade."""
        evaluation = Evaluation(0.0, 30.0)
        assert evaluation.calculate_weighted_grade() == 0.0

    def test_should_calculate_weighted_grade_with_full_weight(self):
        """Test weighted grade calculation with 100% weight."""
        evaluation = Evaluation(18.0, 100.0)
        assert evaluation.calculate_weighted_grade() == 18.0

    def test_should_have_correct_string_representation(self):
        """Test string representation of evaluation."""
        evaluation = Evaluation(15.5, 30.0)
        assert "15.5" in str(evaluation)
        assert "30.0" in str(evaluation)

    def test_should_convert_integer_to_float(self):
        """Test that integer inputs are converted to float."""
        evaluation = Evaluation(15, 30)
        assert isinstance(evaluation.grade, float)
        assert isinstance(evaluation.weight, float)
        assert evaluation.grade == 15.0
        assert evaluation.weight == 30.0
