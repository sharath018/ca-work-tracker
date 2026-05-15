# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.1.0] - 2025-02-15

### Phase 2 Implementation - Feature Enhancements

#### Added
- **Date Range Filtering** - Filter work entries by custom date ranges with quick presets
  - "This Month", "Last Month", "Last 30 Days" preset buttons
  - Manual date range selection with validation
  - Default to last 30 days on startup
  
- **Monthly Summary Report** - Comprehensive reporting view
  - Total billable amount and hours worked
  - Breakdown by status (Pending, In Progress, Completed, Billed, Closed)
  - Breakdown by category with sorting by highest amount
  - Breakdown by billable status
  - Entry counts and averages
  - Copy to clipboard functionality
  
- **Filter-Aware Exports** - PDF and CSV exports now respect current filter/view
  - Export only filtered results, not entire database
  - Maintains consistency with on-screen view
  - Works with search, status filter, and date range filter
  
- **Enhanced Search** - Extended search now includes all relevant fields
  - Client name
  - Category
  - Summary/notes
  - Status
  - Requested By field
  
- **Filter State Tracking** - Internal filter state management
  - Maintains current active filter
  - Enables context-aware exports and reports
  - Clear separation of view types

#### Architecture Improvements
- New `filters.py` module with `DateRangeFilter` and `FilterState` classes
- New `reports.py` module with reporting functionality
- Refactored export methods to be filter-aware
- Better separation of concerns (UI, database, filtering, reporting)

#### User Experience
- More intuitive filter UI with clear date presets
- Monthly summary view with formatted output
- Better visual organization of filter options
- Date format validation with clear error messages

#### Fixed
- Export functionality now respects current filter/search
- Date range filtering with proper format validation

### Technical Details
- **DateRangeFilter**: Reusable UI component for date selection
- **FilterState**: Tracks active filters and generates SQL WHERE clauses
- **MonthlySummaryReport**: Generates comprehensive statistics and formatted reports
- **SummaryReportWindow**: Display window with export-to-clipboard feature

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

### Windows Support
✓ Windows 10
✓ Windows 11
