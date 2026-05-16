@echo off
REM Build script for CA Work Tracker PyInstaller
REM Usage: build.bat

echo.
echo ============================================
echo CA Work Tracker - Build Script
echo ============================================
echo.

REM Check if PyInstaller is installed
where pyinstaller >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: PyInstaller is not installed
    echo Please run: pip install pyinstaller
    if not defined CI pause
    exit /b 1
)

REM Clean previous builds
echo Cleaning previous builds...
cd ..
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

REM Run PyInstaller from root directory
echo.
echo Building CA Work Tracker...
pyinstaller --clean ca_tracker.spec

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================
    echo Build completed successfully!
    echo ============================================
    echo.
    echo Output folder: dist\CA_Work_Tracker
    echo Executable: dist\CA_Work_Tracker\main.exe
    echo.
) else (
    echo.
    echo ERROR: Build failed
    echo Please check the output above for details
    if not defined CI pause
    exit /b 1
)

if not defined CI pause
