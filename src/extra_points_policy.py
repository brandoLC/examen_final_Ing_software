"""
Module for handling extra points policy based on teacher consensus.
"""

from typing import List


class ExtraPointsPolicy:
    """
    Manages extra points based on yearly teacher consensus.

    Each year, teachers collectively decide whether to award
    extra points to students meeting certain criteria.
    """

    EXTRA_POINTS_VALUE = 1.0
    NO_EXTRA_POINTS = 0.0

    def __init__(self, all_years_teachers: List[bool]):
        """
        Initialize the extra points policy.

        Args:
            all_years_teachers: List of boolean values indicating
                               teacher consensus for each academic year.

        Raises:
            ValueError: If input is not a list or contains non-boolean values.
        """
        if not isinstance(all_years_teachers, list):
            raise ValueError("all_years_teachers must be a list")

        if not all(isinstance(decision, bool) for decision in all_years_teachers):
            raise ValueError("All elements in all_years_teachers must be boolean")

        self._all_years_teachers = all_years_teachers

    @property
    def consensus_history(self) -> List[bool]:
        """Get the teacher consensus history."""
        return self._all_years_teachers.copy()

    def calculate_extra_points(self, current_year_index: int) -> float:
        """
        Calculate extra points for a specific academic year.

        Args:
            current_year_index: Index of the current academic year (0-based).

        Returns:
            Extra points value if consensus is True for that year, 0 otherwise.

        Raises:
            ValueError: If year index is out of range.
        """
        if current_year_index < 0 or current_year_index >= len(
            self._all_years_teachers
        ):
            raise ValueError(
                f"Year index must be between 0 and {len(self._all_years_teachers) - 1}"
            )

        if self._all_years_teachers[current_year_index]:
            return self.EXTRA_POINTS_VALUE
        return self.NO_EXTRA_POINTS

    def has_consensus_for_year(self, year_index: int) -> bool:
        """
        Check if teachers agreed on extra points for a specific year.

        Args:
            year_index: Index of the academic year to check.

        Returns:
            True if consensus was reached, False otherwise.
        """
        if year_index < 0 or year_index >= len(self._all_years_teachers):
            return False
        return self._all_years_teachers[year_index]

    def __repr__(self) -> str:
        """String representation of extra points policy."""
        return f"ExtraPointsPolicy(consensus={self._all_years_teachers})"
