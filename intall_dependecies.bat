@echo off
title Checkmate Royale - Dependency Installer

echo ==========================================================
echo     Checkmate Royale - Dependency Check & Installation
echo ==========================================================
echo.
echo This script will:
echo   - Check if Python and pip are installed
echo   - Install required packages: Pillow, python-chess
echo.
echo MANUAL REQUIREMENTS:
echo   1. Python: Download from https://www.python.org/downloads/
echo      IMPORTANT: Check "Add Python to PATH" during install.
echo.
echo   2. Stockfish Engine:
echo      Download from https://stockfishchess.org/download/
echo      Place the executable in your project folder.
echo.
echo   3. Assets Folder:
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
pip install Pillow python-chess

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install packages. Check your internet connection or try running as Administrator.
    goto End
)

echo.
echo SUCCESS: All Python packages installed.
echo.

:: --- Open README.md ---
echo Opening README.md...
start README.md

:End
echo ==========================================================
echo Reminder:
echo - Make sure Stockfish is downloaded & path updated in your script.
echo - Ensure 'assets' folder is in the same directory as the script.
echo ==========================================================
echo Press any key to close this window.
pause > nul
