"""List directory contents."""

import os

from dev_shell.utils import Formatter

from ._shared import VALIDATOR


def ls(args):
    """List files and folders in a directory.

    Usage: ls [path] [-a] [-l] [-h] [-d]
    """
    flag_chars = set()
    for arg in args:
        if arg.startswith("-"):
            flag_chars.update(arg[1:])

    paths = [arg for arg in args if not arg.startswith("-")]
    path = paths[0] if paths else "."

    if not VALIDATOR.is_valid_path(path):
        print(Formatter.highlight_error(f"ls: no such directory: {path}"))
        return

    include_hidden = "a" in flag_chars
    directories_only = "d" in flag_chars
    long_format = "l" in flag_chars
    human_readable = "h" in flag_chars

    if human_readable and not long_format:
        print(Formatter.highlight_error("ls: -h flag requires -l flag"))
        return

    try:
        entries = sorted(os.listdir(path))
        if not include_hidden:
            entries = [entry for entry in entries if not entry.startswith(".")]

        if directories_only:
            entries = [
                entry for entry in entries
                if os.path.isdir(os.path.join(path, entry))
            ]

        if long_format:
            for entry in entries:
                entry_path = os.path.join(path, entry)

                readable = "Yes" if os.access(entry_path, os.R_OK) else "No"
                writable = "Yes" if os.access(entry_path, os.W_OK) else "No"
                executable = "Yes" if os.access(entry_path, os.X_OK) else "No"
                perms = (
                    f"Readable: {readable:<3} Writable: {writable:<3} "
                    f"Executable: {executable:<3}"
                )

                size = os.path.getsize(entry_path) if os.path.isfile(entry_path) else 0
                size_str = Formatter.format_file_size(size) if human_readable else str(size)

                print(f"[{perms}] {size_str:>10}  {entry}")
        else:
            for entry in entries:
                print(entry)
    except NotADirectoryError:
        print(Formatter.highlight_error(f"ls: not a directory: {path}"))
    except Exception as e:
        print(Formatter.highlight_error(f"Error listing directory: {e}"))
