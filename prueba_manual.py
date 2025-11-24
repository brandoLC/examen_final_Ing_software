"""
Script de prueba manual para CS-GradeCalculator
Ejecuta varios casos de prueba de forma automatica
"""

from src.attendance_policy import AttendancePolicy
from src.evaluation import Evaluation
from src.extra_points_policy import ExtraPointsPolicy
from src.grade_calculator import GradeCalculator
from src.student import Student


def print_separator():
    """Imprime una linea separadora"""
    print("\n" + "=" * 70 + "\n")


def test_case_1():
    """Caso 1: Estudiante con asistencia y puntos extra"""
    print("CASO 1: Estudiante con asistencia completa y puntos extra")
    print("-" * 70)

    student = Student("U202012345", has_reached_minimum_attendance=True)

    # Agregar evaluaciones
    student.add_evaluation(Evaluation(16.0, 30.0))  # Parcial 1: 16, peso 30%
    student.add_evaluation(Evaluation(14.0, 40.0))  # Parcial 2: 14, peso 40%
    student.add_evaluation(Evaluation(18.0, 30.0))  # Final: 18, peso 30%

    print(f"Estudiante: {student.student_id}")
    print(f"Evaluaciones: {student.get_evaluation_count()}")
    for i, ev in enumerate(student.evaluations, 1):
        print(f"  Evaluacion {i}: Nota={ev.grade}, Peso={ev.weight}%")
    print(f"Asistencia minima: SI")

    # Configurar politicas
    attendance = AttendancePolicy(student.has_reached_minimum_attendance)
    extra_points = ExtraPointsPolicy([True, False, True])

    print(f"Politica puntos extra: Año 1=SI, Año 2=NO, Año 3=SI")
    print(f"Año academico actual: 1")

    # Calcular
    calculator = GradeCalculator(
        evaluations=student.evaluations,
        attendance_policy=attendance,
        extra_points_policy=extra_points,
        current_year_index=0,
    )

    result = calculator.calculate_final_grade()

    # Mostrar resultado
    print("\nRESULTADO:")
    print(f"  Promedio Ponderado: {result.weighted_average:.2f}")
    print(
        f"  Penalizacion por Asistencia: {'SI' if result.attendance_penalty_applied else 'NO'}"
    )
    print(f"  Puntos Extra Aplicados: +{result.extra_points_applied:.2f}")
    print(f"  NOTA FINAL: {result.final_grade:.2f}")


def test_case_2():
    """Caso 2: Estudiante SIN asistencia"""
    print("CASO 2: Estudiante sin asistencia minima")
    print("-" * 70)

    student = Student("U202067890", has_reached_minimum_attendance=False)

    # Agregar evaluaciones (buenas notas pero sin asistencia)
    student.add_evaluation(Evaluation(18.0, 50.0))
    student.add_evaluation(Evaluation(19.0, 50.0))

    print(f"Estudiante: {student.student_id}")
    print(f"Evaluaciones:")
    for i, ev in enumerate(student.evaluations, 1):
        print(f"  Evaluacion {i}: Nota={ev.grade}, Peso={ev.weight}%")
    print(f"Asistencia minima: NO")

    # Configurar politicas
    attendance = AttendancePolicy(student.has_reached_minimum_attendance)
    extra_points = ExtraPointsPolicy([True])

    # Calcular
    calculator = GradeCalculator(
        evaluations=student.evaluations,
        attendance_policy=attendance,
        extra_points_policy=extra_points,
        current_year_index=0,
    )

    result = calculator.calculate_final_grade()

    # Mostrar resultado
    print("\nRESULTADO:")
    print(f"  Promedio Ponderado: {result.weighted_average:.2f}")
    print(
        f"  Penalizacion por Asistencia: {'SI - Nota queda en 0' if result.attendance_penalty_applied else 'NO'}"
    )
    print(f"  Puntos Extra Aplicados: +{result.extra_points_applied:.2f}")
    print(f"  NOTA FINAL: {result.final_grade:.2f}")


def test_case_3():
    """Caso 3: Año sin puntos extra"""
    print("CASO 3: Estudiante en año sin consenso de puntos extra")
    print("-" * 70)

    student = Student("U202011111", has_reached_minimum_attendance=True)

    # Agregar evaluaciones
    student.add_evaluation(Evaluation(15.0, 50.0))
    student.add_evaluation(Evaluation(16.0, 50.0))

    print(f"Estudiante: {student.student_id}")
    print(f"Evaluaciones:")
    for i, ev in enumerate(student.evaluations, 1):
        print(f"  Evaluacion {i}: Nota={ev.grade}, Peso={ev.weight}%")
    print(f"Asistencia minima: SI")

    # Configurar politicas
    attendance = AttendancePolicy(student.has_reached_minimum_attendance)
    extra_points = ExtraPointsPolicy([True, False, True])

    print(f"Politica puntos extra: Año 1=SI, Año 2=NO, Año 3=SI")
    print(f"Año academico actual: 2 (sin puntos extra)")

    # Calcular
    calculator = GradeCalculator(
        evaluations=student.evaluations,
        attendance_policy=attendance,
        extra_points_policy=extra_points,
        current_year_index=1,  # Año 2 (indice 1)
    )

    result = calculator.calculate_final_grade()

    # Mostrar resultado
    print("\nRESULTADO:")
    print(f"  Promedio Ponderado: {result.weighted_average:.2f}")
    print(
        f"  Penalizacion por Asistencia: {'SI' if result.attendance_penalty_applied else 'NO'}"
    )
    print(f"  Puntos Extra Aplicados: +{result.extra_points_applied:.2f}")
    print(f"  NOTA FINAL: {result.final_grade:.2f}")


def test_case_4():
    """Caso 4: Nota que se limita al maximo (20)"""
    print("CASO 4: Nota que alcanza el limite maximo")
    print("-" * 70)

    student = Student("U202099999", has_reached_minimum_attendance=True)

    # Agregar evaluaciones perfectas
    student.add_evaluation(Evaluation(20.0, 100.0))

    print(f"Estudiante: {student.student_id}")
    print(f"Evaluaciones:")
    for i, ev in enumerate(student.evaluations, 1):
        print(f"  Evaluacion {i}: Nota={ev.grade}, Peso={ev.weight}%")
    print(f"Asistencia minima: SI")

    # Configurar politicas
    attendance = AttendancePolicy(student.has_reached_minimum_attendance)
    extra_points = ExtraPointsPolicy([True])

    print(f"Politica puntos extra: Año 1=SI")
    print(f"Año academico actual: 1 (con puntos extra)")

    # Calcular
    calculator = GradeCalculator(
        evaluations=student.evaluations,
        attendance_policy=attendance,
        extra_points_policy=extra_points,
        current_year_index=0,
    )

    result = calculator.calculate_final_grade()

    # Mostrar resultado
    print("\nRESULTADO:")
    print(f"  Promedio Ponderado: {result.weighted_average:.2f}")
    print(
        f"  Penalizacion por Asistencia: {'SI' if result.attendance_penalty_applied else 'NO'}"
    )
    print(f"  Puntos Extra Aplicados: +{result.extra_points_applied:.2f}")
    print(
        f"  Nota calculada: {result.weighted_average + result.extra_points_applied:.2f}"
    )
    print(f"  NOTA FINAL (limitada a 20): {result.final_grade:.2f}")


def test_case_5():
    """Caso 5: Multiples evaluaciones (10 evaluaciones)"""
    print("CASO 5: Estudiante con 10 evaluaciones (maximo permitido)")
    print("-" * 70)

    student = Student("U202055555", has_reached_minimum_attendance=True)

    # Agregar 10 evaluaciones
    grades = [15, 16, 14, 17, 15, 18, 16, 15, 17, 16]
    weight_per_eval = 10.0  # 10% cada una para sumar 100%

    for grade in grades:
        student.add_evaluation(Evaluation(float(grade), weight_per_eval))

    print(f"Estudiante: {student.student_id}")
    print(f"Evaluaciones: {student.get_evaluation_count()}")
    for i, ev in enumerate(student.evaluations, 1):
        print(f"  Eval {i}: Nota={ev.grade}, Peso={ev.weight}%")
    print(f"Asistencia minima: SI")

    # Configurar politicas
    attendance = AttendancePolicy(student.has_reached_minimum_attendance)
    extra_points = ExtraPointsPolicy([False])

    print(f"Politica puntos extra: Año 1=NO")

    # Calcular
    calculator = GradeCalculator(
        evaluations=student.evaluations,
        attendance_policy=attendance,
        extra_points_policy=extra_points,
        current_year_index=0,
    )

    result = calculator.calculate_final_grade()

    # Mostrar resultado
    print("\nRESULTADO:")
    print(f"  Promedio Ponderado: {result.weighted_average:.2f}")
    print(
        f"  Penalizacion por Asistencia: {'SI' if result.attendance_penalty_applied else 'NO'}"
    )
    print(f"  Puntos Extra Aplicados: +{result.extra_points_applied:.2f}")
    print(f"  NOTA FINAL: {result.final_grade:.2f}")


def main():
    """Ejecutar todos los casos de prueba"""
    print("\n" + "=" * 70)
    print("CS-GradeCalculator - PRUEBAS MANUALES")
    print("=" * 70)

    test_case_1()
    print_separator()

    test_case_2()
    print_separator()

    test_case_3()
    print_separator()

    test_case_4()
    print_separator()

    test_case_5()
    print_separator()

    print("Todas las pruebas completadas exitosamente!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
