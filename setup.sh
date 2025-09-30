#!/bin/bash

# Password Strength Checker - Cross-Platform Setup Script
# This script sets up the environment and runs the application

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to detect OS
detect_os() {
    case "$(uname -s)" in
        Linux*)     echo "Linux";;
        Darwin*)    echo "Mac";;
        CYGWIN*)    echo "Windows";;
        MINGW*)     echo "Windows";;
        MSYS*)      echo "Windows";;
        *)          echo "Unknown";;
    esac
}

# Main setup function
main() {
    print_status "🔒 Password Strength Checker Setup"
    print_status "Detecting operating system..."
    
    OS=$(detect_os)
    print_success "Detected OS: $OS"
    
    # Check for Python
    if command_exists python3; then
        PYTHON_CMD="python3"
    elif command_exists python; then
        PYTHON_CMD="python"
    else
        print_error "Python is not installed. Please install Python 3.7+ and try again."
        exit 1
    fi
    
    print_success "Found Python: $($PYTHON_CMD --version)"
    
    # Check for pip
    if command_exists pip3; then
        PIP_CMD="pip3"
    elif command_exists pip; then
        PIP_CMD="pip"
    else
        print_error "pip is not installed. Please install pip and try again."
        exit 1
    fi
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        print_status "Creating virtual environment..."
        $PYTHON_CMD -m venv venv
        print_success "Virtual environment created"
    fi
    
    # Activate virtual environment
    print_status "Activating virtual environment..."
    if [ "$OS" = "Windows" ]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    
    # Upgrade pip
    print_status "Upgrading pip..."
    $PIP_CMD install --upgrade pip
    
    # Install requirements
    print_status "Installing dependencies..."
    $PIP_CMD install -r requirements.txt
    
    print_success "Setup complete! 🎉"
    print_status "Starting Password Strength Checker..."
    
    # Run the application
    streamlit run app.py --server.headless true
}

# Run setup if script is executed directly
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main "$@"
fi