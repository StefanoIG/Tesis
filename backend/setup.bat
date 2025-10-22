@echo off
echo ================================
echo Setup del Backend - Trazabilidad
echo ================================
echo.

echo [1] Creando entorno virtual...
python -m venv venv

echo [2] Activando entorno virtual...
call venv\Scripts\activate.bat

echo [3] Actualizando pip...
python -m pip install --upgrade pip

echo [4] Instalando dependencias...
pip install -r requirements.txt

echo.
echo [5] Haciendo migraciones iniciales...
python manage.py makemigrations

echo [6] Ejecutando migraciones...
python manage.py migrate

echo.
echo [7] Creando superusuario...
echo Ingresa los datos para el superusuario:
python manage.py createsuperuser

echo.
echo ================================
echo Setup completado exitosamente!
echo ================================
echo.
echo Para iniciar el servidor, ejecuta:
echo   call venv\Scripts\activate.bat
echo   python manage.py runserver
echo.
echo Accede a:
echo   - Admin: http://localhost:8000/admin
echo   - Swagger: http://localhost:8000/api/docs
echo   - ReDoc: http://localhost:8000/api/redoc
echo.
pause
