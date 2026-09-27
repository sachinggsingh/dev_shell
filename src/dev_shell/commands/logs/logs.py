"""Log viewing commands."""

from dev_shell.commands.file._shared import read_file


def logs(args):
    """Display the contents of a file.

    Usage:
        logs <filename>
    """
    if not args:
        print("Usage: logs <filename>")
        return

    read_file(args[0])
