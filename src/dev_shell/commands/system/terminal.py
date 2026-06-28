"""Terminal control commands."""

import os
import subprocess


def clear(args):
    """Clear the terminal screen."""
    subprocess.run("cls" if os.name == "nt" else "clear", check=True)
