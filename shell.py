"""Core shell implementation."""
import os
import shlex
from commands.file_commands import FileCommands
from commands.directory_commands import DirectoryCommands
from commands.system_commands import SystemCommands
from commands.log_commands import LogCommands
from commands.help_command import HelpCommand
from commands.permission_commands import Permissions
from commands.watch_command import WatchServerCommand
from commands.server_commands import ServerCommands
from utils import Formatter, Logger, Validator

try:
    import readline
except ImportError:
    readline = None


class Shell:
    """Main shell implementation with command dispatcher."""

    def __init__(self):
        """Initialize the shell with all available commands."""
        self.running = True
        self.logger = Logger(log_file=os.path.join(os.path.dirname(__file__), "shell.log"))
        self.validator = Validator()
        self.server_registry = {
            "local": {"ip": "127.0.0.1", "port": 8000}
        }
        self.server_watcher = WatchServerCommand(self.server_registry)
        self.server_cmds = ServerCommands(self.server_registry)

        self.commands = {
            "pwd": DirectoryCommands.pwd,
            "ls": FileCommands.ls,
            "mkdir": DirectoryCommands.mkdir,
            "rmdir": DirectoryCommands.rmdir,
            "find":FileCommands.find,
            "touch": FileCommands.touch,
            "rm": FileCommands.rm,
            "cd": DirectoryCommands.cd,
            "clear": SystemCommands.clear,
            "cat": FileCommands.cat,
            "tree": DirectoryCommands.tree,
            "logs": LogCommands.logs,
            "watch": self.server_watcher.execute,
            "watch-server": self.server_watcher.execute,
            "perm": Permissions.execute,
            "add-server": self.server_cmds.add_server,
            "remove-server": self.server_cmds.remove_server,
            "servers": self.server_cmds.list_servers,
            "size": FileCommands.file_size,
            "help": HelpCommand.help,
            "exit": self._handle_exit,
            "q": self._handle_exit,
        }
        self.history_file = os.path.expanduser("~/.dev_shell_history")
        self._configure_readline()
        self.logger.info("Shell initialized")

    def _configure_readline(self):
        """Configure readline for command history and tab completion."""
        if not readline:
            return

        readline.parse_and_bind("tab: complete")
        readline.set_completer(self._complete_command)
        try:
            if os.path.exists(self.history_file):
                readline.read_history_file(self.history_file)
        except Exception:
            pass

    def _complete_command(self, text, state):
        """Tab completion for available shell commands."""
        options = [cmd for cmd in self.commands if cmd.startswith(text)]
        if state < len(options):
            return options[state]
        return None

    def _save_history(self):
        """Save command history to the history file."""
        if not readline:
            return

        try:
            readline.write_history_file(self.history_file)
        except Exception:
            pass

    def _handle_exit(self, args):
        """Handle exit command by setting running flag."""
        self.running = False

    def cleanup(self):
        """Perform cleanup operations before exiting."""
        self._save_history()
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
        print("dev_shell Started")
        print("Type 'help' to see available commands.\n")
        self.logger.info("dev_shell started")

        try:
            while self.running:
                command = input("dev_shell> ").strip()

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
            self.logger.info("dev_shell stopped")
