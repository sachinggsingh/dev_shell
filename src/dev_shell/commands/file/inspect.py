"""Inspect file metadata and integrity."""

import hashlib
import os
from datetime import datetime

from dev_shell.utils import Formatter


def file_size(args):
    """Show the size of a file.

    Usage: size <file_path>
    """
    if not args:
        print("Usage: size <file_path>")
        return

    path = args[0]
    if not os.path.exists(path):
        print(Formatter.highlight_error("Path not found"))
        return

    try:
        size = os.path.getsize(path)
        print(f"{path}: {Formatter.format_file_size(size)}")
    except Exception as e:
        print(Formatter.highlight_error(f"Error reading size: {e}"))


def stat(args):
    """Show detailed file metadata.

    Usage: stat <file>
    """
    if not args:
        print("Usage: stat <file>")
        return

    filename = args[0]

    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return

    try:
        stat_info = os.stat(filename)

        print(f"File: {filename}")
        print(f"Size: {stat_info.st_size} bytes")
        print(f"Last modified: {datetime.fromtimestamp(stat_info.st_mtime)}")
        print(f"Last accessed: {datetime.fromtimestamp(stat_info.st_atime)}")
        print(f"Created: {datetime.fromtimestamp(stat_info.st_ctime)}")
        print(f"Permissions: {stat_info.st_mode}")
        print(f"Owner: {stat_info.st_uid}")
        print(f"Group: {stat_info.st_gid}")
    except Exception as e:
        print(f"Error: {e}")


def checksum(args):
    """Calculate checksum of a file.

    Usage: checksum <file>
    """
    if not args:
        print("Usage: checksum <file>")
        return

    filename = args[0]

    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return

    try:
        with open(filename, "rb") as file:
            print(hashlib.sha256(file.read()).hexdigest())
    except Exception as e:
        print(f"Error: {e}")


def diff(args):
    """Compare two files.

    Usage: diff <file1> <file2>
    """
    if len(args) != 2:
        print("Usage: diff <file1> <file2>")
        return

    file1, file2 = args[0], args[1]

    if not os.path.exists(file1):
        print(f"File not found: {file1}")
        return

    if not os.path.exists(file2):
        print(f"File not found: {file2}")
        return

    try:
        with open(file1, "r", encoding="utf-8") as f1, open(
            file2, "r", encoding="utf-8"
        ) as f2:
            for i, (line1, line2) in enumerate(zip(f1, f2)):
                if line1 != line2:
                    print(f"{i + 1}: {line1.rstrip()} != {line2.rstrip()}")
    except Exception as e:
        print(f"Error: {e}")
