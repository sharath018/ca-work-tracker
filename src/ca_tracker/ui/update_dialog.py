"""Update check UI dialog for CA Work Tracker."""

import tkinter as tk
from tkinter import messagebox
import webbrowser
from datetime import datetime


class UpdateCheckWindow:
    """Dialog for displaying version update information."""

    def __init__(self, parent, current_version, latest_version, release_url, release_notes=None):
        """
        Initialize update check window.

        Args:
            parent: Parent window
            current_version: Current version string
            latest_version: Latest available version string
            release_url: URL to GitHub release page
            release_notes: Optional release notes text
        """
        self.window = tk.Toplevel(parent)
        self.window.title("CA Work Tracker - Update Available")
        self.window.geometry("600x400")
        self.window.resizable(False, False)

        self.current_version = current_version
        self.latest_version = latest_version
        self.release_url = release_url
        self.release_notes = release_notes

        self.create_ui()

    def create_ui(self):
        """Create the update dialog UI."""
        # Header
        header_frame = tk.Frame(self.window, bg="#4CAF50", height=80)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="Update Available!",
            font=("Arial", 16, "bold"),
            bg="#4CAF50",
            fg="white",
        )
        title_label.pack(pady=10)

        subtitle_label = tk.Label(
            header_frame,
            text=f"Version {self.latest_version} is now available (you have {self.current_version})",
            font=("Arial", 10),
            bg="#4CAF50",
            fg="white",
        )
        subtitle_label.pack(pady=5)

        # Content
        content_frame = tk.Frame(self.window)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Release notes
        if self.release_notes:
            tk.Label(content_frame, text="Release Notes:", font=("Arial", 10, "bold")).pack(
                anchor="w", pady=(0, 5)
            )

            notes_frame = tk.Frame(content_frame)
            notes_frame.pack(fill="both", expand=True, padx=0, pady=(0, 15))

            scrollbar = tk.Scrollbar(notes_frame)
            scrollbar.pack(side="right", fill="y")

            notes_text = tk.Text(notes_frame, font=("Courier", 9), yscrollcommand=scrollbar.set)
            notes_text.pack(side="left", fill="both", expand=True)
            scrollbar.config(command=notes_text.yview)

            notes_text.insert("1.0", self.release_notes)
            notes_text.config(state="disabled")

        # Buttons
        button_frame = tk.Frame(content_frame)
        button_frame.pack(fill="x", pady=(10, 0))

        tk.Button(
            button_frame,
            text="Download Update",
            command=self.open_release_url,
            bg="#4CAF50",
            fg="white",
            width=20,
        ).pack(side="left", padx=5)

        tk.Button(button_frame, text="Remind Later", command=self.window.destroy, width=15).pack(
            side="left", padx=5
        )

        tk.Button(button_frame, text="Skip This Version", command=self.skip_version, width=15).pack(
            side="left", padx=5
        )

    def open_release_url(self):
        """Open the release URL in default browser."""
        try:
            webbrowser.open(self.release_url)
            self.window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open browser: {e}")

    def skip_version(self):
        """User chose to skip this version."""
        messagebox.showinfo(
            "Skipped",
            f"You can check for updates manually from the Help menu.\n"
            f"Latest version: {self.latest_version}",
        )
        self.window.destroy()


class VersionCheckNoUpdateWindow:
    """Dialog for when no update is available."""

    def __init__(self, parent, current_version):
        """
        Initialize no-update dialog.

        Args:
            parent: Parent window
            current_version: Current version string
        """
        messagebox.showinfo(
            "Version Check",
            f"You are running the latest version ({current_version}).\n\n"
            f"Last checked: {datetime.now().strftime('%d-%b-%Y %H:%M:%S')}",
        )
