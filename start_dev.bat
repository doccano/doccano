@echo off
:: filepath: /Users/frankfurt/Documents/ualg/les/doccano/start_dev.bat
setlocal EnableDelayedExpansion

:: Script to start doccano development environment on Windows

:: Directory paths
set ROOT_DIR=%~dp0
set ROOT_DIR=%ROOT_DIR:~0,-1%
set FRONTEND_DIR=%ROOT_DIR%\frontend
set BACKEND_DIR=%ROOT_DIR%\backend

echo === Starting Doccano Development Environment ===
echo Root directory: %ROOT_DIR%
echo Frontend directory: %FRONTEND_DIR%
echo Backend directory: %BACKEND_DIR%
echo.

:: Load environment variables from .env file if it exists
if exist "%ROOT_DIR%\.env" (
    echo Loading environment variables from %ROOT_DIR%\.env
    for /f "tokens=*" %%a in (%ROOT_DIR%\.env) do (
        set %%a
    )
) else if exist "%BACKEND_DIR%\.env" (
    echo Loading environment variables from %BACKEND_DIR%\.env
    for /f "tokens=*" %%a in (%BACKEND_DIR%\.env) do (
        set %%a
    )
)

:: Start backend first
echo Starting backend services...
cd "%BACKEND_DIR%" || (
    echo Error: Backend directory not found
    exit /b 1
)

:: Check if poetry is installed
where poetry >nul 2>&1 || (
    echo Error: Poetry is not installed or not in PATH
    exit /b 1
)

:: Check Python version in the Poetry environment
for /f "tokens=*" %%i in ('poetry run python --version 2^>^&1') do (
    set PYTHON_VERSION=%%i
)
echo Using Python: %PYTHON_VERSION%

:: Check if setuptools/pkg_resources is installed in the poetry environment
poetry run python -c "import pkg_resources" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Warning: pkg_resources module not found. Installing setuptools...
    
    :: Try to install a compatible version of setuptools based on Python version
    echo %PYTHON_VERSION% | findstr "3.8." >nul
    if %ERRORLEVEL% equ 0 (
        echo Python 3.8 detected, using setuptools^<80.0.0
        poetry add setuptools^<80.0.0
    ) else (
        echo %PYTHON_VERSION% | findstr "3.9. 3.10. 3.11." >nul
        if %ERRORLEVEL% equ 0 (
            echo Python 3.9+ detected, using latest setuptools
            poetry add setuptools
        ) else (
            echo Trying setuptools with relaxed version constraints...
            poetry add setuptools^<81.0.0
            if %ERRORLEVEL% neq 0 (
                echo ERROR: Failed to install setuptools.
                echo Please run setup.bat to properly configure the environment.
                exit /b 1
            )
        )
    )
)

:: Set database environment variable for PostgreSQL if not already set
if "%DATABASE_URL%"=="" (
    echo DATABASE_URL not found in environment. Setting default...
    set DATABASE_URL=postgres://doccano_admin:doccano_pass@localhost:5432/doccano?sslmode=disable
)
echo DATABASE_URL set to: %DATABASE_URL%

:: Ensure the database is migrated before starting the server
echo Running database migrations...
poetry run python manage.py migrate

:: Start Django server first
echo Starting Django development server...
start "Django Server" cmd /c "poetry run python manage.py runserver"
echo Django server started

:: Wait a moment for Django to fully start
echo Waiting for Django server to initialize (5 seconds)...
timeout /t 5 /nobreak > nul

:: Check if Django is actually running
curl -s http://127.0.0.1:8000/ >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Django server failed to start properly.
    echo Check if port 8000 is already in use or if there's a database connection issue.
    exit /b 1
)

:: Start Celery worker
echo Starting Celery worker...
start "Celery Worker" cmd /c "set DATABASE_URL=%DATABASE_URL% && poetry run celery --app=config worker --loglevel=INFO --concurrency=1"
echo Celery worker started

:: Now start the frontend after the backend is confirmed running
echo Starting frontend...
cd "%FRONTEND_DIR%" || (
    echo Error: Frontend directory not found
    exit /b 1
)

start "Frontend" cmd /c "yarn dev"
echo Frontend started
echo.

echo.
echo === All services started ===
echo Backend API: http://127.0.0.1:8000/
echo Frontend UI: http://localhost:3000/
echo Close the terminal windows to stop the services
echo.

:: Keep this window open until user closes it
echo Press Ctrl+C to exit this window (services will continue running in their own windows)
pause > nul
exit /b 0