"""File manipulation commands."""
import os
import subprocess
import shutil
from utils import Formatter, Validator

_VALIDATOR = Validator()

# File Management

# Advanced File Operations
# ──────────────────────────────────────
# [ ] cp           # Copy files/directories
# [ ] mv           # Move/Rename files/directories
# [ ] cat          # Display file contents
# [ ] head         # Show first N lines of file
# [ ] tail         # Show last N lines of file
# [ ] grep         # Search text inside files
# [ ] stat         # Show detailed file metadata
# [ ] checksum     # Generate SHA256/MD5 hash
# [ ] diff         # Compare two files

# Batch File Operations
# ──────────────────────────────────────
# [ ] rename       # Batch rename files
# [ ] chmod-many   # Change permissions for multiple files
# [ ] compress-many# Compress multiple files/directories

# DevOps / Software Engineer Priority
# ──────────────────────────────────────
# Must Have
# [ ] cat
# [ ] grep
# [ ] tail
# [ ] cp
# [ ] mv
# [ ] stat
# [ ] checksum

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
        
        Usage: ls [path] [-a] [-l] [-h] [-d]
        """
        flag_chars = set()
        for arg in args:
            if arg.startswith("-"):
                flag_chars.update(arg[1:])
                
        paths = [arg for arg in args if not arg.startswith("-")]
        path = paths[0] if paths else "."

        if not _VALIDATOR.is_valid_path(path):
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
                entries = [entry for entry in entries if os.path.isdir(os.path.join(path, entry))]

            if long_format:
                for entry in entries:
                    entry_path = os.path.join(path, entry)
                    
                    readable = "Yes" if os.access(entry_path, os.R_OK) else "No"
                    writable = "Yes" if os.access(entry_path, os.W_OK) else "No"
                    executable = "Yes" if os.access(entry_path, os.X_OK) else "No"
                    perms = f"Readable: {readable:<3} Writable: {writable:<3} Executable: {executable:<3}"
                    
                    size = os.path.getsize(entry_path) if os.path.isfile(entry_path) else 0
                    
                    if human_readable:
                        size_str = Formatter.format_file_size(size)
                    else:
                        size_str = str(size)
                        
                    print(f"[{perms}] {size_str:>10}  {entry}")
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

    @staticmethod
    def find(args):
        """
        Search for files and directories recursively.

        Usage:
            find <name>
            find <name> -f
            find <name> -d
            find <name> -l

        Examples:
            find shell
            find shell -f
            find shell -d
            find shell -l
            find shell -f -l
        """

        if not args:
            print(
                "Usage: find <name> "
                "[-f] [-d] [-l]"
            )
            return

        files_only = "-f" in args
        dirs_only = "-d" in args
        long_format = "-l" in args

        search_term = next(
            (
                arg
                for arg in args
                if not arg.startswith("-")
            ),
            None
        )

        if not search_term:
            print("Search term required.")
            return

        search_term = search_term.lower()

        IGNORE_DIRS = {
            ".venv",
            "venv",
            "__pycache__",
            ".git",
            "node_modules",
            ".idea",
            ".vscode"
        }

        matches = []

        for root, dirs, files in os.walk("."):

            dirs[:] = [
                d
                for d in dirs
                if d not in IGNORE_DIRS
            ]

            # Search directories
            if not files_only:

                for directory in dirs:

                    if (
                        search_term
                        in directory.lower()
                    ):

                        matches.append(
                            (
                                "DIR",
                                os.path.join(
                                    root,
                                    directory
                                )
                            )
                        )

            # Search files
            if not dirs_only:

                for file in files:

                    if (
                        search_term
                        in file.lower()
                    ):

                        matches.append(
                            (
                                "FILE",
                                os.path.join(
                                    root,
                                    file
                                )
                            )
                        )

        if not matches:

            print(
                f"No matches found for "
                f"'{search_term}'"
            )
            
            return
        
        print(
            f"\nFound "
            f"{len(matches)} "
            f"match(es):\n"
        )

        for item_type, path in matches:

            if long_format:

                print(
                    Formatter.format_item_details(
                        item_type,
                        path
                    )
                )

            else:

                print(
                    f"[{item_type}] {path}"
                )

    @staticmethod
    def edit(args):

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
            subprocess.run([editor, file_name])

        except FileNotFoundError:
            print(
                f"{editor} is not installed or not available in PATH"
            )