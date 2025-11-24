"""
Module for handling student evaluations.
"""


class Evaluation:
    """
    Represents a single evaluation with its grade and weight.

    Attributes:
        grade: The numerical grade obtained (0-20 scale).
        weight: The percentage weight of this evaluation (0-100).
    """

    MIN_GRADE = 0.0
    MAX_GRADE = 20.0
    MIN_WEIGHT = 0.0
    MAX_WEIGHT = 100.0
    PERCENTAGE_DIVISOR = 100.0

    def __init__(self, grade: float, weight: float):
        """
        Initialize an Evaluation instance.

        Args:
            grade: The grade obtained in the evaluation.
            weight: The weight percentage of this evaluation.

        Raises:
            ValueError: If grade or weight are out of valid ranges.
        """
        self._validate_grade(grade)
        self._validate_weight(weight)
        self._grade = float(grade)
        self._weight = float(weight)

    @property
    def grade(self) -> float:
        """Get the grade value."""
        return self._grade

    @property
    def weight(self) -> float:
        """Get the weight value."""
        return self._weight

    def _validate_grade(self, grade: float) -> None:
        """
        Validate that grade is within acceptable range.

        Args:
            grade: The grade to validate.

        Raises:
            ValueError: If grade is out of range.
        """
        if not isinstance(grade, (int, float)):
            raise ValueError("Grade must be a number")
        if grade < self.MIN_GRADE or grade > self.MAX_GRADE:
            raise ValueError(
                f"Grade must be between {self.MIN_GRADE} and {self.MAX_GRADE}"
            )

    def _validate_weight(self, weight: float) -> None:
        """
        Validate that weight is within acceptable range.

        Args:
            weight: The weight to validate.

        Raises:
            ValueError: If weight is out of range.
        """
        if not isinstance(weight, (int, float)):
            raise ValueError("Weight must be a number")
        if weight < self.MIN_WEIGHT or weight > self.MAX_WEIGHT:
            raise ValueError(
                f"Weight must be between {self.MIN_WEIGHT} and {self.MAX_WEIGHT}"
            )

    def calculate_weighted_grade(self) -> float:
        """
        Calculate the weighted contribution of this evaluation.

        Returns:
            The weighted grade (grade * weight / 100).
        """
        return self._grade * (self._weight / self.PERCENTAGE_DIVISOR)

    def __repr__(self) -> str:
        """String representation of the evaluation."""
        return f"Evaluation(grade={self._grade}, weight={self._weight}%)"
