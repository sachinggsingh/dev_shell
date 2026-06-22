"""File manipulation commands."""
import os
import subprocess
import shutil
from utils import Formatter, Validator
from collections import deque
from datetime import datetime
import hashlib


_VALIDATOR = Validator()

# File Management

# Advanced File Operations
# ──────────────────────────────────────
# [x] cp           # Copy files/directories
# [x] mv           # Move/Rename files/directories
# [x] cat          # Display file contents
# [x] head         # Show first N lines of file
# [x] tail         # Show last N lines of file
# [x] grep         # Search text inside files
# [x] stat         # Show detailed file metadata
# [x] checksum     # Generate SHA256/MD5 hash
# [x] diff         # Compare two files

# Batch File Operations
# ──────────────────────────────────────
# [ ] rename       # Batch rename files
# [ ] chmod-many   # Change permissions for multiple files
# [ ] compress-many# Compress multiple files/directories

# DevOps / Software Engineer Priority
# ──────────────────────────────────────
# Must Have
# [x] cat
# [x] grep
# [x] tail
# [x] cp
# [x] mv
# [x] head
# [x] stat
# [x] checksum
# [x] diff

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
        """
        Edit a file
        edit <editor-name> <filepath>
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
            subprocess.run([editor, file_name])

        except FileNotFoundError:
            print(
                f"{editor} is not installed or not available in PATH"
            )
    @staticmethod
    def move(args):
        """
        Move command
        Usage move <file_path> <destination_path>
        """

        if len(args) != 2:
            print("Usage: move <source> <destination>")
            return

        source = args[0]
        destination = args[1]

        if not os.path.exists(source):
            print(f"Source not found: {source}")
            return

        try:
            shutil.move(source, destination)
            print(
                f"Moved '{source}' -> '{destination}'"
            )
        except PermissionError:
            print(
                "Permission denied"
            )
        except FileNotFoundError:
            print(
                f"Source not found: {source}"
            )
        except Exception as e:
            print(
                f"Error moving file: {e}"
            )

    @staticmethod
    def cp(args):
        """
         copy command
        Usage copy <file_path> <destination_path>

        """
        if len(args) != 2:
            print("Usage: move <source> <destination>")
            return
        
        source = args[0]
        destination = args[1]

        if not os.path.exists(source):
            print(f"Source not found: {source}")
            return

        try:
            shutil.copy(source, destination)
            print(
                f"Moved '{source}' -> '{destination}'"
            )
        except PermissionError:
            print(
                "Permission denied"
            )
        except FileNotFoundError:
            print(
                f"Source not found: {source}"
            )
        except Exception as e:
            print(
                f"Error moving file: {e}"
            )
        
    @staticmethod
    def head(args):
        """
        Show first N lines of a file.

        Usage:
            head <file>
            head <file> -n 20
        """

        if not args:
            print("Usage: head <file> [-n lines]")
            return

        filename = args[0]
        lines_count = 10

        if "-n" in args:

            try:
                idx = args.index("-n")

                lines_count = int(
                    args[idx + 1]
                )

            except (
                ValueError,
                IndexError
            ):
                print(
                    "Invalid value for -n"
                )
                return

        if not os.path.exists(filename):
            print(
                f"File not found: {filename}"
            )
            return

        try:

            with open(
                filename,
                "r"
            ) as file:

                for i, line in enumerate(file):

                    if i >= lines_count:
                        break

                    print(
                        line.rstrip()
                    )

        except Exception as e:

            print(
                f"Error: {e}"
            )

    @staticmethod
    def tail(args):
        """
        Show last N lines of a file.

        Usage:
            tail <file>
            tail <file> -n 20
        """

        if not args:
            print("Usage: tail <file> [-n lines]")
            return

        filename = args[0]
        lines_count = 10

        if "-n" in args:

            try:
                idx = args.index("-n")

                lines_count = int(
                    args[idx + 1]
                )

            except (
                ValueError,
                IndexError
            ):
                print(
                    "Invalid value for -n"
                )
                return

        if not os.path.exists(filename):
            print(
                f"File not found: {filename}"
            )
            return

        try:

            with open(
                filename,
                "r"
            ) as file:

                last_lines = deque(
                    file,
                    maxlen=lines_count
                )

            for line in last_lines:

                print(
                    line.rstrip()
                )

        except Exception as e:

            print(
                f"Error: {e}"
            )


    @staticmethod
    def grep(args):
        """
        Usage:
        grep <pattern> <file>
        grep <pattern> <file> -i
        grep <pattern> <file> -n
        grep <pattern> <file> -c
        grep <pattern> <file> -v
        grep <pattern> <directory> -r
        """

        if len(args) < 2:
            print(
                "Usage: grep <pattern> <file> "
                "[-i] [-n] [-c] [-v] [-r]"
            )
            return

        pattern = args[0]
        target = args[1]

        ignore_case = "-i" in args
        show_line_numbers = "-n" in args
        count_only = "-c" in args
        invert_match = "-v" in args
        recursive = "-r" in args

        matches = 0

        def process_file(filename):

            nonlocal matches

            try:

                with open(
                    filename,
                    "r",
                    encoding="utf-8",
            errors="ignore"
                ) as file:

                    for line_number, line in enumerate(
                        file,
                          start=1
                    ):

                        content = line.rstrip()

                        if ignore_case:

                            found = (
                                pattern.lower()
                                in content.lower()
                            )

                        else:

                            found = (
                                pattern
                                in content
                            )

                        if invert_match:
                            found = not found

                        if found:

                            matches += 1

                            if count_only:
                                continue

                            if show_line_numbers:

                                print(
                                    f"{line_number}: "
                                    f"{content}"
                                )

                            else:

                                print(content)

            except Exception as e:

                print(
                    f"Error reading "
                    f"{filename}: {e}"
                )

        if recursive:
    
            if not os.path.isdir(target):

                print(
                    f"Directory not found: "
                    f"{target}"
                )

                return

            for root, _, files in os.walk(
                target
            ):

                for file in files:

                    process_file(
                        os.path.join(
                            root,
                            file
                        )
                    )

        else:

            if not os.path.exists(target):

                print(
                    f"File not found: "
                    f"{target}"
                )

                return

            process_file(target)

        if count_only:

            print(
                f"Total matches: "
                f"{matches}"
            )



#  Can be improved better , we can add more details about the file permissions , file size etc in good format and meaningful way
    @staticmethod
    def stat(args):
        """
        Show detailed file metadata.

        Usage:
            stat <file>
        """

        if not args:
            print("Usage: stat <file>")
            return

        filename = args[0]

        if not os.path.exists(filename):
            print(
                f"File not found: {filename}"
            )
            return

        try:
            stat_info = os.stat(filename)
            
            print(
                f"File: {filename}"
            )
            print(
                f"Size: {stat_info.st_size} bytes"
            )
            print(
                f"Last modified: {datetime.fromtimestamp(stat_info.st_mtime)}"
            )
            print(
                f"Last accessed: {datetime.fromtimestamp(stat_info.st_atime)}"
            )
            print(
                f"Created: {datetime.fromtimestamp(stat_info.st_ctime)}"
            )
            print(
                f"Permissions: {stat_info.st_mode}"
            )
            print(
                f"Owner: {stat_info.st_uid}"
            )
            print(
                f"Group: {stat_info.st_gid}"
            )
            print(
                f"File type: {stat_info.st_mode}"
            )

        except Exception as e:
            print(
                f"Error: {e}"
            )

    @staticmethod
    def checksum(args):
        """
        Calculate checksum of a file.

        Usage:
            checksum <file>
        """

        if not args:
            print("Usage: checksum <file>")
            return

        filename = args[0]

        if not os.path.exists(filename):
            print(
                f"File not found: {filename}"
            )
            return

        try:
            with open(
                filename,
                "rb"
            ) as file:
                checksum = hashlib.sha256(file.read()).hexdigest()
                print(checksum)
        except Exception as e:
            print(
                f"Error: {e}"
            )

    @staticmethod
    def diff(args):
        """
        Compare two files.

        Usage:
            diff <file1> <file2>
        """

        if len(args) != 2:
            print("Usage: diff <file1> <file2>")
            return

        file1 = args[0]
        file2 = args[1]

        if not os.path.exists(file1):
            print(
                f"File not found: {file1}"
            )
            return

        if not os.path.exists(file2):
            print(
                f"File not found: {file2}"
            )
            return

        try:

            with open(
                file1,
                "r"
            ) as f1, open(
                file2,
                "r"
            ) as f2:

                for i, (line1, line2) in enumerate(
                    zip(
                        f1,
                        f2
                    )
                ):

                    if line1 != line2:

                        print(
                            f"{i+1}: "
                            f"{line1.rstrip()} != "
                            f"{line2.rstrip()}"
                        )

        except Exception as e:

            print(
                f"Error: {e}"
            )