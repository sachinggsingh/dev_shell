"""Directory navigation commands."""

import os


def pwd(args):
    """Print the current working directory.

    Usage: pwd
    """
    print(os.getcwd())


def cd(args):
    """Change the current directory.

    Usage: cd <folder_name>
    """
    if not args:
        print("Usage: cd <folder_name>")
        return

    try:
        os.chdir(args[0])
        print(f"Current directory: {os.getcwd()}")
    except FileNotFoundError:
        print(f"cd: no such directory: {args[0]}")
    except NotADirectoryError:
        print(f"cd: not a directory: {args[0]}")
