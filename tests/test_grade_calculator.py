"""
Unit tests for the GradeCalculator class.
"""

import pytest

from src.attendance_policy import AttendancePolicy
from src.evaluation import Evaluation
from src.extra_points_policy import ExtraPointsPolicy
from src.grade_calculator import GradeCalculationResult, GradeCalculator


class TestGradeCalculationResult:
    """Test cases for GradeCalculationResult class."""

    def test_should_create_result_with_all_fields(self):
        """Test creating a calculation result."""
        result = GradeCalculationResult(15.5, False, 1.0, 16.5)
        assert result.weighted_average == 15.5
        assert result.attendance_penalty_applied is False
        assert result.extra_points_applied == 1.0
        assert result.final_grade == 16.5

    def test_should_get_details_as_dictionary(self):
        """Test getting result details as dictionary."""
        result = GradeCalculationResult(15.5, False, 1.0, 16.5)
        details = result.get_details()
        assert details["weighted_average"] == 15.5
        assert details["attendance_penalty_applied"] is False
        assert details["extra_points_applied"] == 1.0
        assert details["final_grade"] == 16.5

    def test_should_round_values_in_details(self):
        """Test that details are rounded to 2 decimals."""
        result = GradeCalculationResult(15.556, False, 1.126, 16.666)
        details = result.get_details()
        assert details["weighted_average"] == 15.56
        assert details["extra_points_applied"] == 1.13
        assert details["final_grade"] == 16.67


class TestGradeCalculator:
    """Test cases for GradeCalculator class."""

    def test_should_calculate_normal_case_with_attendance_and_extra_points(self):
        """Test normal calculation with attendance and extra points."""
        evaluations = [
            Evaluation(16.0, 30.0),
            Evaluation(14.0, 40.0),
            Evaluation(18.0, 30.0),
        ]
        attendance = AttendancePolicy(True)
        extra_points = ExtraPointsPolicy([True, False])

        calculator = GradeCalculator(evaluations, attendance, extra_points, 0)
        result = calculator.calculate_final_grade()

        expected_avg = (16.0 * 0.3) + (14.0 * 0.4) + (18.0 * 0.3)
        assert result.weighted_average == expected_avg
        assert result.attendance_penalty_applied is False
        assert result.extra_points_applied == 1.0
        assert result.final_grade == expected_avg + 1.0

    def test_should_return_zero_when_attendance_not_met(self):
        """Test that final grade is zero without attendance."""
        evaluations = [Evaluation(18.0, 50.0), Evaluation(19.0, 50.0)]
        attendance = AttendancePolicy(False)
        extra_points = ExtraPointsPolicy([True])

        calculator = GradeCalculator(evaluations, attendance, extra_points, 0)
        result = calculator.calculate_final_grade()

        assert result.weighted_average == 18.5
        assert result.attendance_penalty_applied is True
        assert result.extra_points_applied == 0.0
        assert result.final_grade == 0.0

    def test_should_calculate_without_extra_points_when_year_consensus_false(self):
        """Test calculation when year has no extra points consensus."""
        evaluations = [Evaluation(15.0, 50.0), Evaluation(16.0, 50.0)]
        attendance = AttendancePolicy(True)
        extra_points = ExtraPointsPolicy([False, True, False])

        calculator = GradeCalculator(evaluations, attendance, extra_points, 0)
        result = calculator.calculate_final_grade()

        assert result.extra_points_applied == 0.0
        assert result.final_grade == 15.5

    def test_should_calculate_with_zero_grade_evaluation(self):
        """Test calculation with a zero grade."""
        evaluations = [Evaluation(0.0, 30.0), Evaluation(15.0, 70.0)]
        attendance = AttendancePolicy(True)
        extra_points = ExtraPointsPolicy([False])

        calculator = GradeCalculator(evaluations, attendance, extra_points, 0)
        result = calculator.calculate_final_grade()

        expected_avg = (0.0 * 0.3) + (15.0 * 0.7)
        assert result.weighted_average == expected_avg
        assert result.final_grade == expected_avg

    def test_should_calculate_with_all_zero_grades(self):
        """Test calculation with all zero grades."""
        evaluations = [Evaluation(0.0, 50.0), Evaluation(0.0, 50.0)]
        attendance = AttendancePolicy(True)
        extra_points = ExtraPointsPolicy([True])

        calculator = GradeCalculator(evaluations, attendance, extra_points, 0)
        result = calculator.calculate_final_grade()

        assert result.weighted_average == 0.0
        assert result.extra_points_applied == 1.0
        assert result.final_grade == 1.0

    def test_should_cap_final_grade_at_maximum(self):
        """Test that final grade doesn't exceed 20."""
        evaluations = [Evaluation(20.0, 100.0)]
        attendance = AttendancePolicy(True)
        extra_points = ExtraPointsPolicy([True])

        calculator = GradeCalculator(evaluations, attendance, extra_points, 0)
        result = calculator.calculate_final_grade()

        assert result.final_grade == 20.0

    def test_should_raise_error_when_no_evaluations(self):
        """Test that empty evaluations list raises ValueError."""
        attendance = AttendancePolicy(True)
        extra_points = ExtraPointsPolicy([True])

        with pytest.raises(ValueError, match="at least one evaluation"):
            GradeCalculator([], attendance, extra_points, 0)

    def test_should_raise_error_when_exceeding_max_evaluations(self):
        """Test that more than 10 evaluations raises ValueError."""
        evaluations = [Evaluation(15.0, 10.0) for _ in range(11)]
        attendance = AttendancePolicy(True)
        extra_points = ExtraPointsPolicy([True])

        with pytest.raises(ValueError, match="Cannot have more than"):
            GradeCalculator(evaluations, attendance, extra_points, 0)

    def test_should_raise_error_when_weights_dont_sum_to_100(self):
        """Test that weights not summing to 100 raises ValueError."""
        evaluations = [Evaluation(15.0, 40.0), Evaluation(16.0, 40.0)]
        attendance = AttendancePolicy(True)
        extra_points = ExtraPointsPolicy([True])

        with pytest.raises(ValueError, match="Total weight must sum"):
            GradeCalculator(evaluations, attendance, extra_points, 0)

    def test_should_raise_error_when_evaluations_not_list(self):
        """Test that non-list evaluations raises ValueError."""
        attendance = AttendancePolicy(True)
        extra_points = ExtraPointsPolicy([True])

        with pytest.raises(ValueError, match="must be a list"):
            GradeCalculator("not a list", attendance, extra_points, 0)

    def test_should_raise_error_when_list_contains_non_evaluation(self):
        """Test that non-Evaluation in list raises ValueError."""
        evaluations = [Evaluation(15.0, 50.0), "not an evaluation"]
        attendance = AttendancePolicy(True)
        extra_points = ExtraPointsPolicy([True])

        with pytest.raises(ValueError, match="must be Evaluation instances"):
            GradeCalculator(evaluations, attendance, extra_points, 0)

    def test_should_accept_weights_summing_to_100_within_tolerance(self):
        """Test that weights close to 100 are accepted."""
        evaluations = [
            Evaluation(15.0, 33.33),
            Evaluation(16.0, 33.34),
            Evaluation(17.0, 33.33),
        ]
        attendance = AttendancePolicy(True)
        extra_points = ExtraPointsPolicy([False])

        calculator = GradeCalculator(evaluations, attendance, extra_points, 0)
        result = calculator.calculate_final_grade()

        assert result is not None

    def test_should_be_deterministic_with_same_inputs(self):
        """Test that calculation is deterministic (RNF03)."""
        evaluations1 = [
            Evaluation(16.0, 30.0),
            Evaluation(14.0, 40.0),
            Evaluation(18.0, 30.0),
        ]
        evaluations2 = [
            Evaluation(16.0, 30.0),
            Evaluation(14.0, 40.0),
            Evaluation(18.0, 30.0),
        ]
        attendance1 = AttendancePolicy(True)
        attendance2 = AttendancePolicy(True)
        extra_points1 = ExtraPointsPolicy([True, False])
        extra_points2 = ExtraPointsPolicy([True, False])

        calculator1 = GradeCalculator(evaluations1, attendance1, extra_points1, 0)
        calculator2 = GradeCalculator(evaluations2, attendance2, extra_points2, 0)

        result1 = calculator1.calculate_final_grade()
        result2 = calculator2.calculate_final_grade()

        assert result1.final_grade == result2.final_grade
        assert result1.weighted_average == result2.weighted_average
        assert result1.extra_points_applied == result2.extra_points_applied

    def test_should_calculate_with_single_evaluation(self):
        """Test calculation with single evaluation."""
        evaluations = [Evaluation(17.5, 100.0)]
        attendance = AttendancePolicy(True)
        extra_points = ExtraPointsPolicy([False])

        calculator = GradeCalculator(evaluations, attendance, extra_points, 0)
        result = calculator.calculate_final_grade()

        assert result.weighted_average == 17.5
        assert result.final_grade == 17.5

    def test_should_calculate_with_maximum_evaluations(self):
        """Test calculation with 10 evaluations (RNF01)."""
        evaluations = [Evaluation(15.0, 10.0) for _ in range(10)]
        attendance = AttendancePolicy(True)
        extra_points = ExtraPointsPolicy([False])

        calculator = GradeCalculator(evaluations, attendance, extra_points, 0)
        result = calculator.calculate_final_grade()

        assert result.weighted_average == 15.0
        assert result.final_grade == 15.0

    def test_should_have_correct_string_representation(self):
        """Test string representation of calculator."""
        evaluations = [Evaluation(15.0, 100.0)]
        attendance = AttendancePolicy(True)
        extra_points = ExtraPointsPolicy([True])

        calculator = GradeCalculator(evaluations, attendance, extra_points, 0)
        representation = str(calculator)

        assert "1" in representation
        assert "0" in representation
