"""Log viewing commands."""
from utils import Formatter, Validator

_VALIDATOR = Validator()


class LogCommands:
    """Handles log-related shell commands."""

    @staticmethod
    def logs(args):
        """Display the contents of a file.
        
        Usage: logs <filename>
        """
        if not args:
            print("Usage: logs <filename>")
            return

        filename = args[0]

        if not _VALIDATOR.is_file(filename):
            print(Formatter.highlight_error(f"File not found: {filename}"))
            return

        try:
            with open(filename, "r") as file:
                print(file.read())
        except Exception as e:
            print(Formatter.highlight_error(f"Error reading file: {e}"))
