"""Create and edit files."""

import os
import subprocess

from dev_shell.utils import Formatter

from ._shared import VALIDATOR


def touch(args):
    """Create or update a file.

    Usage: touch <file_name>
    """
    if not args:
        print("Usage: touch <file_name>")
        return

    file_name = args[0]
    valid, error = VALIDATOR.validate_filename(os.path.basename(file_name))
    if not valid:
        print(Formatter.highlight_error(error))
        return

    try:
        if os.path.exists(file_name):
            raise FileExistsError(f"touch: '{file_name}' already exists.")
        with open(file_name, "a", encoding="utf-8"):
            os.utime(file_name, None)
        print(f"Touched file: {file_name}")
    except FileExistsError as e:
        print(Formatter.highlight_error(str(e)))
    except Exception as e:
        print(Formatter.highlight_error(f"Error touching file: {e}"))


def edit(args):
    """Edit a file with vim or nvim.

    Usage: edit <editor-name> <filepath>
    """
    if len(args) < 2:
        print("Usage: edit <vim|nvim> <file>")
        return

    editor = args[0]
    file_name = args[1]

    if editor not in ("vim", "nvim"):
        print("Editor must be either 'vim' or 'nvim'")
        return

    if not os.path.exists(file_name):
        print(f"File not found: {file_name}")
        return

    try:
        subprocess.run([editor, file_name], check=False)
    except FileNotFoundError:
        print(f"{editor} is not installed or not available in PATH")
