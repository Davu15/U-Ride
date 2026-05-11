@echo off
REM Script para configurar U-Ride en Windows

setlocal enabledelayedexpansion

echo.
echo ============================================
echo    INSTALADOR U-RIDE PARA WINDOWS
echo ============================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no está instalado o no está en PATH
    echo Descargalo desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python detectado

REM Crear entorno virtual si no existe
if not exist "venv" (
    echo.
    echo [*] Creando entorno virtual...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] No se pudo crear el entorno virtual
        pause
        exit /b 1
    )
    echo [OK] Entorno virtual creado
) else (
    echo [OK] Entorno virtual ya existe
)

REM Activar entorno virtual
echo.
echo [*] Activando entorno virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] No se pudo activar el entorno virtual
    pause
    exit /b 1
)
echo [OK] Entorno virtual activado

REM Actualizar pip
echo.
echo [*] Actualizando pip...
python -m pip install --upgrade pip --quiet
if errorlevel 1 (
    echo [ADVERTENCIA] Hubo un problema actualizando pip, continuando...
)

REM Instalar dependencias
echo.
echo [*] Instalando dependencias de requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] No se pudieron instalar las dependencias
    pause
    exit /b 1
)
echo [OK] Dependencias instaladas

REM Verificar Django
echo.
echo [*] Verificando Django...
python -m django --version
if errorlevel 1 (
    echo [ERROR] Django no se instaló correctamente
    pause
    exit /b 1
)
echo [OK] Django está instalado

REM Copiar .env
echo.
if not exist ".env" (
    echo [*] Creando archivo .env...
    copy .env.example .env
    if errorlevel 1 (
        echo [ERROR] No se pudo copiar .env.example
        pause
        exit /b 1
    )
    echo [OK] Archivo .env creado
    echo [!] IMPORTANTE: Edita .env con tu contraseña de MySQL
    echo.
    pause
) else (
    echo [OK] Archivo .env ya existe
)

REM Opción de editar .env
echo.
set /p EDIT_ENV="Deseas editar .env ahora? (s/n): "
if /i "!EDIT_ENV!"=="s" (
    notepad .env
)

REM Ejecutar migraciones
echo.
echo [*] Ejecutando migraciones...
python manage.py makemigrations
if errorlevel 1 (
    echo [ERROR] Error en makemigrations
    pause
    exit /b 1
)

python manage.py migrate
if errorlevel 1 (
    echo [ERROR] Error en migrate
    pause
    exit /b 1
)
echo [OK] Migraciones completadas

REM Crear superusuario
echo.
set /p CREATE_ADMIN="Deseas crear superusuario ahora? (s/n): "
if /i "!CREATE_ADMIN!"=="s" (
    python manage.py createsuperuser
)

REM Ejecutar servidor
echo.
set /p RUN_SERVER="Deseas ejecutar el servidor ahora? (s/n): "
if /i "!RUN_SERVER!"=="s" (
    echo.
    echo ============================================
    echo    Servidor iniciado en http://localhost:8000
    echo    Panel Admin: http://localhost:8000/admin/
    echo    Presiona CTRL+C para detener
    echo ============================================
    echo.
    python manage.py runserver
) else (
    echo.
    echo Para ejecutar el servidor manualmente:
    echo.
    echo   1. Abre una nueva terminal en este directorio
    echo   2. Ejecuta: venv\Scripts\activate
    echo   3. Ejecuta: python manage.py runserver
    echo.
)

pause
