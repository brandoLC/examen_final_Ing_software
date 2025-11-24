# Configuracion de SonarQube con GitHub Actions

Este documento explica como configurar SonarQube para analizar automaticamente el codigo cada vez que hagas push a GitHub.

## Paso 1: Obtener el Token de SonarQube

1. Inicia sesion en SonarQube: http://213.199.42.57:9002
2. Haz clic en tu perfil (arriba a la derecha)
3. Ve a **My Account** → **Security**
4. En la seccion **Generate Tokens**:
   - Ingresa un nombre para el token (ejemplo: "GitHub Actions")
   - Selecciona el tipo: **Project Analysis Token** o **Global Analysis Token**
   - Haz clic en **Generate**
5. **IMPORTANTE**: Copia el token inmediatamente (solo se muestra una vez)

## Paso 2: Configurar Secrets en GitHub

1. Ve a tu repositorio en GitHub: https://github.com/brandoLC/examen_final_Ing_software

2. Haz clic en **Settings** (Configuracion) en la parte superior

3. En el menu lateral izquierdo:
   - Busca **Secrets and variables**
   - Haz clic en **Actions**

4. Crear el primer secret (SONAR_TOKEN):
   - Haz clic en **New repository secret**
   - **Name**: `SONAR_TOKEN`
   - **Secret**: Pega el token que copiaste de SonarQube
   - Haz clic en **Add secret**

5. Crear el segundo secret (SONAR_HOST_URL):
   - Haz clic en **New repository secret**
   - **Name**: `SONAR_HOST_URL`
   - **Secret**: `http://213.199.42.57:9002`
   - Haz clic en **Add secret**

## Paso 3: Crear el Proyecto en SonarQube (Si no existe)

1. En SonarQube, ve a **Projects** → **Create Project**
2. Selecciona **Manually**
3. Ingresa:
   - **Project key**: `brandoLC_examen_final_Ing_software`
   - **Display name**: `CS-GradeCalculator`
4. Haz clic en **Set Up**

## Paso 4: Subir los Archivos de Configuracion

Los archivos ya estan creados en tu proyecto:
- `.github/workflows/sonarqube.yml` - Workflow de GitHub Actions
- `sonar-project.properties` - Configuracion de SonarQube

Solo necesitas hacer commit y push:

```bash
git add .github/workflows/sonarqube.yml
git add sonar-project.properties
git commit -m "Agregar configuracion de SonarQube con GitHub Actions"
git push origin master
```

## Paso 5: Verificar que Funciona

1. Despues del push, ve a tu repositorio en GitHub
2. Haz clic en la pestaña **Actions**
3. Deberias ver el workflow "SonarQube Analysis" ejecutandose
4. Espera a que termine (puede tardar 1-2 minutos)
5. Si todo esta bien, veras un check verde
6. Ve a SonarQube (http://213.199.42.57:9002) para ver el analisis

## Que Hace el Workflow Automaticamente

Cada vez que hagas push a la rama `master`:

1. Descarga el codigo
2. Instala Python 3.11
3. Instala las dependencias (pytest, pytest-cov)
4. Ejecuta los tests con cobertura
5. Genera el reporte de cobertura en XML
6. Envia todo a SonarQube para analisis
7. SonarQube analiza:
   - Calidad del codigo
   - Code smells
   - Bugs potenciales
   - Vulnerabilidades de seguridad
   - Cobertura de tests
   - Duplicacion de codigo

## Troubleshooting

### Error: "Could not find a default branch"
- Asegurate de tener al menos un commit en la rama master

### Error: "Invalid token"
- Verifica que el SONAR_TOKEN en GitHub Secrets sea correcto
- Genera un nuevo token en SonarQube si es necesario

### Error: "Project not found"
- Verifica que el projectKey en sonar-project.properties coincida con el proyecto en SonarQube
- Crea el proyecto manualmente en SonarQube si no existe

### El workflow no se ejecuta
- Verifica que el archivo este en `.github/workflows/sonarqube.yml`
- Asegurate de haber hecho push del archivo

## Ver Resultados

### En GitHub:
- Ve a la pestaña **Actions** para ver el estado de los workflows

### En SonarQube:
- Ve a http://213.199.42.57:9002
- Busca tu proyecto "CS-GradeCalculator"
- Veras metricas como:
  - Bugs: 0
  - Vulnerabilities: 0
  - Code Smells: X
  - Coverage: 99%
  - Duplications: 0%

## Notas Importantes

- El analisis se ejecuta automaticamente en cada push a master
- Tambien se ejecuta en pull requests
- Los resultados se guardan en el historial de SonarQube
- Puedes ver la evolucion de la calidad del codigo en el tiempo
