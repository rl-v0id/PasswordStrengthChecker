#!/usr/bin/env python3
"""
Password Strength Checker - Cross-Platform Launcher
This script provides a cross-platform way to run the application
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def get_python_command():
    """Get the appropriate Python command for the current system"""
    commands = ['python3', 'python', 'py']
    
    for cmd in commands:
        try:
            result = subprocess.run([cmd, '--version'], 
                                 capture_output=True, text=True, check=True)
            if 'Python 3.' in result.stdout:
                return cmd
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    
    raise RuntimeError("Python 3.7+ not found. Please install Python and try again.")


def setup_environment():
    """Set up the virtual environment and install dependencies"""
    python_cmd = get_python_command()
    print(f"✅ Found Python: {python_cmd}")
    
    # Create virtual environment
    venv_path = Path('venv')
    if not venv_path.exists():
        print("🔧 Creating virtual environment...")
        subprocess.run([python_cmd, '-m', 'venv', 'venv'], check=True)
        print("✅ Virtual environment created")
    
    # Get activation script path
    system = platform.system().lower()
    if system == 'windows':
        activate_script = venv_path / 'Scripts' / 'activate'
        python_exe = venv_path / 'Scripts' / 'python.exe'
        pip_exe = venv_path / 'Scripts' / 'pip.exe'
    else:
        activate_script = venv_path / 'bin' / 'activate'
        python_exe = venv_path / 'bin' / 'python'
        pip_exe = venv_path / 'bin' / 'pip'
    
    # Install requirements
    if Path('requirements.txt').exists():
        print("📦 Installing dependencies...")
        
        # Try to upgrade pip (don't fail if it doesn't work)
        try:
            subprocess.run([str(python_exe), '-m', 'pip', 'install', '--upgrade', 'pip'], check=True)
            print("✅ Pip upgraded successfully")
        except subprocess.CalledProcessError:
            print("⚠️  Pip upgrade failed, continuing with existing version...")
        
        subprocess.run([str(pip_exe), 'install', '-r', 'requirements.txt'], check=True)
        print("✅ Dependencies installed")
    
    return python_exe


def run_app():
    """Run the Streamlit application"""
    try:
        python_exe = setup_environment()
        
        print("🚀 Starting Password Strength Checker...")
        print("🌐 The app will open in your default browser")
        print("📍 Local URL: http://localhost:8501")
        print("⏹️  Press Ctrl+C to stop the server\n")
        
        # Run streamlit
        subprocess.run([
            str(python_exe), '-m', 'streamlit', 'run', 'app.py',
                '--server.address', 'localhost',
            '--server.port', '8501'
        ], check=True)
        
    except KeyboardInterrupt:
        print("\n👋 Shutting down Password Strength Checker...")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("🔒 Password Strength Checker")
    print("=" * 40)
    
    # Initialize git repository
    try:
        print("📦 Initializing Git repository...")
        subprocess.run(['git', 'init'], check=True)
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit'], check=True)
        print("✅ Git repository initialized and initial commit made")
    except Exception as e:
        print(f"⚠️  Error initializing Git: {e}")
    
    run_app()
    subprocess.run(['git', 'push', '-u', 'origin', 'main'])