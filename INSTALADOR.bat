@echo off
title INSTALADOR SISTEMA DENTAL SUNRISE
color 0A
echo ===========================================
echo    SISTEMA DENTAL SUNRISE
echo    PROPIEDAD DE: Andres Emanuel Terrazas Rios
echo    PROHIBIDA SU COPIA O DISTRIBUCION
echo ===========================================
echo.

REM Verificar si ya esta instalado
if exist "instalado.ini" (
    cls
    echo ===========================================
    echo    SISTEMA YA INSTALADO ANTERIORMENTE
    echo ===========================================
    echo.
    echo El sistema ya fue activado en esta computadora
    echo.
    echo Iniciando sistema...
    echo.
    call dent\Scripts\activate.bat 2>nul
    python manage.py runserver
    pause
    exit /b 0
)

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado.
    echo.
    echo Descargar desde: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python detectado
echo.

REM === SISTEMA DE ACTIVACION ===
echo ===== ACTIVACION DE LICENCIA =====
echo.
echo Este sistema requiere codigo de activacion
echo para la primera instalacion.
echo.

:VALIDAR_CODIGO
echo Codigos de contacto:
echo - Andres Emanuel Terrazas Rios
echo - Email: andres16soir@gmail.com
echo - Telefono: 69764651
echo.
echo.
set /p "CODIGO=Ingrese codigo de activacion: "

REM Ejecutar validacion con Python
python -c "
import sys
from pathlib import Path
sys.path.append(r'%cd%\SUNRISE')
from codigo_instalacion import CodigoInstalacion
codigo_manager = CodigoInstalacion()
if codigo_manager.verificar_codigo('%CODIGO%'):
    print('OK')
    sys.exit(0)
else:
    print('NO')
    sys.exit(1)
" > temp.txt
set /p RESULT=<temp.txt
del temp.txt

if "%RESULT%"=="OK" goto CODIGO_VALIDO

echo.
echo [ERROR] Codigo de activacion incorrecto
echo.
echo Para obtener un codigo valido, contacte al propietario:
echo Email: andres16soir@gmail.com
echo Telefono: 69764651
echo.
choice /C RN /M "¿Reintentar (R) o Cancelar (N)?"
if errorlevel 2 exit /b
if errorlevel 1 goto VALIDAR_CODIGO

:CODIGO_VALIDO
echo.
echo [OK] Codigo aceptado. Activando licencia...
echo.

REM Marcar como instalado usando el script
python -c "
from pathlib import Path
import sys
sys.path.append(r'%cd%\SUNRISE')
from codigo_instalacion import CodigoInstalacion
codigo_manager = CodigoInstalacion()
codigo_manager.marcar_instalado()
print('✅ Sistema activado permanentemente')
"

REM Esperar 2 segundos
timeout /t 2 /nobreak >nul

REM === INSTALACION NORMAL ===
echo.
echo ===== INSTALANDO COMPONENTES =====
echo.

REM Crear entorno virtual
echo [1/4] Creando entorno virtual...
python -m venv dent
if errorlevel 1 (
    echo [ERROR] No se pudo crear el entorno virtual
    pause
    exit /b 1
)
echo [OK] Entorno virtual creado

REM Activar entorno
call dent\Scripts\activate.bat

REM Instalar dependencias
echo.
echo [2/4] Instalando dependencias...
if exist requirements.txt (
    pip install -r requirements.txt
) else (
    echo [AVISO] Generando requirements.txt...
    pip freeze > requirements.txt
    pip install -r requirements.txt
)
echo [OK] Dependencias instaladas

REM Configurar base de datos
echo.
echo [3/4] Configurando base de datos...
python manage.py migrate
echo [OK] Base de datos configurada

REM Crear usuario administrador
echo.
echo [4/4] Creando usuario administrador...
echo.
echo ===== CREAR CUENTA DE ACCESO =====
echo.
echo Debes crear un usuario para acceder al sistema
echo.
python manage.py createsuperuser

if errorlevel 1 (
    echo.
    echo [ADVERTENCIA] No se pudo crear el usuario
    echo Puedes crearlo manualmente despues con:
    echo python manage.py createsuperuser
    pause
)

echo.
echo ===========================================
echo    INSTALACION COMPLETADA CON EXITO
echo ===========================================
echo.
echo PROPIEDAD DE: Andres Emanuel Terrazas Rios
echo Contacto: 69764651 / andres16soir@gmail.com
echo.
echo Resumen:
echo - Activacion: COMPLETADA (codigo validado)
echo - Licencia: PERMANENTE en este equipo
echo - Usuario: Creado exitosamente
echo.
echo Para iniciar sesion:
echo 1. Ejecutar INICIAR.bat
echo 2. Ir a: http://127.0.0.1:8000
echo 3. Usar credenciales creadas
echo.
echo NOTA: No podras instalar en otro equipo
echo sin un nuevo codigo de activacion.
echo.
pause