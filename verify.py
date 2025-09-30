#!/usr/bin/env python3
"""
Password Strength Checker - Installation Verification Script
This script verifies that all dependencies are properly installed
"""

import sys
import importlib
import subprocess
import platform
from pathlib import Path

# Required packages
REQUIRED_PACKAGES = [
    ('streamlit', '1.28.0'),
    ('re', None),  # Built-in
    ('math', None),  # Built-in
    ('collections', None),  # Built-in
    ('string', None),  # Built-in
    ('secrets', None),  # Built-in
    ('random', None),  # Built-in
]

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    min_version = (3, 7)
    
    print(f"🐍 Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version >= min_version:
        print("✅ Python version is compatible")
        return True
    else:
        print(f"❌ Python {min_version[0]}.{min_version[1]}+ required")
        return False

def check_package(package_name, min_version=None):
    """Check if a package is installed and meets minimum version"""
    try:
        module = importlib.import_module(package_name)
        
        if hasattr(module, '__version__') and min_version:
            installed_version = module.__version__
            print(f"📦 {package_name}: {installed_version}")
            
            # Simple version comparison (works for most cases)
            if installed_version >= min_version:
                print(f"✅ {package_name} version is compatible")
                return True
            else:
                print(f"❌ {package_name} {min_version}+ required")
                return False
        else:
            print(f"✅ {package_name}: Available")
            return True
            
    except ImportError:
        print(f"❌ {package_name}: Not installed")
        return False

def check_system_info():
    """Display system information"""
    print("💻 System Information:")
    print(f"   OS: {platform.system()} {platform.release()}")
    print(f"   Architecture: {platform.machine()}")
    print(f"   Python: {platform.python_version()}")
    print("")

def check_files():
    """Check if required files exist"""
    required_files = [
        'app.py',
        'requirements.txt',
        'README.md',
        'run.py'
    ]
    
    print("📁 Required Files:")
    all_files_exist = True
    
    for file_name in required_files:
        file_path = Path(file_name)
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"✅ {file_name} ({size} bytes)")
        else:
            print(f"❌ {file_name} - Missing!")
            all_files_exist = False
    
    return all_files_exist

def test_streamlit():
    """Test if Streamlit can start"""
    print("\n🧪 Testing Streamlit...")
    try:
        # Test streamlit import
        import streamlit as st
        print("✅ Streamlit imports successfully")
        
        # Test if streamlit command works
        result = subprocess.run([sys.executable, '-m', 'streamlit', '--version'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Streamlit command works: {version}")
            return True
        else:
            print("❌ Streamlit command failed")
            return False
            
    except Exception as e:
        print(f"❌ Streamlit test failed: {e}")
        return False

def main():
    """Main verification function"""
    print("🔒 Password Strength Checker - Installation Verification")
    print("=" * 60)
    
    # Check system info
    check_system_info()
    
    # Check Python version
    python_ok = check_python_version()
    print("")
    
    # Check required files
    files_ok = check_files()
    print("")
    
    # Check packages
    print("📦 Package Dependencies:")
    packages_ok = True
    
    for package, min_version in REQUIRED_PACKAGES:
        if not check_package(package, min_version):
            packages_ok = False
    
    print("")
    
    # Test Streamlit
    streamlit_ok = test_streamlit()
    
    print("\n" + "=" * 60)
    print("📊 Verification Summary:")
    
    results = {
        "Python Version": python_ok,
        "Required Files": files_ok,
        "Dependencies": packages_ok,
        "Streamlit Test": streamlit_ok
    }
    
    all_good = True
    for check, status in results.items():
        icon = "✅" if status else "❌"
        print(f"{icon} {check}")
        if not status:
            all_good = False
    
    print("\n" + "=" * 60)
    
    if all_good:
        print("🎉 All checks passed! You're ready to run the Password Strength Checker!")
        print("\n🚀 To start the application, run:")
        print("   python run.py")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print("\n🔧 To fix issues:")
        print("   1. Install Python 3.7+: https://python.org/downloads")
        print("   2. Install dependencies: pip install -r requirements.txt")
        print("   3. Run this verification again: python verify.py")
    
    return all_good

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n👋 Verification cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Verification failed with error: {e}")
        sys.exit(1)