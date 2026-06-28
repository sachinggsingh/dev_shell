"""Directory create and remove commands."""

import os
import shutil


def mkdir(args):
    """Create a new directory.

    Usage: mkdir <folder_name> [-p]
    """
    flags = [arg for arg in args if arg.startswith("-")]
    paths = [arg for arg in args if not arg.startswith("-")]

    if not paths:
        print("Usage: mkdir <folder_name> [-p]")
        return

    target = paths[0]
    parents = "-p" in flags

    try:
        if parents:
            os.makedirs(target, exist_ok=True)
        else:
            os.mkdir(target)
        print(f"Created folder: {target}")
    except FileExistsError:
        print(f"mkdir: cannot create directory '{target}': File exists")
    except Exception as e:
        print(f"Error creating directory: {e}")


def rmdir(args):
    """Remove a directory.

    Usage: rmdir <folder_name> [-r]
    """
    if not args:
        print("Usage: rmdir <folder_name>")
        return

    target = args[0]
    recursive = "-r" in args or "--recursive" in args

    if recursive:
        try:
            shutil.rmtree(target)
            print(f"Removed folder (recursively): {target}")
        except Exception as e:
            print(f"Error removing folder: {e}")
    else:
        try:
            os.rmdir(target)
            print(f"Removed folder: {target}")
        except OSError:
            print(
                f"rmdir: '{target}' is not empty. "
                "Use 'rmdir -r <folder>' to remove recursively."
            )
