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
    def watch(args):
        """Watch CPU usage for a server.
        
        Usage: watch [server-name]
        """
        server = args[0] if args else "local"
        if server.lower() not in ("local", "localhost"):
            print(f"Remote watch for server '{server}' is not implemented yet.")
            print("Supported usage: watch [local|localhost]")
            return

        try:
            import psutil
        except ImportError:
            psutil = None

        try:
            while True:
                subprocess.run("cls" if os.name == "nt" else "clear")
                print(f"Watching CPU for: {server}\n")

                if psutil:
                    cpu = psutil.cpu_percent(interval=1)
                    per_cpu = psutil.cpu_percent(interval=None, percpu=True)
                    memory = psutil.virtual_memory()
                    print(f"Total CPU Usage: {cpu:.1f}%")
                    print("Per-CPU:")
                    print("  " + ", ".join(f"{value:.1f}%" for value in per_cpu))
                    print(f"Memory Usage: {memory.percent:.1f}% ({Formatter.format_file_size(memory.used)} / {Formatter.format_file_size(memory.total)})")
                else:
                    try:
                        load = os.getloadavg()[0]
                        print(f"Load average (1m): {load:.2f}")
                    except Exception:
                        print("Install 'psutil' for CPU percentage output: pip install psutil")
                    time.sleep(1)
                    continue

                print("\nPress Ctrl+C to stop.")
        except KeyboardInterrupt:
            print("\nWatch stopped.")

    @staticmethod
    def exit_shell(args):
        """Exit the shell.
        
        Usage: exit
        """
        return True
