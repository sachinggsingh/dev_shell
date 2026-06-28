"""Find and search files."""

import os

from dev_shell.utils import Formatter


IGNORE_DIRS = {
    ".venv",
    "venv",
    "__pycache__",
    ".git",
    "node_modules",
    ".idea",
    ".vscode",
}


def find(args):
    """Search for files and directories recursively.

    Usage: find <name> [-f] [-d] [-l]
    """
    if not args:
        print("Usage: find <name> [-f] [-d] [-l]")
        return

    files_only = "-f" in args
    dirs_only = "-d" in args
    long_format = "-l" in args

    search_term = next((arg for arg in args if not arg.startswith("-")), None)
    if not search_term:
        print("Search term required.")
        return

    search_term = search_term.lower()
    matches = []

    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        if not files_only:
            for directory in dirs:
                if search_term in directory.lower():
                    matches.append(("DIR", os.path.join(root, directory)))

        if not dirs_only:
            for file in files:
                if search_term in file.lower():
                    matches.append(("FILE", os.path.join(root, file)))

    if not matches:
        print(f"No matches found for '{search_term}'")
        return

    print(f"\nFound {len(matches)} match(es):\n")

    for item_type, path in matches:
        if long_format:
            print(Formatter.format_item_details(item_type, path))
        else:
            print(f"[{item_type}] {path}")


def grep(args):
    """Search text inside files.

    Usage: grep <pattern> <file> [-i] [-n] [-c] [-v] [-r]
    """
    if len(args) < 2:
        print("Usage: grep <pattern> <file> [-i] [-n] [-c] [-v] [-r]")
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
            with open(filename, "r", encoding="utf-8", errors="ignore") as file:
                for line_number, line in enumerate(file, start=1):
                    content = line.rstrip()

                    if ignore_case:
                        found = pattern.lower() in content.lower()
                    else:
                        found = pattern in content

                    if invert_match:
                        found = not found

                    if found:
                        matches += 1

                        if count_only:
                            continue

                        if show_line_numbers:
                            print(f"{line_number}: {content}")
                        else:
                            print(content)
        except Exception as e:
            print(f"Error reading {filename}: {e}")

    if recursive:
        if not os.path.isdir(target):
            print(f"Directory not found: {target}")
            return

        for root, _, files in os.walk(target):
            for file in files:
                process_file(os.path.join(root, file))
    else:
        if not os.path.exists(target):
            print(f"File not found: {target}")
            return

        process_file(target)

    if count_only:
        print(f"Total matches: {matches}")
