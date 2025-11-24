"""
Unit tests for the Student class.
"""

import pytest

from src.evaluation import Evaluation
from src.student import Student


class TestStudent:
    """Test cases for Student class."""

    def test_should_create_student_with_valid_id(self):
        """Test creating a student with valid ID."""
        student = Student("U202012345")
        assert student.student_id == "U202012345"
        assert student.get_evaluation_count() == 0

    def test_should_create_student_with_attendance_false_by_default(self):
        """Test that attendance is False by default."""
        student = Student("U202012345")
        assert student.has_reached_minimum_attendance is False

    def test_should_create_student_with_attendance_true(self):
        """Test creating student with attendance True."""
        student = Student("U202012345", has_reached_minimum_attendance=True)
        assert student.has_reached_minimum_attendance is True

    def test_should_raise_error_when_id_is_empty(self):
        """Test that empty ID raises ValueError."""
        with pytest.raises(ValueError, match="non-empty string"):
            Student("")

    def test_should_raise_error_when_id_is_whitespace(self):
        """Test that whitespace-only ID raises ValueError."""
        with pytest.raises(ValueError, match="non-empty string"):
            Student("   ")

    def test_should_raise_error_when_id_is_not_string(self):
        """Test that non-string ID raises ValueError."""
        with pytest.raises(ValueError, match="non-empty string"):
            Student(12345)

    def test_should_raise_error_when_attendance_is_not_boolean(self):
        """Test that non-boolean attendance raises ValueError."""
        with pytest.raises(ValueError, match="must be a boolean"):
            Student("U202012345", has_reached_minimum_attendance="yes")

    def test_should_trim_whitespace_from_id(self):
        """Test that whitespace is trimmed from ID."""
        student = Student("  U202012345  ")
        assert student.student_id == "U202012345"

    def test_should_add_evaluation_successfully(self):
        """Test adding an evaluation to student."""
        student = Student("U202012345")
        evaluation = Evaluation(15.0, 30.0)
        student.add_evaluation(evaluation)
        assert student.get_evaluation_count() == 1

    def test_should_add_multiple_evaluations(self):
        """Test adding multiple evaluations."""
        student = Student("U202012345")
        student.add_evaluation(Evaluation(15.0, 30.0))
        student.add_evaluation(Evaluation(16.0, 40.0))
        student.add_evaluation(Evaluation(17.0, 30.0))
        assert student.get_evaluation_count() == 3

    def test_should_raise_error_when_exceeding_max_evaluations(self):
        """Test that exceeding max evaluations raises ValueError."""
        student = Student("U202012345")
        for i in range(10):
            student.add_evaluation(Evaluation(15.0, 10.0))

        with pytest.raises(ValueError, match="Cannot add more than"):
            student.add_evaluation(Evaluation(15.0, 10.0))

    def test_should_raise_error_when_adding_non_evaluation(self):
        """Test that adding non-Evaluation raises ValueError."""
        student = Student("U202012345")
        with pytest.raises(ValueError, match="valid Evaluation instance"):
            student.add_evaluation("not an evaluation")

    def test_should_return_copy_of_evaluations_list(self):
        """Test that evaluations property returns a copy."""
        student = Student("U202012345")
        eval1 = Evaluation(15.0, 50.0)
        student.add_evaluation(eval1)

        evaluations = student.evaluations
        evaluations.append(Evaluation(16.0, 50.0))

        assert student.get_evaluation_count() == 1

    def test_should_clear_all_evaluations(self):
        """Test clearing all evaluations."""
        student = Student("U202012345")
        student.add_evaluation(Evaluation(15.0, 50.0))
        student.add_evaluation(Evaluation(16.0, 50.0))

        student.clear_evaluations()
        assert student.get_evaluation_count() == 0

    def test_should_set_attendance_status(self):
        """Test setting attendance status."""
        student = Student("U202012345", has_reached_minimum_attendance=False)
        student.has_reached_minimum_attendance = True
        assert student.has_reached_minimum_attendance is True

    def test_should_raise_error_when_setting_invalid_attendance(self):
        """Test that setting invalid attendance raises ValueError."""
        student = Student("U202012345")
        with pytest.raises(ValueError, match="must be a boolean"):
            student.has_reached_minimum_attendance = "yes"

    def test_should_have_correct_string_representation(self):
        """Test string representation of student."""
        student = Student("U202012345", has_reached_minimum_attendance=True)
        student.add_evaluation(Evaluation(15.0, 100.0))
        representation = str(student)
        assert "U202012345" in representation
        assert "1" in representation

    def test_should_allow_exactly_max_evaluations(self):
        """Test that exactly 10 evaluations are allowed."""
        student = Student("U202012345")
        for i in range(10):
            student.add_evaluation(Evaluation(15.0, 10.0))
        assert student.get_evaluation_count() == 10
