@echo off
echo ========================================
echo    SOLAR MONITORING DASHBOARD
echo    Starting Streamlit Server...
echo ========================================
echo.

REM Kiểm tra Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found!
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Kiểm tra Streamlit
python -c "import streamlit" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Installing required packages...
    pip install -r requirements.txt
    echo.
)

echo [OK] Dependencies ready
echo.
echo ========================================
echo    Starting Dashboard...
echo    URL: http://localhost:8501
echo    Press Ctrl+C to stop
echo ========================================
echo.

streamlit run app.py

pause

