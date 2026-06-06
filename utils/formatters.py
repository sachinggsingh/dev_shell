"""Output formatting utilities."""
import os


class Formatter:
    """Utilities for formatting output."""

    @staticmethod
    def format_file_size(size_bytes):
        """Format byte size to human-readable format.
        
        Args:
            size_bytes: Size in bytes
            
        Returns:
            str: Formatted size (e.g., "1.5 MB")
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"

    @staticmethod
    def format_directory_listing(path, detailed=False):
        """Format directory listing output.
        
        Args:
            path: Directory path
            detailed: Include file sizes and types if True
            
        Returns:
            str: Formatted directory listing
        """
        try:
            items = os.listdir(path)
            output = []
            
            for item in sorted(items):
                item_path = os.path.join(path, item)
                
                if detailed:
                    if os.path.isdir(item_path):
                        output.append(f"[DIR]  {item}")
                    else:
                        size = os.path.getsize(item_path)
                        formatted_size = Formatter.format_file_size(size)
                        output.append(f"[FILE] {item:<30} {formatted_size:>10}")
                else:
                    output.append(item)
            
            return "\n".join(output)
        except Exception as e:
            return f"Error listing directory: {e}"

    @staticmethod
    def format_table(headers, rows):
        """Format data as a table.
        
        Args:
            headers: List of column headers
            rows: List of rows (each row is a list of values)
            
        Returns:
            str: Formatted table
        """
        if not rows:
            return "No data to display"
        
        col_widths = [len(header) for header in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))
        
        header_row = " | ".join(
            str(h).ljust(col_widths[i]) for i, h in enumerate(headers)
        )
        separator = "-+-".join("-" * width for width in col_widths)
        
        output = [header_row, separator]
        for row in rows:
            output.append(" | ".join(
                str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)
            ))
        
        return "\n".join(output)

    @staticmethod
    def format_item_details(item_type, path):
        """Format detailed information about a file or directory.
        
        Args:
            item_type: Type of the item (e.g., 'FILE' or 'DIR')
            path: Path to the item
            
        Returns:
            str: Formatted details
        """
        try:
            lines = [
                "\n" + "=" * 50,
                f"Path : {path}",
                f"Type : {item_type}"
            ]
            
            if os.path.isfile(path):
                size = os.path.getsize(path)
                lines.append(f"Size : {Formatter.format_file_size(size)}")
            else:
                lines.append("Size : N/A")
                
            return "\n".join(lines)
        except OSError as e:
            return f"Error reading {path}: {e}"

    @staticmethod
    def highlight_error(message):
        """Format error message with highlighting.
        
        Args:
            message: Error message
            
        Returns:
            str: Formatted error message
        """
        return f" ERROR: {message}"

    @staticmethod
    def highlight_success(message):
        """Format success message with highlighting.
        
        Args:
            message: Success message
            
        Returns:
            str: Formatted success message
        """
        return f" SUCCESS: {message}"

    @staticmethod
    def highlight_warning(message):
        """Format warning message with highlighting.
        
        Args:
            message: Warning message
            
        Returns:
            str: Formatted warning message
        """
        return f" WARNING: {message}"
