"""Core shell implementation."""
import os
import shlex
from commands.file_commands import FileCommands
from commands.directory_commands import DirectoryCommands
from commands.system_commands import SystemCommands
from commands.log_commands import LogCommands
from commands.help_command import HelpCommand
from commands.permission_commands import Permissions
from utils import Formatter, Logger, Validator


class Shell:
    """Main shell implementation with command dispatcher."""

    def __init__(self):
        """Initialize the shell with all available commands."""
        self.running = True
        self.logger = Logger(log_file=os.path.join(os.path.dirname(__file__), "shell.log"))
        self.validator = Validator()
        self.commands = {
            "pwd": DirectoryCommands.pwd,
            "ls": FileCommands.ls,
            "mkdir": DirectoryCommands.mkdir,
            "rmdir": DirectoryCommands.rmdir,
            "touch": FileCommands.touch,
            "rm": FileCommands.rm,
            "cd": DirectoryCommands.cd,
            "clear": SystemCommands.clear,
            "cat": FileCommands.cat,
            "tree": DirectoryCommands.tree,
            "logs": LogCommands.logs,
            "watch": SystemCommands.watch,
            "perm": Permissions.execute,
            "size": FileCommands.file_size,
            "help": HelpCommand.help,
            "exit": self._handle_exit,
            "q": self._handle_exit,
        }
        self.logger.info("Shell initialized")

    def _handle_exit(self, args):
        """Handle exit command by setting running flag."""
        self.running = False

    def cleanup(self):
        """Perform cleanup operations before exiting."""
        print("\nCleaning up resources...")
        print("Goodbye!")

    def execute(self, command_line):
        """Parse and execute a command.
        
        Args:
            command_line: Raw command string from user input
        """
        parts = shlex.split(command_line)

        if not parts:
            return

        command = parts[0]
        args = parts[1:]

        handler = self.commands.get(command)

        if handler:
            handler(args)
        else:
            print(f"Unknown command: '{command}'. Type 'help' for available commands.")

    def run(self):
        """Main shell loop."""
        print("Mini Shell Started")
        print("Type 'help' to see available commands.\n")
        self.logger.info("Shell started")

        try:
            while self.running:
                command = input("shell> ").strip()

                if not command:
                    continue

                try:
                    self.logger.info(f"Running command: {command}")
                    self.execute(command)

                except FileNotFoundError:
                    message = "File or directory not found."
                    print(Formatter.highlight_error(message))
                    self.logger.error(message)

                except PermissionError:
                    message = "Permission denied."
                    print(Formatter.highlight_error(message))
                    self.logger.error(message)

                except OSError as e:
                    message = f"OS Error: {e}"
                    print(Formatter.highlight_error(message))
                    self.logger.error(message)

                except Exception as e:
                    message = f"Unexpected error: {e}"
                    print(Formatter.highlight_error(message))
                    self.logger.error(message)

        except KeyboardInterrupt:
            message = "Ctrl+C — shutting down gracefully..."
            print(f"\n{message}")
            self.logger.info(message)

        finally:
            self.cleanup()
            self.logger.info("Shell stopped")
