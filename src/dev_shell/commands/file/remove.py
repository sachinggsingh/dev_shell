"""Remove files."""

import os

from dev_shell.utils import Formatter

from ._shared import VALIDATOR


def rm(args):
    """Remove a file.

    Usage: rm <file_name> [-f]
    """
    if not args:
        print("Usage: rm <file_name> [-f]")
        return

    force = "-f" in args
    filename = next((a for a in args if not a.startswith("-")), None)

    if not filename:
        print("Usage: rm <file_name> [-f]")
        return

    if not VALIDATOR.is_file(filename):
        msg = f"File not found: {filename}"
        if force:
            return
        print(Formatter.highlight_error(msg))
        return

    try:
        os.remove(filename)
        print(Formatter.highlight_success(f"Removed file: {filename}"))
    except Exception as e:
        print(Formatter.highlight_error(f"Error removing file: {e}"))
