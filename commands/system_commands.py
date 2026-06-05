"""System-level commands."""
import os
import subprocess
import time
from utils import Formatter


class SystemCommands:
    """Handles system-related shell commands."""

    @staticmethod
    def clear(args):
        """Clear the screen.
        
        Usage: clear
        """
        subprocess.run("cls" if os.name == "nt" else "clear", check=True)
    @staticmethod
    def exit_shell(args):
        """Exit the shell.
        
        Usage: exit
        """
        return True
