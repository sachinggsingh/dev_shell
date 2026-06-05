"""File manipulation commands."""
import os
from utils import Formatter, Validator

_VALIDATOR = Validator()


class FileCommands:
    """Handles file-related shell commands."""

    @staticmethod
    def touch(args):
        """Create or update a file.
        
        Usage: touch <file_name>
        """
        if not args:
            print("Usage: touch <file_name>")
            return

        file_name = args[0]
        valid, error = _VALIDATOR.validate_filename(os.path.basename(file_name))
        if not valid:
            print(Formatter.highlight_error(error))
            return

        try:
            if os.path.exists(file_name):
                raise FileExistsError(f"touch: '{file_name}' already exists.")
            with open(file_name, "a"):
                os.utime(file_name, None)
            print(f"Touched file: {file_name}")
        except FileExistsError as e:
            print(Formatter.highlight_error(str(e)))
        except Exception as e:
            print(Formatter.highlight_error(f"Error touching file: {e}"))

    @staticmethod
    def ls(args):
        """List files and folders in a directory.
        
        Usage: ls [path] [-a] [-l] [-d]
        """
        flags = [arg for arg in args if arg.startswith("-")]
        paths = [arg for arg in args if not arg.startswith("-")]
        path = paths[0] if paths else "."

        if not _VALIDATOR.is_valid_path(path):
            print(Formatter.highlight_error(f"ls: no such directory: {path}"))
            return

        include_hidden = "-a" in flags
        directories_only = "-d" in flags
        long_format = "-l" in flags

        try:
            entries = sorted(os.listdir(path))
            if not include_hidden:
                entries = [entry for entry in entries if not entry.startswith(".")]

            if directories_only:
                entries = [entry for entry in entries if os.path.isdir(os.path.join(path, entry))]

            if long_format:
                for entry in entries:
                    entry_path = os.path.join(path, entry)
                    entry_type = "<DIR>" if os.path.isdir(entry_path) else "<FILE>"
                    size = os.path.getsize(entry_path) if os.path.isfile(entry_path) else 0
                    print(f"{entry_type:6} {Formatter.format_file_size(size):>10}  {entry}")
            else:
                for entry in entries:
                    print(entry)
        except NotADirectoryError:
            print(Formatter.highlight_error(f"ls: not a directory: {path}"))
        except Exception as e:
            print(Formatter.highlight_error(f"Error listing directory: {e}"))

    @staticmethod
    def cat(args):
        """Show the content of a file."""
        if not args:
            print("Usage: cat <filename>")
            return

        filename = args[0]
        if not _VALIDATOR.is_file(filename):
            print(Formatter.highlight_error(f"File not found: {filename}"))
            return

        try:
            with open(filename, "r") as file:
                print(file.read())
        except Exception as e:
            print(Formatter.highlight_error(f"Error reading file: {e}"))

    @staticmethod
    def rm(args):
        """Remove a file.

        Usage: rm <file_name> [-f]
        """
        if not args:
            print("Usage: rm <file_name> [-f]")
            return

        force = "-f" in args
        # first non-flag arg is filename
        filename = next((a for a in args if not a.startswith("-")), None)

        if not filename:
            print("Usage: rm <file_name> [-f]")
            return

        if not _VALIDATOR.is_file(filename):
            msg = f"File not found: {filename}"
            if force:
                return
            print(Formatter.highlight_error(msg))
            return

        try:
            os.remove(filename)
            print(Formatter.highlight_success(f"Removed file: {filename}"))
        except Exception as e:
            print(Formatter.highlight_error(f"Error removing file: {e}"))
    
    @staticmethod
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
