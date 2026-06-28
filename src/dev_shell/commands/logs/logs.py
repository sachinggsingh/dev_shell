"""Log viewing commands."""

from dev_shell.utils import Formatter, Validator

_VALIDATOR = Validator()


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
        with open(filename, "r", encoding="utf-8") as file:
            print(file.read())
    except Exception as e:
        print(Formatter.highlight_error(f"Error reading file: {e}"))
