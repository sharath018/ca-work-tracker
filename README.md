# CA Work Tracker v1.0.0

Professional work logging and billing tracker for Chartered Accountants (CAs).

## Overview

CA Work Tracker is a comprehensive desktop application designed to help Chartered Accountants and their firms manage work entries, track billable hours, and maintain detailed records of client work across multiple matters.

**Key Features:**
- Log work entries with client, category, hours, and billable status
- Track work status (Pending → In Progress → Completed → Billed → Closed)
- Search and filter work entries by multiple criteria
- Dashboard showing billable amount and task statistics
- Export data to CSV and PDF formats
- Automatic database backups with cleanup
- Cross-platform support (Windows 10 & 11)

## Installation

### For End Users (Windows)

1. Download the latest installer from [GitHub Releases](https://github.com/[your-repo]/releases)
2. Run `CAWorkTracker_Setup_v1.0.0.exe`
3. Follow the installation wizard
4. Launch from Start Menu or Desktop shortcut

### For Developers

**Requirements:**
- Python 3.8+
- pip (Python package manager)

**Setup:**

```bash
# Clone the repository
git clone https://github.com/[your-repo]/ca-work-tracker.git
cd ca-work-tracker

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python src/main.py
```

## Building from Source

### Building .exe for Windows Distribution

```bash
cd build_scripts

# On Windows
build.bat

# On Linux/Mac
./build.sh
```

The built application will be in `dist/CA_Work_Tracker/`

### Version Management

Update version before building:

```bash
cd build_scripts
python version.py patch   # 1.0.0 → 1.0.1
python version.py minor   # 1.0.0 → 1.1.0
python version.py major   # 1.0.0 → 2.0.0
```

## Project Structure

```
ca-work-tracker/
├── src/
│   ├── main.py                          # Application entry point
│   └── ca_tracker/
│       ├── __init__.py
│       ├── config.py                    # Configuration and constants
│       ├── version.py                   # Version information
│       ├── ui/
│       │   ├── __init__.py
│       │   └── main_window.py          # Main UI window
│       ├── database/
│       │   ├── __init__.py
│       │   ├── manager.py              # Database connection manager
│       │   └── schema.py               # Database schema and migrations
│       └── utils/
│           ├── __init__.py
│           ├── path_utils.py           # PyInstaller path handling
│           └── logger.py               # Logging configuration
├── assets/                              # Application assets (icons, etc)
├── build_scripts/
│   ├── build.bat                        # Windows build script
│   ├── build.sh                         # Linux/Mac build script
│   └── version.py                       # Version management utility
├── installer/                           # Installer configuration (Inno Setup)
├── docs/
│   ├── CA_Work_Tracker_Production_Roadmap.md
│   └── phases-of-implementation/
├── ca_tracker.spec                      # PyInstaller configuration
├── requirements.txt                     # Python dependencies
├── version.txt                          # Single source of truth for version
├── CHANGELOG.md                         # Release history
└── README.md                            # This file
```

## Architecture

### Database
- SQLite database with automatic backup on startup
- Automatic error recovery and reconnection
- Indexes on frequently queried columns for performance
- Schema versioning for future migrations

### UI
- Tkinter-based cross-platform interface
- Responsive layout with horizontal/vertical scrollbars
- Form validation and user feedback
- Double-click to edit functionality

### Logging
- File-based logging to `ca_work_tracker.log`
- Console logging for development
- Comprehensive error tracking for debugging

## Data Privacy

⚠️ **Important Security Note:**

Currently, the database is stored as an unencrypted SQLite file. Client financial data is stored in plain text. For enterprises handling sensitive financial information, consider:

1. **Phase 2 Enhancement**: Implement database encryption
2. **Manual Security**: Store the database file in an encrypted folder or external drive
3. **Access Control**: Restrict access to the application directory

## Support

For issues, feature requests, or questions:
1. Check [GitHub Issues](https://github.com/[your-repo]/issues)
2. Review [Production Roadmap](docs/CA_Work_Tracker_Production_Roadmap.md)
3. Contact: [support email]

## License

[License information]

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and release notes.

---

**Current Version:** 1.0.0  
**Last Updated:** January 15, 2025  
**Supported Platforms:** Windows 10, Windows 11
