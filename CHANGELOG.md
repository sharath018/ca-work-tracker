# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.0.0] - 2025-01-15

### Initial Production Release

**Phase 1 Implementation - Foundation & Infrastructure**

#### Added
- Production-ready project structure with modular architecture
- Enhanced database manager with automatic error recovery and reconnection logic
- Comprehensive logging system for debugging and production monitoring
- Improved backup strategy with automatic cleanup (keeps max 30 daily backups)
- Date validation with proper error handling
- Search functionality extended to include `requested_by` field
- Horizontal scrollbar for table navigation on smaller screens
- Window minimum size constraints (1200×700) for better UX
- Confirmation dialog on Update operations for data safety
- Automatic index creation on database columns for faster queries
- Better billable tracking (stored as integer instead of text)

#### Fixed
- Database connection error recovery - app no longer crashes on connection failures
- PDF export now respects current filters/search view
- Dashboard now shows only billable amounts (excludes non-billable work)
- Backup cleanup prevents infinite accumulation of backup files
- Date field now has format validation (DD-MMM-YYYY)

#### Infrastructure
- Created modular architecture with separate packages for database, UI, utils
- Set up PyInstaller configuration for Windows .exe building
- Added build scripts for automated packaging
- Version management system
- Comprehensive error handling and logging throughout
- Git workflow setup with proper .gitignore

#### Architecture Decisions
- Split monolithic script into modular Python packages for maintainability
- Implemented DatabaseManager class for connection resilience
- Separated UI, database, and utility concerns
- Used PyInstaller `--onedir` approach (recommended for easier updates)
- Implemented logging to both file and console for better debugging

### Known Limitations (Phase 2+ features)
- Monthly summary report not yet implemented
- Date range filtering not yet available
- In-app version checking not implemented
- Code signing certificate not applied (causes Windows SmartScreen warning)
- Application icon not yet set

### Windows Support
✓ Windows 10
✓ Windows 11

### Build Instructions
```bash
# Install dependencies
pip install -r requirements.txt

# Run development version
python src/main.py

# Build .exe for distribution
cd build_scripts
build.bat  # On Windows
# or
./build.sh  # On Linux/Mac
```
