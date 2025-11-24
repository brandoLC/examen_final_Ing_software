"""
Module for handling attendance policy and penalties.
"""


class AttendancePolicy:
    """
    Handles attendance validation and penalty calculation.

    According to UTEC academic regulations, students must meet
    minimum attendance requirements to pass the course.
    """

    PENALTY_FOR_INSUFFICIENT_ATTENDANCE = 0.0

    def __init__(self, has_reached_minimum: bool):
        """
        Initialize the attendance policy.

        Args:
            has_reached_minimum: Whether the student met minimum attendance.
        """
        if not isinstance(has_reached_minimum, bool):
            raise ValueError("has_reached_minimum must be a boolean")
        self._has_reached_minimum = has_reached_minimum

    @property
    def has_reached_minimum(self) -> bool:
        """Check if student reached minimum attendance."""
        return self._has_reached_minimum

    def apply_penalty(self, base_grade: float) -> float:
        """
        Apply attendance penalty to the base grade if applicable.

        Args:
            base_grade: The calculated weighted average grade.

        Returns:
            The grade after applying attendance penalty.
            If attendance is insufficient, returns 0.
        """
        if not self._has_reached_minimum:
            return self.PENALTY_FOR_INSUFFICIENT_ATTENDANCE
        return base_grade

    def __repr__(self) -> str:
        """String representation of attendance policy."""
        status = "Met" if self._has_reached_minimum else "Not met"
        return f"AttendancePolicy(minimum_attendance={status})"
