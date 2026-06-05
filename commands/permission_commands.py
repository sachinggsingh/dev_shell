"""Permissions-Commands."""
import os
class Permissions:
    """Handles the permissions related to files."""

    @staticmethod
    def execute(args):
        if not args:
            print("Usage: perm <path>")
            return
        path = args[0]

        if not os.path.exists(path):
            print("Path does not exist")
            return
        print(f"\nPath: {path}\n")

        print(
            f"Readable  :   "
            f"{'Yes' if os.access(path, os.R_OK)else 'No'}"
        )
        print(
            f"Writable   : "
            f"{'Yes' if os.access(path, os.W_OK) else 'No'}"
        )

        print(
            f"Executable : "
            f"{'Yes' if os.access(path, os.X_OK) else 'No'}"
        )