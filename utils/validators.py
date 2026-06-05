"""Input validation utilities."""
import os


class Validator:
    """Utilities for validating user inputs and paths."""

    @staticmethod
    def is_valid_path(path):
        """Check if path exists and is accessible.
        
        Args:
            path: Path to validate
            
        Returns:
            bool: True if path is valid, False otherwise
        """
        try:
            return os.path.exists(path)
        except (OSError, ValueError):
            return False

    @staticmethod
    def is_file(path):
        """Check if path is a file.
        
        Args:
            path: Path to check
            
        Returns:
            bool: True if path is a file, False otherwise
        """
        try:
            return os.path.isfile(path)
        except (OSError, ValueError):
            return False

    @staticmethod
    def is_directory(path):
        """Check if path is a directory.
        
        Args:
            path: Path to check
            
        Returns:
            bool: True if path is a directory, False otherwise
        """
        try:
            return os.path.isdir(path)
        except (OSError, ValueError):
            return False

    @staticmethod
    def is_readable(path):
        """Check if path is readable.
        
        Args:
            path: Path to check
            
        Returns:
            bool: True if path is readable, False otherwise
        """
        try:
            return os.access(path, os.R_OK)
        except (OSError, ValueError):
            return False

    @staticmethod
    def is_writable(path):
        """Check if path is writable.
        
        Args:
            path: Path to check
            
        Returns:
            bool: True if path is writable, False otherwise
        """
        try:
            return os.access(path, os.W_OK)
        except (OSError, ValueError):
            return False

    @staticmethod
    def validate_filename(filename):
        """Validate filename format.
        
        Args:
            filename: Filename to validate
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not filename:
            return False, "Filename cannot be empty"
        
        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        if any(char in filename for char in invalid_chars):
            return False, f"Filename contains invalid characters: {', '.join(invalid_chars)}"
        
        return True, ""
