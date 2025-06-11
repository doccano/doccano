#!/bin/bash

# Script to set up doccano development environment
# This script installs all dependencies and can start the dev environment

# Directory paths
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRONTEND_DIR="${ROOT_DIR}/frontend"
BACKEND_DIR="${ROOT_DIR}/backend"

echo "=== Doccano Development Environment Setup ==="
echo "Root directory: ${ROOT_DIR}"
echo

# Check prerequisites
echo "Checking prerequisites..."

if ! command -v git &> /dev/null; then
    echo "Error: git is not installed or not in PATH"
    exit 1
fi

# Check for Python 3.10 specifically
PYTHON_CMD=""
if command -v python3.10 &> /dev/null; then
    PYTHON_CMD="python3.10"
elif command -v python3 &> /dev/null; then
    PY_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    if [[ "$PY_VERSION" == "3.10" ]]; then
        PYTHON_CMD="python3"
    fi
fi

if [ -z "$PYTHON_CMD" ]; then
    echo "Error: Python 3.10 is not installed or not in PATH"
    echo "Please install Python 3.10: https://www.python.org/downloads/"
    exit 1
fi

echo "Found Python 3.10: $(which $PYTHON_CMD)"

if ! command -v poetry &> /dev/null; then
    echo "Error: Poetry is not installed or not in PATH"
    echo "Please install Poetry: https://python-poetry.org/docs/#installation"
    exit 1
fi

if ! command -v yarn &> /dev/null; then
    echo "Error: Yarn is not installed or not in PATH"
    echo "Please install Yarn: https://yarnpkg.com/getting-started/install"
    exit 1
fi

# Set up backend
echo "Setting up backend..."
cd "${BACKEND_DIR}" || { echo "Error: Backend directory not found"; exit 1; }
echo "Configuring Poetry to use Python 3.10..."
PYTHON_PATH=$(which $PYTHON_CMD)
poetry env use $PYTHON_PATH

# Update Python version in pyproject.toml to match setuptools requirements
echo "Updating Python version in pyproject.toml..."
if [ -f pyproject.toml ]; then
    # Check if we need to modify the Python version constraint
    if grep -q "python = \"\^3.8\"" pyproject.toml || grep -q "python = \">=3.8,<4.0\"" pyproject.toml; then
        echo "Updating Python version constraint from 3.8 to 3.9..."
        sed -i.bak 's/python = "\^3.8"/python = "^3.9"/g' pyproject.toml
        sed -i.bak 's/python = ">=3.8,<4.0"/python = ">=3.9,<4.0"/g' pyproject.toml
        rm -f pyproject.toml.bak
    fi
fi

# Ensure setuptools is installed with a compatible version
echo "Installing setuptools to provide pkg_resources module..."
poetry add setuptools || {
    echo "Failed to install latest setuptools. Trying with a version compatible with Python 3.9+..."
    poetry add "setuptools<81.0.0" || {
        echo "ERROR: Failed to install setuptools."
        echo "Please make sure you're using Python 3.9+ and try running setup.sh again."
        exit 1
    }
}

# Install PostgreSQL adapter (inside backend directory)
echo "Installing PostgreSQL adapter (psycopg2-binary)..."
poetry add psycopg2-binary || {
    echo "Failed to install psycopg2-binary through Poetry."
    echo "Trying direct pip installation..."
    poetry run pip install psycopg2-binary || {
        echo "ERROR: Failed to install psycopg2-binary."
        echo "Please make sure you have PostgreSQL development libraries installed."
        echo "On Ubuntu/Debian: sudo apt-get install libpq-dev python3-dev"
        echo "On macOS: brew install postgresql"
        exit 1
    }
}

echo "Installing Python dependencies with Poetry..."
poetry install
echo "Backend dependencies installed successfully."

# Initialize Django database
echo
echo "=== Initializing Django Database ==="
echo "Running database migrations..."
poetry run python manage.py migrate

echo "Creating user roles..."
poetry run python manage.py create_roles

echo "Creating admin user..."
poetry run python manage.py create_admin --noinput --username "admin" --email "admin@example.com" --password "password"
echo "Admin user created with username: admin and password: password"
echo "Database initialization completed successfully."
echo

# Set up frontend
echo "Setting up frontend..."
cd "${FRONTEND_DIR}" || { echo "Error: Frontend directory not found"; exit 1; }
echo "Installing JavaScript dependencies with Yarn..."
yarn install
echo "Frontend dependencies installed successfully."
echo

cd "${ROOT_DIR}" || exit

# Database setup function
setup_postgres() {
    echo
    echo "=== PostgreSQL Database Setup ==="
    
    # Check if psql is installed
    if ! command -v psql &> /dev/null; then
        echo "Error: PostgreSQL client (psql) is not installed or not in PATH"
        echo "Please install PostgreSQL: https://www.postgresql.org/download/"
        return 1
    fi
    
    echo "PostgreSQL client found: $(which psql)"
    
    # Check if PostgreSQL server is running
    if ! pg_isready &> /dev/null; then
        echo "Error: PostgreSQL server is not running"
        echo "Please start your PostgreSQL server"
        return 1
    fi
    
    echo "PostgreSQL server is running"
    
    # Default values
    local PG_USER="doccano_admin"
    local PG_PASS="doccano_pass"
    local PG_DB="doccano"
    local PG_HOST="localhost"
    local PG_PORT="5432"
    
    echo "Setting up PostgreSQL database with the following configuration:"
    echo "  Host: ${PG_HOST}:${PG_PORT}"
    echo "  Database: ${PG_DB}"
    echo "  User: ${PG_USER}"
    echo "  Password: ${PG_PASS}"
    echo
    
    # Ask for confirmation
    read -p "Continue with these settings? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Database setup cancelled"
        return 1
    fi
    
    # Create user if it doesn't exist
    echo "Creating user ${PG_USER} if it doesn't exist..."
    psql -h ${PG_HOST} -p ${PG_PORT} -c "SELECT 1 FROM pg_roles WHERE rolname='${PG_USER}'" | grep -q 1
    if [ $? -ne 0 ]; then
        psql -h ${PG_HOST} -p ${PG_PORT} -c "CREATE USER ${PG_USER} WITH PASSWORD '${PG_PASS}';"
        if [ $? -ne 0 ]; then
            echo "Error: Failed to create user ${PG_USER}"
            return 1
        fi
        echo "User ${PG_USER} created successfully"
    else
        echo "User ${PG_USER} already exists"
    fi
    
    # Grant privileges to user
    echo "Granting necessary privileges to ${PG_USER}..."
    psql -h ${PG_HOST} -p ${PG_PORT} -c "ALTER USER ${PG_USER} WITH CREATEDB;" || {
        echo "Error: Failed to grant CREATEDB privilege to ${PG_USER}"
        return 1
    }
    
    # Create database if it doesn't exist
    echo "Creating database ${PG_DB} if it doesn't exist..."
    psql -h ${PG_HOST} -p ${PG_PORT} -c "SELECT 1 FROM pg_database WHERE datname='${PG_DB}'" | grep -q 1
    if [ $? -ne 0 ]; then
        psql -h ${PG_HOST} -p ${PG_PORT} -c "CREATE DATABASE ${PG_DB} OWNER ${PG_USER};"
        if [ $? -ne 0 ]; then
            echo "Error: Failed to create database ${PG_DB}"
            return 1
        fi
        echo "Database ${PG_DB} created successfully"
    else
        echo "Database ${PG_DB} already exists"
        
        # Ensure the existing database is owned by our user
        psql -h ${PG_HOST} -p ${PG_PORT} -c "ALTER DATABASE ${PG_DB} OWNER TO ${PG_USER};" || {
            echo "Warning: Failed to change ownership of existing database ${PG_DB}"
        }
    fi
    
    # Grant privileges on database
    echo "Granting all privileges on database ${PG_DB} to ${PG_USER}..."
    psql -h ${PG_HOST} -p ${PG_PORT} -c "GRANT ALL PRIVILEGES ON DATABASE ${PG_DB} TO ${PG_USER};" || {
        echo "Error: Failed to grant privileges on ${PG_DB} to ${PG_USER}"
        return 1
    }
    
    echo "PostgreSQL database setup completed successfully"
    echo "Connection URL: postgres://${PG_USER}:${PG_PASS}@${PG_HOST}:${PG_PORT}/${PG_DB}?sslmode=disable"
    echo
    
    # Store the config in a .env file
    echo "DATABASE_URL=postgres://${PG_USER}:${PG_PASS}@${PG_HOST}:${PG_PORT}/${PG_DB}?sslmode=disable" > "${ROOT_DIR}/.env"
    echo "Database configuration saved to ${ROOT_DIR}/.env"
    
    # Create a .env file also in the backend directory for direct access
    echo "DATABASE_URL=postgres://${PG_USER}:${PG_PASS}@${PG_HOST}:${PG_PORT}/${PG_DB}?sslmode=disable" > "${BACKEND_DIR}/.env"
    echo "Database configuration also saved to ${BACKEND_DIR}/.env"
    
    return 0
}

# Docker PostgreSQL setup function
show_docker_command() {
    echo
    echo "=== PostgreSQL Docker Setup Command ==="
    echo "To set up PostgreSQL in a Docker container, run:"
    echo
    echo "docker run -d \\"
    echo "  --name doccano-postgres \\"
    echo "  -e POSTGRES_USER=doccano_admin \\"
    echo "  -e POSTGRES_PASSWORD=doccano_pass \\"
    echo "  -e POSTGRES_DB=doccano \\"
    echo "  -v doccano-db:/var/lib/postgresql/data \\"
    echo "  -p 5432:5432 \\"
    echo "  postgres:13.8-alpine"
    echo
    echo "After running the container, press any key to continue setup..."
    echo
    read -n 1 -s -r
    # After showing the command and waiting for user to run it, save the connection info
    echo "DATABASE_URL=postgres://doccano_admin:doccano_pass@localhost:5432/doccano?sslmode=disable" > "${ROOT_DIR}/.env"
    echo "DATABASE_URL=postgres://doccano_admin:doccano_pass@localhost:5432/doccano?sslmode=disable" > "${BACKEND_DIR}/.env"
    echo "Database configuration saved to ${ROOT_DIR}/.env and ${BACKEND_DIR}/.env"
}

# Ask about database setup
echo
echo "=== Database Configuration ==="
echo "How would you like to set up the PostgreSQL database?"
echo "1. Set up local PostgreSQL database with psql (requires PostgreSQL server)"
echo "2. Show Docker command to run PostgreSQL container"
echo "3. Skip database setup (use existing database or configure manually)"

read -p "Select an option (1-3): " db_option
case $db_option in
    1)
        setup_postgres
        ;;
    2)
        show_docker_command
        ;;
    3)
        echo "Skipping database setup"
        ;;
    *)
        echo "Invalid option, skipping database setup"
        ;;
esac

echo "=== Setup Complete ==="
echo "All dependencies have been installed successfully."
echo "Python version for virtual environment: $($PYTHON_CMD --version)"

# Ask to start development environment
read -p "Do you want to start the development environment now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Starting development environment..."
    "${ROOT_DIR}/start_dev.sh"
else
    echo "Setup completed. To start the development environment later, run:"
    echo "  ${ROOT_DIR}/start_dev.sh"
fi
