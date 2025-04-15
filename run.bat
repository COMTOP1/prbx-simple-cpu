@echo off

REM Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not added to PATH.
    pause
    exit /b
)

REM Run the Python GUI
python main.py -gui
pause