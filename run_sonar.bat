@echo off
echo ==========================================
echo Ejecutando analisis de SonarQube
echo ==========================================
echo.
echo NOTA: Asegurese de tener SonarScanner instalado
echo y configurado en su PATH
echo.
echo Si no tiene SonarQube local, puede usar SonarCloud:
echo https://sonarcloud.io
echo.
sonar-scanner.bat
echo.
echo ==========================================
echo Analisis completado
echo ==========================================
pause
