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

# Ensure setuptools (which provides pkg_resources) is installed
echo "Installing setuptools to provide pkg_resources module..."
poetry add setuptools

echo "Installing Python dependencies with Poetry..."
poetry install
echo "Backend dependencies installed successfully."
echo

# Set up frontend
echo "Setting up frontend..."
cd "${FRONTEND_DIR}" || { echo "Error: Frontend directory not found"; exit 1; }
echo "Installing JavaScript dependencies with Yarn..."
yarn install
echo "Frontend dependencies installed successfully."
echo

cd "${ROOT_DIR}" || exit

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
