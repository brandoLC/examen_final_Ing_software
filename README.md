# CS-GradeCalculator

Sistema de calculo de notas finales para docentes UTEC - Examen Final de Ingenieria de Software

## Descripcion

CS-GradeCalculator es un sistema modular diseñado para calcular las notas finales de estudiantes, considerando evaluaciones ponderadas, asistencia minima y politicas de puntos extra por consenso docente. Implementa el caso de uso CU001: Calcular nota final del estudiante.

## Arquitectura y Diseño

### Estructura del Proyecto

```
Examen_final/
├── src/
│   ├── __init__.py
│   ├── evaluation.py              # Clase Evaluation
│   ├── attendance_policy.py       # Clase AttendancePolicy
│   ├── extra_points_policy.py     # Clase ExtraPointsPolicy
│   ├── grade_calculator.py        # Clase GradeCalculator y GradeCalculationResult
│   └── student.py                 # Clase Student
├── tests/
│   ├── __init__.py
│   ├── test_evaluation.py
│   ├── test_attendance_policy.py
│   ├── test_extra_points_policy.py
│   ├── test_grade_calculator.py
│   └── test_student.py
├── main.py                        # Punto de entrada de la aplicacion
├── requirements.txt               # Dependencias del proyecto
├── pytest.ini                     # Configuracion de pytest
├── sonar-project.properties       # Configuracion de SonarQube
├── run_tests.bat                  # Script para ejecutar tests
└── README.md
```

### Clases Principales

#### 1. Evaluation
Representa una evaluacion individual con su nota y peso porcentual.

**Responsabilidades:**
- Validar notas (rango 0-20)
- Validar pesos porcentuales (rango 0-100)
- Calcular la contribucion ponderada de la evaluacion

**Constantes:**
- MIN_GRADE = 0.0
- MAX_GRADE = 20.0
- MIN_WEIGHT = 0.0
- MAX_WEIGHT = 100.0
- PERCENTAGE_DIVISOR = 100.0

#### 2. AttendancePolicy
Maneja la politica de asistencia y penalizaciones.

**Responsabilidades:**
- Verificar si el estudiante cumplio con la asistencia minima
- Aplicar penalizacion (nota = 0) si no cumple

**Constantes:**
- PENALTY_FOR_INSUFFICIENT_ATTENDANCE = 0.0

#### 3. ExtraPointsPolicy
Gestiona los puntos extra basados en consenso docente anual.

**Responsabilidades:**
- Almacenar decisiones de puntos extra por año academico
- Calcular puntos extra para un año especifico

**Constantes:**
- EXTRA_POINTS_VALUE = 1.0
- NO_EXTRA_POINTS = 0.0

#### 4. GradeCalculator
Calcula la nota final aplicando todas las politicas.

**Responsabilidades:**
- Validar evaluaciones (maximo 10, pesos suman 100%)
- Calcular promedio ponderado
- Aplicar penalizacion por asistencia
- Agregar puntos extra segun consenso
- Limitar nota final entre 0 y 20

**Constantes:**
- MAX_EVALUATIONS = 10
- WEIGHT_TOLERANCE = 0.01
- EXPECTED_TOTAL_WEIGHT = 100.0
- MIN_FINAL_GRADE = 0.0
- MAX_FINAL_GRADE = 20.0
- INITIAL_EXTRA_POINTS = 0.0

#### 5. GradeCalculationResult
Contiene el resultado detallado del calculo.

**Atributos:**
- weighted_average: Promedio ponderado
- attendance_penalty_applied: Si se aplico penalizacion
- extra_points_applied: Puntos extra agregados
- final_grade: Nota final

#### 6. Student
Representa a un estudiante con sus evaluaciones.

**Responsabilidades:**
- Gestionar identificacion del estudiante
- Administrar lista de evaluaciones (maximo 10)
- Controlar estado de asistencia

**Constantes:**
- MAX_EVALUATIONS = 10

## Requerimientos Funcionales (RF)

### RF01: Registro de Evaluaciones
Como docente podre registrar las evaluaciones de un estudiante indicando nota y peso porcentual.
- Implementado en: `Student.add_evaluation()`, `Evaluation.__init__()`

### RF02: Registro de Asistencia
Como docente podre registrar si el estudiante cumplio la asistencia minima.
- Implementado en: `Student.has_reached_minimum_attendance`, `AttendancePolicy.__init__()`

### RF03: Politica de Puntos Extra
Como docente podre registrar consenso de puntos extra por año academico.
- Implementado en: `ExtraPointsPolicy.__init__()`, `ExtraPointsPolicy.calculate_extra_points()`

### RF04: Calculo de Nota Final
Como docente podre solicitar el calculo de nota final.
- Implementado en: `GradeCalculator.calculate_final_grade()`

### RF05: Visualizacion de Detalle
Como docente podre visualizar el detalle del calculo.
- Implementado en: `GradeCalculationResult.get_details()`, `main.py (GradeCalculatorApp.calculate_and_display_grade)`

## Requerimientos No Funcionales (RNF)

### RNF01: Limite de Evaluaciones
Maximo 10 evaluaciones por estudiante.
- Validado en: `Student.add_evaluation()`, `GradeCalculator._validate_evaluations()`

### RNF02: Usuarios Concurrentes
Soporta hasta 50 usuarios concurrentes.
- El diseño stateless permite escalabilidad horizontal

### RNF03: Determinismo
El calculo debe ser deterministico: mismos datos = misma nota.
- Probado en: `test_grade_calculator.py::test_should_be_deterministic_with_same_inputs`

### RNF04: Tiempo de Calculo
Tiempo de calculo < 300ms.
- Complejidad: O(n) donde n es el numero de evaluaciones (max 10)

## Instalacion y Ejecucion

### Requisitos
- Python 3.8 o superior
- pip

### Instalacion de Dependencias

```bash
pip install -r requirements.txt
```

### Ejecutar la Aplicacion

```bash
python main.py
```

### Ejecutar Tests

```bash
# Ejecutar todos los tests con cobertura
pytest

# Ejecutar con reporte detallado
pytest -v

# En Windows usando el script batch
run_tests.bat
```

### Analisis de Codigo con SonarQube

1. Instalar SonarScanner: https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/
2. Configurar servidor SonarQube (local o SonarCloud)
3. Ejecutar analisis:

```bash
# En Windows
run_sonar.bat

# En Linux/Mac
sonar-scanner
```

## Calidad del Codigo

### Principios Aplicados

1. **Nombres Significativos**
   - No se usan nombres como x1, dato, aux, temp
   - Variables y metodos con nombres descriptivos

2. **Ausencia de Valores Magicos**
   - Todos los valores numericos estan definidos como constantes de clase
   - Ejemplos: MAX_EVALUATIONS, EXTRA_POINTS_VALUE, PERCENTAGE_DIVISOR

3. **Separacion de Responsabilidades**
   - Cada clase tiene una responsabilidad unica y clara
   - Bajo acoplamiento entre componentes

4. **Alta Cohesion**
   - Metodos relacionados agrupados logicamente
   - Validaciones encapsuladas

5. **Manejo de Errores**
   - Validaciones con mensajes descriptivos
   - Uso de excepciones apropiadas (ValueError)

### Cobertura de Tests

- **Cobertura Total: 99%**
- 79 tests unitarios
- Tests cubren:
  - Casos normales
  - Casos con asistencia insuficiente
  - Años con y sin puntos extra
  - Validaciones de limites (notas 0, 20, pesos invalidos)
  - Determinismo del calculo

### Metricas de Calidad

```
Name                         Stmts   Miss  Cover
--------------------------------------------------
src/__init__.py                  1      0   100%
src/attendance_policy.py        16      0   100%
src/evaluation.py               31      0   100%
src/extra_points_policy.py      25      0   100%
src/grade_calculator.py         54      1    98%
src/student.py                  40      0   100%
--------------------------------------------------
TOTAL                          167      1    99%
```

## Ejemplo de Uso

```python
from src.student import Student
from src.evaluation import Evaluation
from src.attendance_policy import AttendancePolicy
from src.extra_points_policy import ExtraPointsPolicy
from src.grade_calculator import GradeCalculator

# Crear estudiante
student = Student("U202012345", has_reached_minimum_attendance=True)

# Agregar evaluaciones
student.add_evaluation(Evaluation(16.0, 30.0))  # Parcial 1: 16/20, 30%
student.add_evaluation(Evaluation(14.0, 40.0))  # Parcial 2: 14/20, 40%
student.add_evaluation(Evaluation(18.0, 30.0))  # Final: 18/20, 30%

# Configurar politicas
attendance = AttendancePolicy(student.has_reached_minimum_attendance)
extra_points = ExtraPointsPolicy([True, False, True])  # 3 años, año actual: 0

# Calcular nota final
calculator = GradeCalculator(
    evaluations=student.evaluations,
    attendance_policy=attendance,
    extra_points_policy=extra_points,
    current_year_index=0
)

result = calculator.calculate_final_grade()

# Mostrar resultado
print(f"Promedio Ponderado: {result.weighted_average:.2f}")
print(f"Puntos Extra: +{result.extra_points_applied:.2f}")
print(f"Nota Final: {result.final_grade:.2f}")

# Output:
# Promedio Ponderado: 16.00
# Puntos Extra: +1.00
# Nota Final: 17.00
```

## Flujo de Calculo

```
1. Validar evaluaciones
   └─ Maximo 10 evaluaciones
   └─ Pesos suman 100% (tolerancia 0.01)

2. Calcular promedio ponderado
   └─ Σ (nota × peso / 100)

3. Aplicar politica de asistencia
   └─ Si no cumple asistencia → nota = 0
   └─ Si cumple → mantener promedio

4. Aplicar politica de puntos extra
   └─ Si asistencia OK y consenso del año → +1 punto
   └─ Si no → +0 puntos

5. Limitar resultado
   └─ min(max(nota_final, 0), 20)
```

## Decisiones de Diseño

### 1. Uso de Clases Separadas para Politicas
- **Razon**: Facilita testing y extension futura
- **Beneficio**: Bajo acoplamiento, alta cohesion

### 2. Validacion en Constructor
- **Razon**: Fail-fast, evita estados invalidos
- **Beneficio**: Garantiza integridad desde la creacion

### 3. Propiedades de Solo Lectura
- **Razon**: Inmutabilidad de datos criticos
- **Beneficio**: Previene modificaciones accidentales

### 4. Constantes de Clase
- **Razon**: Evitar valores magicos, facilitar mantenimiento
- **Beneficio**: Codigo mas legible y configurable

### 5. Resultado como Objeto
- **Razon**: Encapsular multiples valores de retorno
- **Beneficio**: API clara y extensible

## Autores

- Desarrollado como proyecto del Examen Final de Ingenieria de Software
- Universidad de Ingenieria y Tecnologia (UTEC)

## Licencia

Proyecto academico - UTEC 2025

## Quality Gate

[![Quality Gate](http://213.199.42.57:9002/api/project_badges/measure?project=Backend-Student-32&metric=alert_status)](http://213.199.42.57:9002/dashboard?id=Backend-Student-32)
