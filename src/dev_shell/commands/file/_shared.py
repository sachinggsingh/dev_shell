"""Shared helpers for file commands."""

from dev_shell.utils import Formatter, Validator

VALIDATOR = Validator()


def read_file(filename):
    """Validate and print the contents of a file."""
    if not VALIDATOR.is_file(filename):
        print(Formatter.highlight_error(f"File not found: {filename}"))
        return

    try:
        with open(filename, encoding="utf-8") as file:
            print(file.read())
    except OSError as error:
        print(Formatter.highlight_error(f"Error reading file: {error}"))
