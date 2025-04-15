@echo off
title Checkmate Royale - Dependency Installer

echo ==========================================================
echo     Checkmate Royale - Dependency Check & Installation
echo ==========================================================
echo.
echo This script will:
echo   - Check if Python and pip are installed
echo   - Install required packages: Pillow, python-chess, tkinter
echo   - Ensure assets folder is set up correctly
echo.
echo MANUAL REQUIREMENTS:
echo   1. Python: Download from https://www.python.org/downloads/
echo      IMPORTANT: Check "Add Python to PATH" during install.
echo.
echo   2. Assets Folder:
echo      Ensure folder 'assets' contains images like wp.png, bn.png, logo.png etc.
echo.
echo Press any key to begin installation or Ctrl+C to cancel...
pause > nul
echo.

:: --- Check Python ---
echo Checking for Python...
where python > nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found in PATH.
    echo Please install Python from https://www.python.org/downloads/
    goto End
) else (
    echo Python found:
    python --version
)

:: --- Check pip ---
echo.
echo Checking for pip...
where pip > nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: pip not found.
    echo Try reinstalling Python and make sure pip is added to PATH.
    goto End
) else (
    echo pip found:
    pip --version
)

:: --- Install Required Packages ---
echo.
echo Installing required packages...
pip install --upgrade pip

:: Install packages
pip install Pillow python-chess

:: Install tkinter if not present (tkinter is included in standard Python distribution for Windows)
echo Checking for tkinter...
python -c "import tkinter" > nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: tkinter is not installed. This should be bundled with Python.
    echo Please install Python with tkinter support.
    goto End
) else (
    echo tkinter is already installed.
)

echo.
echo SUCCESS: All Python packages installed.
echo.

:: --- Check Assets Folder ---
if exist "assets" (
    echo Assets folder found.
) else (
    echo ERROR: 'assets' folder not found. Make sure 'assets' folder is in the same directory as this script.
    goto End
)

:: --- Open README.md ---
echo.
if exist README.md (
    echo Opening README.md...
    start README.md
) else (
    echo README.md not found.
)

:End
echo ==========================================================
echo Reminder:
echo - Ensure 'assets' folder is in the same directory as the script.
echo ==========================================================
echo Press any key to close this window.
pause > nul
