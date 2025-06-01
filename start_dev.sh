#!/bin/bash

# Script to start doccano development environment

# Function to clean up background processes on exit
cleanup() {
  echo "Shutting down all processes..."
  # Kill all background processes in the current process group
  kill $(jobs -p) 2>/dev/null
  exit
}

# Set up trap to catch SIGINT (Ctrl+C) and other termination signals
trap cleanup SIGINT SIGTERM

# Directory paths
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRONTEND_DIR="${ROOT_DIR}/frontend"
BACKEND_DIR="${ROOT_DIR}/backend"

echo "=== Starting Doccano Development Environment ==="
echo "Root directory: ${ROOT_DIR}"
echo "Frontend directory: ${FRONTEND_DIR}"
echo "Backend directory: ${BACKEND_DIR}"
echo

# Start backend first
echo "Starting backend services..."
cd "${BACKEND_DIR}" || { echo "Error: Backend directory not found"; exit 1; }

# Check if poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "Error: Poetry is not installed or not in PATH"
    cleanup
fi

# Check Python version in the Poetry environment
PYTHON_VERSION=$(poetry run python --version 2>&1)
echo "Using Python: ${PYTHON_VERSION}"

# Check if setuptools/pkg_resources is installed in the poetry environment
if ! poetry run python -c "import pkg_resources" 2>/dev/null; then
    echo "Warning: pkg_resources module not found. Installing setuptools..."
    
    # Try to install a compatible version of setuptools based on Python version
    if echo "${PYTHON_VERSION}" | grep -q "3\.8\."; then
        echo "Python 3.8 detected, using setuptools<80.0.0"
        poetry add "setuptools<80.0.0"
    elif echo "${PYTHON_VERSION}" | grep -q "3\.9\.|3\.10\.|3\.11\."; then
        echo "Python 3.9+ detected, using latest setuptools"
        poetry add setuptools
    else
        echo "Trying setuptools with relaxed version constraints..."
        poetry add "setuptools<81.0.0" || {
            echo "ERROR: Failed to install setuptools."
            echo "Please run setup.sh to properly configure the environment."
            cleanup
        }
    fi
fi

# Set database environment variable for PostgreSQL
echo "Configuring PostgreSQL database connection..."
export DATABASE_URL="postgres://doccano_admin:doccano_pass@localhost:5432/doccano?sslmode=disable"
echo "DATABASE_URL set to: ${DATABASE_URL}"

# Ensure the database is migrated before starting the server
echo "Running database migrations..."
poetry run python manage.py migrate

# Start Django server first
echo "Starting Django development server..."
poetry run python manage.py runserver &
DJANGO_PID=$!
echo "Django server started with PID: ${DJANGO_PID}"

# Wait a moment for Django to fully start
echo "Waiting for Django server to initialize (5 seconds)..."
sleep 5

# Check if Django is actually running
if ! curl -s http://127.0.0.1:8000/ > /dev/null; then
    echo "ERROR: Django server failed to start properly."
    echo "Check if port 8000 is already in use or if there's a database connection issue."
    cleanup
fi

# Start Celery worker
echo "Starting Celery worker..."
DATABASE_URL="${DATABASE_URL}" poetry run celery --app=config worker --loglevel=INFO --concurrency=1 &
CELERY_PID=$!
echo "Celery worker started with PID: ${CELERY_PID}"

# Now start the frontend after the backend is confirmed running
echo "Starting frontend..."
cd "${FRONTEND_DIR}" || { echo "Error: Frontend directory not found"; exit 1; }
yarn dev &
FRONTEND_PID=$!
echo "Frontend started with PID: ${FRONTEND_PID}"
echo

echo
echo "=== All services started ==="
echo "Backend API: http://127.0.0.1:8000/"
echo "Frontend UI: http://localhost:3000/"
echo "Press Ctrl+C to stop all services"

# Wait for all background processes to finish (or until we receive SIGINT)
wait

# Should not reach here unless a background process exits unexpectedly
echo "One or more processes exited unexpectedly"
cleanup
