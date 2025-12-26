@echo off
echo ========================================
echo    SOLAR MONITORING DASHBOARD
echo    Starting Local Server...
echo ========================================
echo.

REM Kiểm tra Python
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] Python found! Starting server...
    echo.
    echo Server running at: http://localhost:8000
    echo Press Ctrl+C to stop the server
    echo.
    python -m http.server 8000
    goto :end
)

REM Kiểm tra Python 2
python2 --version >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] Python 2 found! Starting server...
    echo.
    echo Server running at: http://localhost:8000
    echo Press Ctrl+C to stop the server
    echo.
    python2 -m SimpleHTTPServer 8000
    goto :end
)

REM Nếu không có Python, mở trực tiếp
echo [INFO] Python not found. Opening file directly...
echo [WARNING] You may encounter CORS errors. Consider installing Python.
echo.
start index.html
goto :end

:end
pause

