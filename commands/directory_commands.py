"""Directory manipulation commands."""
import os
import shutil
from utils import Validator

_VALIDATOR = Validator()


class DirectoryCommands:
    """Handles directory-related dev_shell commands."""

    @staticmethod
    def pwd(args):
        """Print the current working directory.
        
        Usage: pwd
        """
        print(os.getcwd())

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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
                    entries = [entry for entry in entries if os.path.isdir(os.path.join(base, entry))]
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
