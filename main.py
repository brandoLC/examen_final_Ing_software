"""
CS-GradeCalculator - Main Application Entry Point

Sistema de cálculo de notas finales para docentes UTEC.
Caso de Uso: CU001 - Calcular nota final del estudiante
"""

import sys
from typing import List

from src.attendance_policy import AttendancePolicy
from src.evaluation import Evaluation
from src.extra_points_policy import ExtraPointsPolicy
from src.grade_calculator import GradeCalculator
from src.student import Student


class GradeCalculatorApp:
    """
    Main application class for the grade calculator system.
    """

    EXPECTED_WEIGHT_TOTAL = 100.0
    WEIGHT_TOLERANCE = 0.01
    HEADER_WIDTH = 60
    INITIAL_YEAR_INDEX = 0

    def __init__(self):
        """Initialize the application."""
        self.student = None
        self.extra_points_policy = None
        self.current_year_index = self.INITIAL_YEAR_INDEX

    def print_header(self) -> None:
        """Display application header."""
        print("=" * self.HEADER_WIDTH)
        print("CS-GradeCalculator - Sistema de Calculo de Notas UTEC")
        print("=" * self.HEADER_WIDTH)
        print()

    def get_student_info(self) -> None:
        """Get student identification from user."""
        print("--- Datos del Estudiante ---")
        while True:
            student_id = input("Ingrese el codigo del estudiante: ").strip()
            if student_id:
                break
            print("Error: El codigo no puede estar vacio.")

        self.student = Student(student_id)
        print(f"Estudiante registrado: {student_id}")
        print()

    def register_evaluations(self) -> None:
        """Register student evaluations."""
        print("--- Registro de Evaluaciones ---")
        print(f"Maximo de evaluaciones permitidas: {Student.MAX_EVALUATIONS}")

        while True:
            try:
                num_evaluations = int(input("Cantidad de evaluaciones a registrar: "))
                if 1 <= num_evaluations <= Student.MAX_EVALUATIONS:
                    break
                print(f"Error: Debe ser entre 1 y {Student.MAX_EVALUATIONS}")
            except ValueError:
                print("Error: Ingrese un numero valido")

        total_weight = 0.0
        evaluations_data = []

        for i in range(num_evaluations):
            print(f"\nEvaluacion {i + 1}:")
            while True:
                try:
                    grade = float(input(f"  Nota (0-20): "))
                    weight = float(input(f"  Peso porcentual: "))

                    evaluation = Evaluation(grade, weight)
                    evaluations_data.append((grade, weight))
                    total_weight += weight
                    break
                except ValueError as e:
                    print(f"  Error: {e}")

        if abs(total_weight - self.EXPECTED_WEIGHT_TOTAL) > self.WEIGHT_TOLERANCE:
            print(
                f"\nAdvertencia: Los pesos suman {total_weight}% (debe ser {self.EXPECTED_WEIGHT_TOTAL}%)"
            )
            print("Ajustando proporcionalmente...")

            factor = self.EXPECTED_WEIGHT_TOTAL / total_weight
            evaluations_data = [(g, w * factor) for g, w in evaluations_data]

        for grade, weight in evaluations_data:
            self.student.add_evaluation(Evaluation(grade, weight))

        print(f"\n{len(evaluations_data)} evaluaciones registradas correctamente.")
        print()

    def register_attendance(self) -> None:
        """Register student attendance status."""
        print("--- Asistencia del Estudiante ---")
        while True:
            response = input(
                "El estudiante cumplio con la asistencia minima? (s/n): "
            ).lower()
            if response in ["s", "n"]:
                self.student.has_reached_minimum_attendance = response == "s"
                break
            print("Error: Ingrese 's' para si o 'n' para no")

        status = "SI" if self.student.has_reached_minimum_attendance else "NO"
        print(f"Asistencia minima: {status}")
        print()

    def configure_extra_points_policy(self) -> None:
        """Configure extra points policy for academic years."""
        print("--- Politica de Puntos Extra ---")

        while True:
            try:
                num_years = int(input("Numero de años academicos a configurar: "))
                if num_years > 0:
                    break
                print("Error: Debe ser mayor a 0")
            except ValueError:
                print("Error: Ingrese un numero valido")

        all_years_teachers = []
        for i in range(num_years):
            while True:
                response = input(
                    f"Año {i + 1} - Docentes aprueban puntos extra? (s/n): "
                ).lower()
                if response in ["s", "n"]:
                    all_years_teachers.append(response == "s")
                    break
                print("Error: Ingrese 's' para si o 'n' para no")

        self.extra_points_policy = ExtraPointsPolicy(all_years_teachers)

        while True:
            try:
                self.current_year_index = (
                    int(input(f"Año academico actual (1-{num_years}): ")) - 1
                )
                if 0 <= self.current_year_index < num_years:
                    break
                print(f"Error: Debe ser entre 1 y {num_years}")
            except ValueError:
                print("Error: Ingrese un numero valido")

        print(f"Politica configurada para {num_years} años academicos.")
        print()

    def calculate_and_display_grade(self) -> None:
        """Calculate and display the final grade with details."""
        print("--- Calculando Nota Final ---")

        try:
            attendance_policy = AttendancePolicy(
                self.student.has_reached_minimum_attendance
            )

            calculator = GradeCalculator(
                evaluations=self.student.evaluations,
                attendance_policy=attendance_policy,
                extra_points_policy=self.extra_points_policy,
                current_year_index=self.current_year_index,
            )

            result = calculator.calculate_final_grade()

            print("\n" + "=" * self.HEADER_WIDTH)
            print("RESULTADO DEL CALCULO")
            print("=" * self.HEADER_WIDTH)
            print(f"Estudiante: {self.student.student_id}")
            print()

            print("Detalle del Calculo:")
            print(f"  1. Promedio Ponderado: {result.weighted_average:.2f}")

            if result.attendance_penalty_applied:
                print(f"  2. Penalizacion por Asistencia: SI (Nota = 0)")
            else:
                print(f"  2. Penalizacion por Asistencia: NO")

            print(f"  3. Puntos Extra Aplicados: +{result.extra_points_applied:.2f}")
            print()
            print(f"NOTA FINAL: {result.final_grade:.2f}")
            print("=" * self.HEADER_WIDTH)
            print()

        except Exception as e:
            print(f"Error al calcular la nota: {e}")
            sys.exit(1)

    def run(self) -> None:
        """Run the main application flow."""
        try:
            self.print_header()
            self.get_student_info()
            self.register_evaluations()
            self.register_attendance()
            self.configure_extra_points_policy()
            self.calculate_and_display_grade()

        except KeyboardInterrupt:
            print("\n\nOperacion cancelada por el usuario.")
            sys.exit(0)
        except Exception as e:
            print(f"\nError inesperado: {e}")
            sys.exit(1)


def main():
    """Main entry point."""
    app = GradeCalculatorApp()
    app.run()


if __name__ == "__main__":
    main()
