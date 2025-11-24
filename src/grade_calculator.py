"""
Module for calculating final grades with detailed breakdown.
"""

from typing import Dict, List

from src.attendance_policy import AttendancePolicy
from src.evaluation import Evaluation
from src.extra_points_policy import ExtraPointsPolicy


class GradeCalculationResult:
    """
    Contains the result of a grade calculation with detailed breakdown.

    Attributes:
        weighted_average: The calculated weighted average of evaluations.
        attendance_penalty_applied: Whether attendance penalty was applied.
        extra_points_applied: Amount of extra points added.
        final_grade: The final calculated grade.
    """

    def __init__(
        self,
        weighted_average: float,
        attendance_penalty_applied: bool,
        extra_points_applied: float,
        final_grade: float,
    ):
        """Initialize the grade calculation result."""
        self.weighted_average = weighted_average
        self.attendance_penalty_applied = attendance_penalty_applied
        self.extra_points_applied = extra_points_applied
        self.final_grade = final_grade

    def get_details(self) -> Dict[str, any]:
        """
        Get detailed breakdown of the calculation.

        Returns:
            Dictionary with calculation details.
        """
        return {
            "weighted_average": round(self.weighted_average, 2),
            "attendance_penalty_applied": self.attendance_penalty_applied,
            "extra_points_applied": round(self.extra_points_applied, 2),
            "final_grade": round(self.final_grade, 2),
        }

    def __repr__(self) -> str:
        """String representation of the result."""
        return (
            f"GradeCalculationResult(weighted_avg={self.weighted_average:.2f}, "
            f"penalty={self.attendance_penalty_applied}, "
            f"extra_points={self.extra_points_applied:.2f}, "
            f"final={self.final_grade:.2f})"
        )


class GradeCalculator:
    """
    Calculates final grades based on evaluations, attendance, and extra points.

    This class implements the core business logic for grade calculation
    following UTEC academic regulations.
    """

    MAX_EVALUATIONS = 10
    WEIGHT_TOLERANCE = 0.01
    EXPECTED_TOTAL_WEIGHT = 100.0
    MIN_FINAL_GRADE = 0.0
    MAX_FINAL_GRADE = 20.0
    INITIAL_EXTRA_POINTS = 0.0

    def __init__(
        self,
        evaluations: List[Evaluation],
        attendance_policy: AttendancePolicy,
        extra_points_policy: ExtraPointsPolicy,
        current_year_index: int,
    ):
        """
        Initialize the grade calculator.

        Args:
            evaluations: List of student evaluations.
            attendance_policy: Policy for handling attendance.
            extra_points_policy: Policy for extra points.
            current_year_index: Index of current academic year.

        Raises:
            ValueError: If evaluations exceed maximum or weights don't sum to 100.
        """
        self._validate_evaluations(evaluations)
        self._evaluations = evaluations
        self._attendance_policy = attendance_policy
        self._extra_points_policy = extra_points_policy
        self._current_year_index = current_year_index

    def _validate_evaluations(self, evaluations: List[Evaluation]) -> None:
        """
        Validate evaluations list.

        Args:
            evaluations: List of evaluations to validate.

        Raises:
            ValueError: If validations fail.
        """
        if not isinstance(evaluations, list):
            raise ValueError("Evaluations must be a list")

        if len(evaluations) == 0:
            raise ValueError("Must have at least one evaluation")

        if len(evaluations) > self.MAX_EVALUATIONS:
            raise ValueError(
                f"Cannot have more than {self.MAX_EVALUATIONS} evaluations"
            )

        if not all(isinstance(e, Evaluation) for e in evaluations):
            raise ValueError("All elements must be Evaluation instances")

        total_weight = sum(e.weight for e in evaluations)
        if abs(total_weight - self.EXPECTED_TOTAL_WEIGHT) > self.WEIGHT_TOLERANCE:
            raise ValueError(
                f"Total weight must sum to {self.EXPECTED_TOTAL_WEIGHT}, "
                f"got {total_weight}"
            )

    def _calculate_weighted_average(self) -> float:
        """
        Calculate the weighted average of all evaluations.

        Returns:
            The weighted average grade.
        """
        total = sum(
            evaluation.calculate_weighted_grade() for evaluation in self._evaluations
        )
        return total

    def calculate_final_grade(self) -> GradeCalculationResult:
        """
        Calculate the final grade with all policies applied.

        Returns:
            GradeCalculationResult with detailed breakdown.
        """
        weighted_avg = self._calculate_weighted_average()

        grade_after_attendance = self._attendance_policy.apply_penalty(weighted_avg)
        attendance_penalty_applied = not self._attendance_policy.has_reached_minimum

        extra_points = self.INITIAL_EXTRA_POINTS
        if self._attendance_policy.has_reached_minimum:
            extra_points = self._extra_points_policy.calculate_extra_points(
                self._current_year_index
            )

        final_grade = grade_after_attendance + extra_points

        final_grade = max(self.MIN_FINAL_GRADE, min(self.MAX_FINAL_GRADE, final_grade))

        return GradeCalculationResult(
            weighted_average=weighted_avg,
            attendance_penalty_applied=attendance_penalty_applied,
            extra_points_applied=extra_points,
            final_grade=final_grade,
        )

    def __repr__(self) -> str:
        """String representation of the calculator."""
        return (
            f"GradeCalculator(evaluations={len(self._evaluations)}, "
            f"year={self._current_year_index})"
        )
