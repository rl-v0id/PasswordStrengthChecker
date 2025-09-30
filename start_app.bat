@echo off
echo Starting Password Strength Checker...
cd /d "E:\GIT PROJECTS\PasswordStrengthChecker"
echo Current directory: %cd%

if exist app.py (
    echo ✅ app.py found
    echo ✅ Starting Streamlit on http://localhost:8501
    echo ✅ The app will open automatically in your browser
    echo.
    echo 🛑 To stop the server, close this window or press Ctrl+C
    echo.
    streamlit run app.py
) else (
    echo ❌ app.py not found in current directory
    echo Current directory contents:
    dir
    pause
)