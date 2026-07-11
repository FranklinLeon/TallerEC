@echo off
echo.
echo  TallerEC - Iniciando servicios...
echo.

echo [1/2] Levantando Docker (db + core + ai_service)...
docker-compose up -d
if errorlevel 1 (
    echo ERROR: Docker no pudo levantar. Asegurate de que Docker Desktop este corriendo.
    pause
    exit /b 1
)

echo.
echo [2/2] Iniciando servidor frontend...
echo.
cd frontend
npm run dev
