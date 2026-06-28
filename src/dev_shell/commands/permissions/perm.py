"""File permission commands."""

import os


def perm(args):
    """Show file permission flags for a path.

    Usage: perm <path>
    """
    if not args:
        print("Usage: perm <path>")
        return

    path = args[0]

    if not os.path.exists(path):
        print("Path does not exist")
        return

    print(f"\nPath: {path}\n")
    print(f"Readable  :   {'Yes' if os.access(path, os.R_OK) else 'No'}")
    print(f"Writable   : {'Yes' if os.access(path, os.W_OK) else 'No'}")
    print(f"Executable : {'Yes' if os.access(path, os.X_OK) else 'No'}")
