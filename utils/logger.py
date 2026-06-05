"""Logging utilities for the shell."""
import os
from datetime import datetime


class Logger:
    """Simple logging utility for shell operations."""

    def __init__(self, log_file=None):
        """Initialize logger with optional log file.
        
        Args:
            log_file: Path to log file (optional)
        """
        self.log_file = log_file
        self.logs = []

    def log(self, level, message):
        """Log a message with timestamp.
        
        Args:
            level: Log level (INFO, WARNING, ERROR, DEBUG)
            message: Message to log
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        self.logs.append(log_entry)
        
        if self.log_file:
            try:
                with open(self.log_file, "a") as f:
                    f.write(log_entry + "\n")
            except Exception as e:
                print(f"Failed to write to log file: {e}")

    def info(self, message):
        """Log info level message."""
        self.log("INFO", message)

    def warning(self, message):
        """Log warning level message."""
        self.log("WARNING", message)

    def error(self, message):
        """Log error level message."""
        self.log("ERROR", message)

    def debug(self, message):
        """Log debug level message."""
        self.log("DEBUG", message)

    def get_logs(self):
        """Get all logged messages."""
        return self.logs
