@echo off
:: filepath: /Users/frankfurt/Documents/ualg/les/doccano/setup.bat
setlocal EnableDelayedExpansion

:: Script to set up doccano development environment on Windows
:: This script installs all dependencies and can start the dev environment

:: Directory paths
set ROOT_DIR=%~dp0
set ROOT_DIR=%ROOT_DIR:~0,-1%
set FRONTEND_DIR=%ROOT_DIR%\frontend
set BACKEND_DIR=%ROOT_DIR%\backend

echo === Doccano Development Environment Setup ===
echo Root directory: %ROOT_DIR%
echo.

:: Check prerequisites
echo Checking prerequisites...

where git >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: git is not installed or not in PATH
    exit /b 1
)

:: Check for Python 3.9 or 3.10
set PYTHON_CMD=
where python3.10 >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set PYTHON_CMD=python3.10
) else (
    where python3.9 >nul 2>&1
    if %ERRORLEVEL% equ 0 (
        set PYTHON_CMD=python3.9
    ) else (
        where python >nul 2>&1
        if %ERRORLEVEL% equ 0 (
            for /f "tokens=*" %%i in ('python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"') do (
                set PY_VERSION=%%i
                if "!PY_VERSION!" == "3.10" (
                    set PYTHON_CMD=python
                ) else if "!PY_VERSION!" == "3.9" (
                    set PYTHON_CMD=python
                )
            )
        )
        
        if "!PYTHON_CMD!" == "" (
            where python3 >nul 2>&1
            if %ERRORLEVEL% equ 0 (
                for /f "tokens=*" %%i in ('python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"') do (
                    set PY_VERSION=%%i
                    if "!PY_VERSION!" == "3.10" (
                        set PYTHON_CMD=python3
                    ) else if "!PY_VERSION!" == "3.9" (
                        set PYTHON_CMD=python3
                    )
                )
            )
        )
    )
)

if "%PYTHON_CMD%" == "" (
    echo Error: Python 3.9 or 3.10 is not installed or not in PATH
    echo Checked commands: python3.10, python3.9, python, python3
    echo Please install Python 3.9 or 3.10: https://www.python.org/downloads/
    exit /b 1
)

for /f "tokens=*" %%i in ('where %PYTHON_CMD%') do set PYTHON_PATH=%%i
for /f "tokens=*" %%i in ('%PYTHON_CMD% -c "import sys; print(f\"Python {sys.version_info.major}.{sys.version_info.minor}\")"') do set PYTHON_VER=%%i
echo Found %PYTHON_VER%: %PYTHON_PATH%

where poetry >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Poetry is not installed or not in PATH
    echo Please install Poetry: https://python-poetry.org/docs/#installation
    exit /b 1
)

where yarn >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Yarn is not installed or not in PATH
    echo Please install Yarn: https://yarnpkg.com/getting-started/install
    exit /b 1
)

:: Set up backend
echo Setting up backend...
cd "%BACKEND_DIR%" || (
    echo Error: Backend directory not found
    exit /b 1
)
echo Configuring Poetry to use Python 3.10...
poetry env use %PYTHON_PATH%

:: Update Python version in pyproject.toml to match setuptools requirements
echo Updating Python version in pyproject.toml...
if exist pyproject.toml (
    :: Check if we need to modify the Python version constraint
    findstr /C:"python = \"^3.8\"" pyproject.toml >nul
    if %ERRORLEVEL% equ 0 (
        echo Updating Python version constraint from 3.8 to 3.9...
        powershell -Command "(Get-Content pyproject.toml) -replace 'python = \"\^3.8\"', 'python = \"^3.9\"' | Set-Content pyproject.toml"
    )
    findstr /C:"python = \">=3.8,<4.0\"" pyproject.toml >nul
    if %ERRORLEVEL% equ 0 (
        echo Updating Python version constraint from 3.8 to 3.9...
        powershell -Command "(Get-Content pyproject.toml) -replace 'python = \">=3.8,<4.0\"', 'python = \">=3.9,<4.0\"' | Set-Content pyproject.toml"
    )
)

:: Ensure setuptools is installed with a compatible version
echo Installing setuptools to provide pkg_resources module...
poetry add setuptools
if %ERRORLEVEL% neq 0 (
    echo Failed to install latest setuptools. Trying with a version compatible with Python 3.9+...
    poetry add setuptools^<81.0.0
    if %ERRORLEVEL% neq 0 (
        echo ERROR: Failed to install setuptools.
        echo Please make sure you're using Python 3.9+ and try running setup.bat again.
        exit /b 1
    )
)

:: Install PostgreSQL adapter (inside backend directory)
echo Installing PostgreSQL adapter (psycopg2-binary)...
poetry add psycopg2-binary
if %ERRORLEVEL% neq 0 (
    echo Failed to install psycopg2-binary through Poetry.
    echo Trying direct pip installation...
    poetry run pip install psycopg2-binary
    if %ERRORLEVEL% neq 0 (
        echo ERROR: Failed to install psycopg2-binary.
        echo Please make sure you have PostgreSQL development libraries installed.
        echo On Windows: Install PostgreSQL and make sure its bin directory is in PATH
        exit /b 1
    )
)

echo Installing Python dependencies with Poetry...
poetry install
echo Backend dependencies installed successfully.

:: Initialize Django database
echo.
echo === Initializing Django Database ===
echo Running database migrations...
poetry run python manage.py migrate

echo Creating user roles...
poetry run python manage.py create_roles

echo Creating admin user...
poetry run python manage.py create_admin --noinput --username "admin" --email "admin@example.com" --password "password"
echo Admin user created with username: admin and password: password
echo Database initialization completed successfully.
echo.

:: Set up frontend
echo Setting up frontend...
cd "%FRONTEND_DIR%" || (
    echo Error: Frontend directory not found
    exit /b 1
)
echo Installing JavaScript dependencies with Yarn...
yarn install
echo Frontend dependencies installed successfully.
echo.

cd "%ROOT_DIR%" || exit /b

:: Database setup function
:setup_postgres
echo.
echo === PostgreSQL Database Setup ===

:: Check if psql is installed
where psql >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: PostgreSQL client (psql) is not installed or not in PATH
    echo Please install PostgreSQL: https://www.postgresql.org/download/
    goto end_postgres
)

echo PostgreSQL client found: %psql%

:: Check if PostgreSQL server is running
pg_isready >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: PostgreSQL server is not running
    echo Please start your PostgreSQL server
    goto end_postgres
)

echo PostgreSQL server is running

:: Default values
set PG_USER=doccano_admin
set PG_PASS=doccano_pass
set PG_DB=doccano
set PG_HOST=localhost
set PG_PORT=5432

echo Setting up PostgreSQL database with the following configuration:
echo   Host: %PG_HOST%:%PG_PORT%
echo   Database: %PG_DB%
echo   User: %PG_USER%
echo   Password: %PG_PASS%
echo.

:: Ask for confirmation
set /p CONFIRM=Continue with these settings? (y/n):
if /i "%CONFIRM%" neq "y" (
    echo Database setup cancelled
    goto end_postgres
)

:: Create user if it doesn't exist
echo Creating user %PG_USER% if it doesn't exist...
psql -h %PG_HOST% -p %PG_PORT% -c "SELECT 1 FROM pg_roles WHERE rolname='%PG_USER%'" | findstr 1 >nul
if %ERRORLEVEL% neq 0 (
    psql -h %PG_HOST% -p %PG_PORT% -c "CREATE USER %PG_USER% WITH PASSWORD '%PG_PASS%';"
    if %ERRORLEVEL% neq 0 (
        echo Error: Failed to create user %PG_USER%
        goto end_postgres
    )
    echo User %PG_USER% created successfully
) else (
    echo User %PG_USER% already exists
)

:: Grant privileges to user
echo Granting necessary privileges to %PG_USER%...
psql -h %PG_HOST% -p %PG_PORT% -c "ALTER USER %PG_USER% WITH CREATEDB;"
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to grant CREATEDB privilege to %PG_USER%
    goto end_postgres
)

:: Create database if it doesn't exist
echo Creating database %PG_DB% if it doesn't exist...
psql -h %PG_HOST% -p %PG_PORT% -c "SELECT 1 FROM pg_database WHERE datname='%PG_DB%'" | findstr 1 >nul
if %ERRORLEVEL% neq 0 (
    psql -h %PG_HOST% -p %PG_PORT% -c "CREATE DATABASE %PG_DB% OWNER %PG_USER%;"
    if %ERRORLEVEL% neq 0 (
        echo Error: Failed to create database %PG_DB%
        goto end_postgres
    )
    echo Database %PG_DB% created successfully
) else (
    echo Database %PG_DB% already exists
    
    :: Ensure the existing database is owned by our user
    psql -h %PG_HOST% -p %PG_PORT% -c "ALTER DATABASE %PG_DB% OWNER TO %PG_USER%;"
    if %ERRORLEVEL% neq 0 (
        echo Warning: Failed to change ownership of existing database %PG_DB%
    )
)

:: Grant privileges on database
echo Granting all privileges on database %PG_DB% to %PG_USER%...
psql -h %PG_HOST% -p %PG_PORT% -c "GRANT ALL PRIVILEGES ON DATABASE %PG_DB% TO %PG_USER%;"
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to grant privileges on %PG_DB% to %PG_USER%
    goto end_postgres
)

echo PostgreSQL database setup completed successfully
echo Connection URL: postgres://%PG_USER%:%PG_PASS%@%PG_HOST%:%PG_PORT%/%PG_DB%?sslmode=disable
echo.

:: Store the config in a .env file
echo DATABASE_URL=postgres://%PG_USER%:%PG_PASS%@%PG_HOST%:%PG_PORT%/%PG_DB%?sslmode=disable> "%ROOT_DIR%\.env"
echo Database configuration saved to %ROOT_DIR%\.env

:: Create a .env file also in the backend directory for direct access
echo DATABASE_URL=postgres://%PG_USER%:%PG_PASS%@%PG_HOST%:%PG_PORT%/%PG_DB%?sslmode=disable> "%BACKEND_DIR%\.env"
echo Database configuration also saved to %BACKEND_DIR%\.env

:end_postgres
goto continue_setup

:: Docker PostgreSQL setup function
:show_docker_command
echo.
echo === PostgreSQL Docker Setup Command ===
echo To set up PostgreSQL in a Docker container, run:
echo.
echo docker run -d ^
echo   --name doccano-postgres ^
echo   -e POSTGRES_USER=doccano_admin ^
echo   -e POSTGRES_PASSWORD=doccano_pass ^
echo   -e POSTGRES_DB=doccano ^
echo   -v doccano-db:/var/lib/postgresql/data ^
echo   -p 5432:5432 ^
echo   postgres:13.8-alpine
echo.
echo After running the container, press any key to continue setup...
echo.
pause > nul
:: After showing the command and waiting for user to run it, save the connection info
echo DATABASE_URL=postgres://doccano_admin:doccano_pass@localhost:5432/doccano?sslmode=disable> "%ROOT_DIR%\.env"
echo DATABASE_URL=postgres://doccano_admin:doccano_pass@localhost:5432/doccano?sslmode=disable> "%BACKEND_DIR%\.env"
echo Database configuration saved to %ROOT_DIR%\.env and %BACKEND_DIR%\.env
goto continue_setup

:continue_setup
:: Ask about database setup
echo.
echo === Database Configuration ===
echo How would you like to set up the PostgreSQL database?
echo 1. Set up local PostgreSQL database with psql (requires PostgreSQL server)
echo 2. Show Docker command to run PostgreSQL container
echo 3. Skip database setup (use existing database or configure manually)

set /p db_option=Select an option (1-3): 
if "%db_option%"=="1" goto setup_postgres
if "%db_option%"=="2" goto show_docker_command
if "%db_option%"=="3" (
    echo Skipping database setup
) else (
    echo Invalid option, skipping database setup
)

echo === Setup Complete ===
echo All dependencies have been installed successfully.
for /f "tokens=*" %%i in ('%PYTHON_CMD% --version') do (
    set PYTHON_VERSION=%%i
)
echo Python version for virtual environment: %PYTHON_VERSION%

:: Ask to start development environment
set /p start_dev=Do you want to start the development environment now? (y/n): 
if /i "%start_dev%"=="y" (
    echo Starting development environment...
    call "%ROOT_DIR%\start_dev.bat"
) else (
    echo Setup completed. To start the development environment later, run:
    echo   %ROOT_DIR%\start_dev.bat
)

exit /b 0