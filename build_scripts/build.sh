#!/bin/bash
# Build script for CA Work Tracker PyInstaller (Linux/Mac)
# Usage: ./build.sh

echo ""
echo "============================================"
echo "CA Work Tracker - Build Script"
echo "============================================"
echo ""

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "ERROR: PyInstaller is not installed"
    echo "Please run: pip install pyinstaller"
    exit 1
fi

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf dist build

# Run PyInstaller
echo ""
echo "Building CA Work Tracker..."
pyinstaller --clean ca_tracker.spec

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================"
    echo "Build completed successfully!"
    echo "============================================"
    echo ""
    echo "Output folder: dist/CA_Work_Tracker"
    echo "Executable: dist/CA_Work_Tracker/CA_Work_Tracker"
    echo ""
else
    echo ""
    echo "ERROR: Build failed"
    echo "Please check the output above for details"
    exit 1
fi
