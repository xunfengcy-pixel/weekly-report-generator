@echo off
chcp 65001 >nul
echo ========================================
echo    Weekly Report Generator - Starting
echo ========================================
echo.

:: Get script directory
set "SCRIPT_DIR=%~dp0"
echo Script directory: %SCRIPT_DIR%

:: Change to script directory
cd /d "%SCRIPT_DIR%"
echo Current directory: %CD%
echo.

:: Check if app.py exists
if not exist "app.py" (
    echo ERROR: app.py not found in current directory!
    pause
    exit /b 1
)

:: Check if streamlit is available
where streamlit >nul 2>nul
if errorlevel 1 (
    echo ERROR: streamlit command not found!
    echo Please install it first: pip install streamlit
    pause
    exit /b 1
)

echo Streamlit is installed.
echo Starting Streamlit app...
echo Browser will open at: http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

:: Start Streamlit
streamlit run app.py

:: Pause when stopped
echo.
echo ========================================
echo    Server stopped
echo ========================================
pause
