"""Copy, move, and rename files."""

import os
import shutil


def move(args):
    """Move a file or directory.

    Usage: move <source> <destination>
    """
    if len(args) != 2:
        print("Usage: move <source> <destination>")
        return

    source, destination = args[0], args[1]

    if not os.path.exists(source):
        print(f"Source not found: {source}")
        return

    try:
        shutil.move(source, destination)
        print(f"Moved '{source}' -> '{destination}'")
    except PermissionError:
        print("Permission denied")
    except FileNotFoundError:
        print(f"Source not found: {source}")
    except Exception as e:
        print(f"Error moving file: {e}")


def cp(args):
    """Copy a file or directory.

    Usage: copy <source> <destination>
    """
    if len(args) != 2:
        print("Usage: copy <source> <destination>")
        return

    source, destination = args[0], args[1]

    if not os.path.exists(source):
        print(f"Source not found: {source}")
        return

    try:
        if os.path.isdir(source):
            shutil.copytree(source, destination)
        else:
            shutil.copy(source, destination)
        print(f"Copied '{source}' -> '{destination}'")
    except PermissionError:
        print("Permission denied")
    except FileNotFoundError:
        print(f"Source not found: {source}")
    except Exception as e:
        print(f"Error copying file: {e}")


def rename(args):
    """Rename a file.

    Usage: rename <old_file> <new_file>
    """
    if len(args) < 2:
        print(
            "Usage:\n"
            "  rename <old_file> <new_file>\n"
            "  rename ext <old_ext> <new_ext>\n"
            "  rename text <old> <new>\n"
            "  rename prefix <prefix>\n"
            "  rename suffix <suffix>"
        )
        return

    mode = args[0]

    if mode in ("ext", "text", "prefix", "suffix"):
        print("Batch rename modes are not yet implemented.")
        return

    if len(args) != 2:
        print("Usage: rename <old_file> <new_file>")
        return

    old_name, new_name = args[0], args[1]

    if not os.path.exists(old_name):
        print(f"File not found: {old_name}")
        return

    if os.path.exists(new_name):
        print(f"'{new_name}' already exists.")
        return

    try:
        os.rename(old_name, new_name)
        print(f"Renamed '{old_name}' -> '{new_name}'")
    except Exception as e:
        print(f"Error: {e}")
