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

# Start frontend
echo "Starting frontend..."
cd "${FRONTEND_DIR}" || { echo "Error: Frontend directory not found"; exit 1; }
yarn dev &
FRONTEND_PID=$!
echo "Frontend started with PID: ${FRONTEND_PID}"
echo

# Start backend
echo "Starting backend services..."
cd "${BACKEND_DIR}" || { echo "Error: Backend directory not found"; exit 1; }

# Check if poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "Error: Poetry is not installed or not in PATH"
    cleanup
fi

# Check if setuptools/pkg_resources is installed in the poetry environment
if ! poetry run python -c "import pkg_resources" 2>/dev/null; then
    echo "Warning: pkg_resources module not found. Installing setuptools..."
    poetry add setuptools
    if [ $? -ne 0 ]; then
        echo "Failed to install setuptools. Please run setup.sh again."
        cleanup
    fi
fi

# Start Celery worker
echo "Starting Celery worker..."
poetry run celery --app=config worker --loglevel=INFO --concurrency=1 &
CELERY_PID=$!
echo "Celery worker started with PID: ${CELERY_PID}"

# Start Django server
echo "Starting Django development server..."
poetry run python manage.py runserver &
DJANGO_PID=$!
echo "Django server started with PID: ${DJANGO_PID}"

echo
echo "=== All services started ==="
echo "Press Ctrl+C to stop all services"

# Wait for all background processes to finish (or until we receive SIGINT)
wait

# Should not reach here unless a background process exits unexpectedly
echo "One or more processes exited unexpectedly"
cleanup
