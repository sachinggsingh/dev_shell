"""Directory tree visualization."""

import os

from dev_shell.utils import Validator

_VALIDATOR = Validator()


def tree(args):
    """Print a directory tree.

    Usage: tree [path] [-d]
    """
    flags = [arg for arg in args if arg.startswith("-")]
    paths = [arg for arg in args if not arg.startswith("-")]
    path = paths[0] if paths else "."
    directories_only = "-d" in flags

    if not _VALIDATOR.is_valid_path(path):
        print(f"tree: no such file or directory: {path}")
        return

    def _print_tree(base, prefix=""):
        try:
            entries = sorted(os.listdir(base))
            if directories_only:
                entries = [
                    entry for entry in entries
                    if os.path.isdir(os.path.join(base, entry))
                ]
        except Exception as e:
            print(prefix + f"[error opening dir] {e}")
            return

        for i, entry in enumerate(entries):
            path_entry = os.path.join(base, entry)
            connector = "└── " if i == len(entries) - 1 else "├── "
            print(prefix + connector + entry)
            if os.path.isdir(path_entry):
                extension = "    " if i == len(entries) - 1 else "│   "
                _print_tree(path_entry, prefix + extension)

    print(path)
    _print_tree(path)
