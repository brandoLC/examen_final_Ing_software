# Instrucciones para Configurar SonarQube

## Tus Credenciales

**Project Key**: `Backend-Student-32`
**Token**: `sqp_08f5db84cf96276ea79d7858ab47e661728bebe5`
**SonarQube URL**: `http://213.199.42.57:9002`

## Opcion 1: Configurar GitHub Actions (Recomendado)

### Paso 1: Agregar Secrets en GitHub

1. Ve a tu repositorio: https://github.com/brandoLC/examen_final_Ing_software
2. Click en **Settings** → **Secrets and variables** → **Actions**
3. Click en **New repository secret** y agrega:

**Secret 1:**
- Name: `SONAR_TOKEN`
- Secret: `sqp_08f5db84cf96276ea79d7858ab47e661728bebe5`
- Click **Add secret**

**Secret 2:**
- Name: `SONAR_HOST_URL`
- Secret: `http://213.199.42.57:9002`
- Click **Add secret**

### Paso 2: Hacer Push

```bash
git add .
git commit -m "Configurar SonarQube con GitHub Actions"
git push origin master
```

### Paso 3: Verificar

1. Ve a la pestaña **Actions** en GitHub
2. Espera a que termine el workflow (1-2 minutos)
3. Ve a http://213.199.42.57:9002 y busca tu proyecto "Backend-Student-32"

---

## Opcion 2: Analisis Local (Manual)

Si prefieres ejecutar el analisis desde tu computadora:

### Paso 1: Instalar SonarScanner

**Windows:**
1. Descarga: https://docs.sonarsource.com/sonarqube/latest/analyzing-source-code/scanners/sonarscanner/
2. Descomprime en `C:\sonar-scanner`
3. Agrega a PATH: `C:\sonar-scanner\bin`

**Linux/Mac:**
```bash
# Descargar
wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip
unzip sonar-scanner-cli-5.0.1.3006-linux.zip
sudo mv sonar-scanner-5.0.1.3006-linux /opt/sonar-scanner
sudo ln -s /opt/sonar-scanner/bin/sonar-scanner /usr/local/bin/sonar-scanner
```

### Paso 2: Ejecutar Tests con Cobertura

```bash
pytest --cov=src --cov-report=xml:coverage.xml
```

### Paso 3: Ejecutar SonarScanner

```bash
sonar-scanner \
  -Dsonar.projectKey=Backend-Student-32 \
  -Dsonar.sources=src \
  -Dsonar.host.url=http://213.199.42.57:9002 \
  -Dsonar.token=sqp_08f5db84cf96276ea79d7858ab47e661728bebe5
```

**Windows (PowerShell):**
```powershell
sonar-scanner `
  -Dsonar.projectKey=Backend-Student-32 `
  -Dsonar.sources=src `
  -Dsonar.host.url=http://213.199.42.57:9002 `
  -Dsonar.token=sqp_08f5db84cf96276ea79d7858ab47e661728bebe5
```

### Paso 4: Ver Resultados

Ve a: http://213.199.42.57:9002/dashboard?id=Backend-Student-32

---

## Que Analiza SonarQube

1. **Bugs**: Errores en el codigo
2. **Vulnerabilities**: Problemas de seguridad
3. **Code Smells**: Malas practicas
4. **Coverage**: Cobertura de tests (deberia ser ~99%)
5. **Duplications**: Codigo duplicado
6. **Maintainability**: Facilidad de mantenimiento
7. **Reliability**: Confiabilidad del codigo
8. **Security**: Nivel de seguridad

## Metricas Esperadas para tu Proyecto

- **Bugs**: 0
- **Vulnerabilities**: 0
- **Code Smells**: 0-5 (bajo)
- **Coverage**: 99%
- **Duplications**: 0%
- **Maintainability Rating**: A
- **Reliability Rating**: A
- **Security Rating**: A

## Ver tu Quality Profile

1. Accede a: http://213.199.42.57:9002
2. Busca "Backend-Student-32"
3. Podras ver:
   - Overview con las metricas principales
   - Issues (bugs, vulnerabilities, code smells)
   - Measures (metricas detalladas)
   - Code (codigo analizado)
   - Activity (historial de analisis)

## Troubleshooting

### Error: "Unauthorized"
- Verifica que el token sea correcto
- Verifica que el projectKey sea exactamente `Backend-Student-32`

### Error: "Project not found"
- El proyecto debe existir en SonarQube
- Si no existe, contacta al profesor para que lo cree

### No aparece la cobertura
- Asegurate de ejecutar `pytest --cov=src --cov-report=xml` antes
- Verifica que exista el archivo `coverage.xml`

### Windows: "sonar-scanner no se reconoce"
- Agrega SonarScanner al PATH
- O usa la ruta completa: `C:\sonar-scanner\bin\sonar-scanner.bat`

## IMPORTANTE

- NO compartas tu token publicamente
- NO lo subas a GitHub (ya esta en los Secrets)
- El analisis se ejecuta automaticamente en cada push si configuraste GitHub Actions
