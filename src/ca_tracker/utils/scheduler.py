"""Simple scheduled report generator for CA Work Tracker.

This module provides a minimal background scheduler that can be started
from the main application to generate periodic summary reports and charts.
It's intentionally lightweight to avoid heavy dependencies.
"""
import threading
import os
from datetime import datetime, timedelta
from ca_tracker.ui.reports import MonthlySummaryReport

class ReportScheduler:
    """Schedule periodic generation of monthly summary reports."""

    def __init__(self, db_manager, output_dir=None, interval_hours=24):
        self.db = db_manager
        self.interval = max(1, interval_hours) * 3600
        self.output_dir = output_dir or os.path.join(os.getcwd(), "reports")
        os.makedirs(self.output_dir, exist_ok=True)
        self._timer = None
        self._stopped = False

    def _generate_report(self):
        try:
            today = datetime.now()
            # Default: last 30 days
            from_date = today - timedelta(days=30)
            to_date = today
            report = MonthlySummaryReport(self.db, from_date, to_date)
            # Write textual summary
            filename = os.path.join(self.output_dir, f"monthly_summary_{today.strftime('%Y%m%d')}.txt")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(report.get_summary_text())

            # Generate charts if available
            try:
                paths = report.generate_charts(self.output_dir)
            except Exception:
                paths = []

        except Exception:
            pass
        finally:
            # Reschedule if not stopped
            if not self._stopped:
                self._timer = threading.Timer(self.interval, self._generate_report)
                self._timer.daemon = True
                self._timer.start()

    def start(self):
        """Start the scheduler (runs in background)."""
        self._stopped = False
        if self._timer is None:
            self._timer = threading.Timer(1, self._generate_report)
            self._timer.daemon = True
            self._timer.start()

    def stop(self):
        """Stop the scheduler."""
        self._stopped = True
        if self._timer:
            try:
                self._timer.cancel()
            except Exception:
                pass
            self._timer = None
