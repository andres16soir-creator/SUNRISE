@echo off
title INSTALADOR SISTEMA DENTISTA
color 0A
echo ========================================
echo    INSTALANDO SISTEMA DENTISTA
echo ========================================
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado.
    echo Descargalo desde: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python detectado

REM Crear entorno virtual "dent"
echo.
echo [1/5] Creando entorno virtual "dent"...
python -m venv dent
if errorlevel 1 (
    echo [ERROR] No se pudo crear el entorno virtual
    pause
    exit /b 1
)
echo [OK] Entorno virtual "dent" creado

REM Activar entorno
echo.
echo [2/5] Activando entorno...
call dent\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] No se pudo activar el entorno
    pause
    exit /b 1
)
echo [OK] Entorno activado

REM Actualizar pip
echo.
echo [3/5] Actualizando pip...
python -m pip install --upgrade pip >nul
echo [OK] Pip actualizado

REM Instalar dependencias desde requirements.txt
echo.
echo [4/5] Instalando dependencias...
if exist requirements.txt (
    echo Instalando desde requirements.txt...
    pip install -r requirements.txt
) else (
    echo [ERROR] No se encuentra requirements.txt
    echo Por favor, ejecuta primero: pip freeze ^> requirements.txt
    pause
    exit /b 1
)

if errorlevel 1 (
    echo [ERROR] Fallo la instalacion de dependencias
    pause
    exit /b 1
)
echo [OK] Dependencias instaladas correctamente

REM Configurar base de datos
echo.
echo [5/5] Configurando base de datos...
if exist db.sqlite3 (
    echo [OK] Base de datos SQLite encontrada
    echo Aplicando migraciones...
    python manage.py migrate
) else (
    echo [AVISO] No hay base de datos, creando nueva...
    python manage.py migrate
)

REM Recolectar archivos estaticos (si existe el comando)
echo.
echo Recolectando archivos estaticos...
python manage.py collectstatic --noinput >nul 2>&1
if errorlevel 1 (
    echo [AVISO] No se recolectaron estaticos (opcional)
) else (
    echo [OK] Archivos estaticos recolectados
)

REM Crear INICIAR.bat
echo.
echo Creando acceso directo INICIAR.bat...
(
echo @echo off
echo title SISTEMA DENTISTA
echo color 0A
echo echo ========================================
echo echo    INICIANDO SISTEMA DENTISTA
echo echo ========================================
echo echo.
echo echo Activando entorno...
echo call dent\Scripts\activate
echo echo.
echo echo Iniciando servidor...
echo echo.
echo python manage.py runserver
echo echo.
echo echo Servidor corriendo en: http://127.0.0.1:8000
echo echo Presiona CTRL+C para detener
echo pause
) > INICIAR.bat
echo [OK] Archivo INICIAR.bat creado

echo.
echo ========================================
echo    INSTALACION COMPLETADA CON EXITO
echo ========================================
echo.
echo Para iniciar el sistema:
echo ------------------------
echo 1. Hacer doble click en INICIAR.bat
echo 2. O manualmente:
echo    - Activar: dent\Scripts\activate
echo    - Ejecutar: python manage.py runserver
echo.
echo Acceso web: http://127.0.0.1:8000
echo.
pause