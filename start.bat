@echo off
echo Starting Password Strength Checker...
cd /d "E:\GIT PROJECTS\PasswordStrengthChecker"
echo Current directory: %cd%
echo Testing if app.py exists...
if exist app.py (
    echo ✅ app.py found
    echo Starting Streamlit...
    streamlit run app.py --server.address localhost --server.port 8501
) else (
    echo ❌ app.py not found in current directory
    echo Current directory contents:
    dir
    pause
)