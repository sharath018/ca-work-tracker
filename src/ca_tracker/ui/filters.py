"""Filter utilities and UI components for CA Work Tracker."""

import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from ca_tracker.config import DATE_FORMAT, STATUS_OPTIONS


class DateRangeFilter:
    """Date range filter UI component."""
    
    def __init__(self, parent, callback=None):
        """
        Initialize date range filter.
        
        Args:
            parent: Parent widget
            callback: Function to call when filter is applied
        """
        self.callback = callback
        self.frame = tk.Frame(parent)
        self.create_ui()
    
    def create_ui(self):
        """Create the date range filter UI."""
        tk.Label(self.frame, text="Date Range:").pack(side="left", padx=5)
        
        # From date
        tk.Label(self.frame, text="From").pack(side="left", padx=5)
        self.from_date_entry = tk.Entry(self.frame, width=15)
        self.from_date_entry.pack(side="left", padx=5)
        
        # Set default from date to 30 days ago
        default_from = (datetime.now() - timedelta(days=30)).strftime(DATE_FORMAT)
        self.from_date_entry.insert(0, default_from)
        
        # To date
        tk.Label(self.frame, text="To").pack(side="left", padx=5)
        self.to_date_entry = tk.Entry(self.frame, width=15)
        self.to_date_entry.pack(side="left", padx=5)
        
        # Set default to date to today
        default_to = datetime.now().strftime(DATE_FORMAT)
        self.to_date_entry.insert(0, default_to)
        
        # Quick preset buttons
        tk.Button(
            self.frame, text="This Month", 
            command=self.set_this_month, width=12
        ).pack(side="left", padx=2)
        
        tk.Button(
            self.frame, text="Last Month", 
            command=self.set_last_month, width=12
        ).pack(side="left", padx=2)
        
        tk.Button(
            self.frame, text="Last 30 Days", 
            command=self.set_last_30_days, width=12
        ).pack(side="left", padx=2)
        
        tk.Button(
            self.frame, text="Reset", 
            command=self.reset, width=8
        ).pack(side="left", padx=2)
    
    def set_this_month(self):
        """Set date range to current month."""
        today = datetime.now()
        month_start = datetime(today.year, today.month, 1)
        
        self.from_date_entry.delete(0, tk.END)
        self.from_date_entry.insert(0, month_start.strftime(DATE_FORMAT))
        
        self.to_date_entry.delete(0, tk.END)
        self.to_date_entry.insert(0, today.strftime(DATE_FORMAT))
        
        if self.callback:
            self.callback()
    
    def set_last_month(self):
        """Set date range to last month."""
        today = datetime.now()
        month_start = datetime(today.year, today.month, 1)
        last_month_end = month_start - timedelta(days=1)
        last_month_start = datetime(last_month_end.year, last_month_end.month, 1)
        
        self.from_date_entry.delete(0, tk.END)
        self.from_date_entry.insert(0, last_month_start.strftime(DATE_FORMAT))
        
        self.to_date_entry.delete(0, tk.END)
        self.to_date_entry.insert(0, last_month_end.strftime(DATE_FORMAT))
        
        if self.callback:
            self.callback()
    
    def set_last_30_days(self):
        """Set date range to last 30 days."""
        today = datetime.now()
        thirty_days_ago = today - timedelta(days=30)
        
        self.from_date_entry.delete(0, tk.END)
        self.from_date_entry.insert(0, thirty_days_ago.strftime(DATE_FORMAT))
        
        self.to_date_entry.delete(0, tk.END)
        self.to_date_entry.insert(0, today.strftime(DATE_FORMAT))
        
        if self.callback:
            self.callback()
    
    def reset(self):
        """Reset to default range (last 30 days)."""
        self.set_last_30_days()
    
    def get_range(self):
        """Get the current date range."""
        try:
            from_date = datetime.strptime(self.from_date_entry.get(), DATE_FORMAT)
            to_date = datetime.strptime(self.to_date_entry.get(), DATE_FORMAT)
            return from_date, to_date
        except ValueError:
            return None, None
    
    def pack(self, **kwargs):
        """Pack the frame."""
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Grid the frame."""
        self.frame.grid(**kwargs)


class FilterState:
    """Tracks current filter/search state for exports and reports."""
    
    def __init__(self):
        """Initialize filter state."""
        self.search_keyword = None
        self.status_filter = None
        self.date_range = None  # (from_date, to_date) tuple
        self.view_type = "all"  # "all", "search", "status", "date_range"
    
    def set_search(self, keyword):
        """Set search filter."""
        self.search_keyword = keyword
        self.status_filter = None
        self.date_range = None
        self.view_type = "search" if keyword else "all"
    
    def set_status_filter(self, status):
        """Set status filter."""
        self.status_filter = status
        self.search_keyword = None
        self.date_range = None
        self.view_type = "status" if status else "all"
    
    def set_date_range(self, from_date, to_date):
        """Set date range filter."""
        self.date_range = (from_date, to_date)
        self.search_keyword = None
        self.status_filter = None
        self.view_type = "date_range" if from_date and to_date else "all"
    
    def clear(self):
        """Clear all filters."""
        self.search_keyword = None
        self.status_filter = None
        self.date_range = None
        self.view_type = "all"
    
    def get_sql_clause(self):
        """Get SQL WHERE clause based on current filters."""
        clauses = []
        params = []
        
        if self.view_type == "search" and self.search_keyword:
            wildcard = f"%{self.search_keyword}%"
            search_clause = """
                (client LIKE ? OR category LIKE ? OR summary LIKE ? 
                 OR status LIKE ? OR requested_by LIKE ?)
            """
            clauses.append(search_clause)
            params.extend([wildcard] * 5)
        
        elif self.view_type == "status" and self.status_filter:
            clauses.append("status = ?")
            params.append(self.status_filter)
        
        elif self.view_type == "date_range" and self.date_range:
            from_date, to_date = self.date_range
            clauses.append("date BETWEEN ? AND ?")
            params.append(from_date.strftime(DATE_FORMAT))
            params.append(to_date.strftime(DATE_FORMAT))
        
        if clauses:
            where_clause = " AND ".join([f"({c})" for c in clauses])
            return f"WHERE {where_clause}", params
        
        return "", []
