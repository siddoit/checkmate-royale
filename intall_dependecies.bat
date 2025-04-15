@echo off
title Checkmate Royale - Dependency Installer

echo ==========================================================
echo     Checkmate Royale - Dependency Check & Installation
echo ==========================================================
echo.
echo This script will:
echo   - Check if Python and pip are installed
echo   - Install required packages: Pillow, python-chess
echo   - Auto-download Stockfish if not already present
echo.
echo MANUAL REQUIREMENTS:
echo   1. Python: https://www.python.org/downloads/
echo      IMPORTANT: Check "Add Python to PATH" during install.
echo.
echo   2. Assets Folder:
echo      Ensure 'assets' folder contains images like wp.png, bn.png, logo.png etc.
echo.
echo Press any key to begin installation or Ctrl+C to cancel...
pause > nul
echo.

:: --- Check Python ---
echo Checking for Python...
set PYTHON_OK=true
where python > nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found in PATH.
    echo Please install Python from https://www.python.org/downloads/
    set PYTHON_OK=false
) else (
    echo Python found:
    python --version
)

:: --- Check pip ---
echo.
if "%PYTHON_OK%"=="true" (
    echo Checking for pip...
    where pip > nul 2>&1
    if %errorlevel% neq 0 (
        echo ERROR: pip not found.
        echo Try reinstalling Python and make sure pip is added to PATH.
    ) else (
        echo pip found:
        pip --version

        :: --- Install Required Packages ---
        echo.
        echo Installing required packages...
        pip install --upgrade pip
        pip install Pillow python-chess

        if %errorlevel% neq 0 (
            echo.
            echo ERROR: Failed to install packages. Check your internet or run as Admin.
        ) else (
            echo.
            echo SUCCESS: All Python packages installed.
        )
    )
)

:: --- Setup Stockfish ---
set "STOCKFISH_PATH=C:\ChessEngines\stockfish\stockfish-windows-x86-64-avx2.exe"

if exist "%STOCKFISH_PATH%" (
    echo.
    echo Stockfish already installed at:
    echo %STOCKFISH_PATH%
) else (
    echo.
    echo Stockfish not found. Downloading now...
    powershell -Command ^
        "$url = 'https://stockfishchess.org/files/stockfish-16-win.zip'; ^
        $out = 'stockfish.zip'; ^
        Invoke-WebRequest -Uri $url -OutFile $out; ^
        Expand-Archive $out -DestinationPath 'stockfish_extract' -Force; ^
        $exe = Get-ChildItem -Path 'stockfish_extract' -Recurse -Filter 'stockfish-windows-x86-64-avx2.exe' | Select-Object -First 1; ^
        $target = 'C:\ChessEngines\stockfish'; ^
        New-Item -ItemType Directory -Force -Path $target | Out-Null; ^
        Copy-Item $exe.FullName -Destination $target; ^
        Remove-Item stockfish.zip; ^
        Remove-Item stockfish_extract -Recurse -Force"

    if exist "%STOCKFISH_PATH%" (
        echo SUCCESS: Stockfish downloaded and placed in:
        echo %STOCKFISH_PATH%
    ) else (
        echo ERROR: Failed to download Stockfish. Download manually if needed.
    )
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
echo.
echo ==========================================================
echo Reminder:
echo - Make sure 'assets' folder is in the same directory as this script.
echo - Stockfish will now be available at:
echo   %STOCKFISH_PATH%
echo ==========================================================
echo Press any key to close this window.
pause > nul
