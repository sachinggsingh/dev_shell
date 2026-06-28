"""Read file contents."""

import os
from collections import deque

from dev_shell.utils import Formatter

from ._shared import VALIDATOR


def cat(args):
    """Show the content of a file."""
    if not args:
        print("Usage: cat <filename>")
        return

    filename = args[0]
    if not VALIDATOR.is_file(filename):
        print(Formatter.highlight_error(f"File not found: {filename}"))
        return

    try:
        with open(filename, "r", encoding="utf-8") as file:
            print(file.read())
    except Exception as e:
        print(Formatter.highlight_error(f"Error reading file: {e}"))


def head(args):
    """Show first N lines of a file.

    Usage:
        head <file>
        head <file> -n 20
    """
    if not args:
        print("Usage: head <file> [-n lines]")
        return

    filename = args[0]
    lines_count = 10

    if "-n" in args:
        try:
            idx = args.index("-n")
            lines_count = int(args[idx + 1])
        except (ValueError, IndexError):
            print("Invalid value for -n")
            return

    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for i, line in enumerate(file):
                if i >= lines_count:
                    break
                print(line.rstrip())
    except Exception as e:
        print(f"Error: {e}")


def tail(args):
    """Show last N lines of a file.

    Usage:
        tail <file>
        tail <file> -n 20
    """
    if not args:
        print("Usage: tail <file> [-n lines]")
        return

    filename = args[0]
    lines_count = 10

    if "-n" in args:
        try:
            idx = args.index("-n")
            lines_count = int(args[idx + 1])
        except (ValueError, IndexError):
            print("Invalid value for -n")
            return

    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return

    try:
        with open(filename, "r", encoding="utf-8") as file:
            last_lines = deque(file, maxlen=lines_count)

        for line in last_lines:
            print(line.rstrip())
    except Exception as e:
        print(f"Error: {e}")
