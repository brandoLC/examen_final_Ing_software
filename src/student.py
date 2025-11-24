"""
Module for managing student data and evaluations.
"""

from typing import List

from src.evaluation import Evaluation


class Student:
    """
    Represents a student with their evaluations and attendance status.

    Attributes:
        student_id: Unique identifier for the student.
        evaluations: List of evaluations for this student.
        has_reached_minimum_attendance: Whether student met attendance requirement.
    """

    MAX_EVALUATIONS = 10

    def __init__(self, student_id: str, has_reached_minimum_attendance: bool = False):
        """
        Initialize a Student instance.

        Args:
            student_id: Unique identifier for the student.
            has_reached_minimum_attendance: Attendance status.

        Raises:
            ValueError: If student_id is empty or invalid.
        """
        if not isinstance(student_id, str):
            raise ValueError("Student ID must be a non-empty string")

        if not student_id or not student_id.strip():
            raise ValueError("Student ID must be a non-empty string")

        if not isinstance(has_reached_minimum_attendance, bool):
            raise ValueError("has_reached_minimum_attendance must be a boolean")

        self._student_id = student_id.strip()
        self._evaluations: List[Evaluation] = []
        self._has_reached_minimum_attendance = has_reached_minimum_attendance

    @property
    def student_id(self) -> str:
        """Get the student ID."""
        return self._student_id

    @property
    def evaluations(self) -> List[Evaluation]:
        """Get a copy of the evaluations list."""
        return self._evaluations.copy()

    @property
    def has_reached_minimum_attendance(self) -> bool:
        """Check if student met minimum attendance."""
        return self._has_reached_minimum_attendance

    @has_reached_minimum_attendance.setter
    def has_reached_minimum_attendance(self, value: bool) -> None:
        """
        Set the attendance status.

        Args:
            value: New attendance status.

        Raises:
            ValueError: If value is not a boolean.
        """
        if not isinstance(value, bool):
            raise ValueError("Attendance status must be a boolean")
        self._has_reached_minimum_attendance = value

    def add_evaluation(self, evaluation: Evaluation) -> None:
        """
        Add an evaluation to the student's record.

        Args:
            evaluation: The evaluation to add.

        Raises:
            ValueError: If maximum evaluations exceeded or invalid evaluation.
        """
        if not isinstance(evaluation, Evaluation):
            raise ValueError("Must provide a valid Evaluation instance")

        if len(self._evaluations) >= self.MAX_EVALUATIONS:
            raise ValueError(f"Cannot add more than {self.MAX_EVALUATIONS} evaluations")

        self._evaluations.append(evaluation)

    def clear_evaluations(self) -> None:
        """Remove all evaluations from the student's record."""
        self._evaluations.clear()

    def get_evaluation_count(self) -> int:
        """
        Get the number of evaluations registered.

        Returns:
            Number of evaluations.
        """
        return len(self._evaluations)

    def __repr__(self) -> str:
        """String representation of the student."""
        return (
            f"Student(id={self._student_id}, "
            f"evaluations={len(self._evaluations)}, "
            f"attendance_ok={self._has_reached_minimum_attendance})"
        )
