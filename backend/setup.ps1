# Setup del Backend - Trazabilidad Agroindustrial
# Script para PowerShell

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Setup del Backend - Trazabilidad" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1] Creando entorno virtual..." -ForegroundColor Yellow
python -m venv venv

Write-Host "[2] Activando entorno virtual..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

Write-Host "[3] Actualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

Write-Host "[4] Instalando dependencias..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host ""
Write-Host "[5] Haciendo migraciones iniciales..." -ForegroundColor Yellow
python manage.py makemigrations

Write-Host "[6] Ejecutando migraciones..." -ForegroundColor Yellow
python manage.py migrate

Write-Host ""
Write-Host "[7] Creando superusuario..." -ForegroundColor Yellow
Write-Host "Ingresa los datos para el superusuario:" -ForegroundColor Green
python manage.py createsuperuser

Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "Setup completado exitosamente!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""
Write-Host "Para iniciar el servidor, ejecuta:" -ForegroundColor Cyan
Write-Host "  . .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "  python manage.py runserver" -ForegroundColor White
Write-Host ""
Write-Host "Accede a:" -ForegroundColor Cyan
Write-Host "  - Admin: http://localhost:8000/admin" -ForegroundColor White
Write-Host "  - Swagger: http://localhost:8000/api/docs" -ForegroundColor White
Write-Host "  - ReDoc: http://localhost:8000/api/redoc" -ForegroundColor White
Write-Host ""
