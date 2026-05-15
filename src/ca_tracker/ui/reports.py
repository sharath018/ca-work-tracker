"""Reporting and summary functionality for CA Work Tracker."""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from ca_tracker.config import DATE_FORMAT


class MonthlySummaryReport:
    """Monthly summary report view."""
    
    def __init__(self, db, from_date, to_date):
        """
        Initialize monthly summary report.
        
        Args:
            db: Database manager instance
            from_date: Start date
            to_date: End date
        """
        self.db = db
        self.from_date = from_date
        self.to_date = to_date
        self.data = {}
        self.load_data()
    
    def load_data(self):
        """Load summary data from database."""
        from_str = self.from_date.strftime(DATE_FORMAT)
        to_str = self.to_date.strftime(DATE_FORMAT)
        
        # Total billable amount
        self.db.execute(
            "SELECT SUM(amount) FROM work_log WHERE billable=1 AND date BETWEEN ? AND ?",
            (from_str, to_str)
        )
        self.data['total_billable'] = self.db.fetchone()[0] or 0
        
        # Total hours
        self.db.execute(
            "SELECT SUM(hours) FROM work_log WHERE date BETWEEN ? AND ?",
            (from_str, to_str)
        )
        self.data['total_hours'] = self.db.fetchone()[0] or 0
        
        # Total entries
        self.db.execute(
            "SELECT COUNT(*) FROM work_log WHERE date BETWEEN ? AND ?",
            (from_str, to_str)
        )
        self.data['total_entries'] = self.db.fetchone()[0] or 0
        
        # By status
        self.db.execute(
            "SELECT status, COUNT(*), SUM(amount) FROM work_log WHERE date BETWEEN ? AND ? GROUP BY status",
            (from_str, to_str)
        )
        self.data['by_status'] = self.db.fetchall()
        
        # By category
        self.db.execute(
            "SELECT category, COUNT(*), SUM(amount), SUM(hours) FROM work_log WHERE date BETWEEN ? AND ? GROUP BY category ORDER BY SUM(amount) DESC",
            (from_str, to_str)
        )
        self.data['by_category'] = self.db.fetchall()
        
        # By billable status
        self.db.execute(
            "SELECT billable, COUNT(*), SUM(amount), SUM(hours) FROM work_log WHERE date BETWEEN ? AND ? GROUP BY billable",
            (from_str, to_str)
        )
        self.data['by_billable'] = self.db.fetchall()
    
    def get_summary_text(self):
        """Get formatted summary as text."""
        summary = []
        summary.append("="*70)
        summary.append(f"CA WORK TRACKER - MONTHLY SUMMARY REPORT")
        summary.append(f"Period: {self.from_date.strftime(DATE_FORMAT)} to {self.to_date.strftime(DATE_FORMAT)}")
        summary.append("="*70)
        summary.append("")
        
        # Overview
        summary.append("OVERVIEW")
        summary.append("-" * 70)
        summary.append(f"Total Billable Amount:      ₹{self.data['total_billable']:,.2f}")
        summary.append(f"Total Hours:                {self.data['total_hours']:,.1f} hrs")
        summary.append(f"Total Entries:              {self.data['total_entries']} entries")
        if self.data['total_entries'] > 0:
            avg_billable = self.data['total_billable'] / self.data['total_entries']
            summary.append(f"Average per Entry:          ₹{avg_billable:,.2f}")
        summary.append("")
        
        # By Billable Status
        summary.append("BILLABLE STATUS BREAKDOWN")
        summary.append("-" * 70)
        billable_total = 0
        non_billable_total = 0
        for row in self.data['by_billable']:
            billable_flag, count, amount, hours = row
            amount = amount or 0
            hours = hours or 0
            status_label = "Billable" if billable_flag else "Non-Billable"
            summary.append(f"{status_label:20} {count:5} entries  ₹{amount:12,.2f}  {hours:8.1f} hrs")
            if billable_flag:
                billable_total = amount
            else:
                non_billable_total = amount
        summary.append("")
        
        # By Status
        summary.append("STATUS BREAKDOWN")
        summary.append("-" * 70)
        for row in self.data['by_status']:
            status, count, amount = row
            amount = amount or 0
            summary.append(f"{status:20} {count:5} entries  ₹{amount:12,.2f}")
        summary.append("")
        
        # By Category
        summary.append("CATEGORY BREAKDOWN (Top Contributors)")
        summary.append("-" * 70)
        summary.append(f"{'Category':<30} {'Count':>6} {'Amount':>15} {'Hours':>10}")
        summary.append("-" * 70)
        for row in self.data['by_category']:
            category, count, amount, hours = row
            amount = amount or 0
            hours = hours or 0
            summary.append(f"{category:<30} {count:>6} ₹{amount:>13,.2f} {hours:>10.1f}")
        summary.append("")
        summary.append("="*70)
        
        return "\n".join(summary)
    
    def get_data_dict(self):
        """Get raw data dictionary for programmatic access."""
        return self.data


class SummaryReportWindow:
    """Window for displaying summary report."""
    
    def __init__(self, parent, report):
        """
        Initialize summary report window.
        
        Args:
            parent: Parent window
            report: MonthlySummaryReport instance
        """
        self.window = tk.Toplevel(parent)
        self.window.title("Monthly Summary Report")
        self.window.geometry("900x600")
        self.report = report
        
        self.create_ui()
    
    def create_ui(self):
        """Create the report UI."""
        # Header
        header_frame = tk.Frame(self.window)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        period_text = f"Report Period: {self.report.from_date.strftime('%d-%b-%Y')} to {self.report.to_date.strftime('%d-%b-%Y')}"
        tk.Label(header_frame, text=period_text, font=("Arial", 12, "bold")).pack(anchor="w")
        
        # Text widget with scrollbar
        text_frame = tk.Frame(self.window)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.text_widget = tk.Text(
            text_frame, 
            font=("Courier", 10),
            yscrollcommand=scrollbar.set,
            bg="white",
            fg="black"
        )
        self.text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.text_widget.yview)
        
        # Display report
        report_text = self.report.get_summary_text()
        self.text_widget.insert("1.0", report_text)
        self.text_widget.config(state="disabled")
        
        # Buttons
        button_frame = tk.Frame(self.window)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Button(
            button_frame, text="Copy to Clipboard", 
            command=self.copy_to_clipboard
        ).pack(side="left", padx=5)
        
        tk.Button(
            button_frame, text="Close", 
            command=self.window.destroy
        ).pack(side="left", padx=5)
    
    def copy_to_clipboard(self):
        """Copy report text to clipboard."""
        try:
            self.window.clipboard_clear()
            self.window.clipboard_append(self.report.get_summary_text())
            messagebox.showinfo("Success", "Report copied to clipboard")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy: {e}")
