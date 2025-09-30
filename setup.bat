@echo off
REM Password Strength Checker - Windows Setup Script
REM This script sets up the environment and runs the application

setlocal enabledelayedexpansion

echo [INFO] 🔒 Password Strength Checker Setup
echo [INFO] Detecting Windows environment...

REM Check for Python
python --version >nul 2>&1
if errorlevel 1 (
    py --version >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Python is not installed. Please install Python 3.7+ and try again.
        pause
        exit /b 1
    ) else (
        set PYTHON_CMD=py
    )
) else (
    set PYTHON_CMD=python
)

echo [SUCCESS] Found Python
%PYTHON_CMD% --version

REM Check for pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is not installed. Please install pip and try again.
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    %PYTHON_CMD% -m venv venv
    echo [SUCCESS] Virtual environment created
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo [INFO] Installing dependencies...
pip install -r requirements.txt

echo [SUCCESS] Setup complete! 🎉
echo [INFO] Starting Password Strength Checker...

REM Run the application
streamlit run app.py --server.headless true

pause