"""Help command."""


class HelpCommand:
    """Handles the help command."""

    HELP_TEXT = {
        "pwd": "Show current directory",
        "ls": "List files/folders [path] [-a] [-l] [-h] [-d]",
        "mkdir": "Create folder       <name> [-p]",
        "rmdir": "Remove folder       <name> [-r]",
        "find": "Find files or directories <name> [-f] [-d] [-l]",
        "touch": "Create/update file  <name>",
        "cd": "Change directory    <path>",
        "cat": "Show the file content <name>",
        "size": "Show file size <path>",
        "rm": "Remove file <name> [-f]",
        "perm": "Show file permissions for a path",
        "tree": "Show directory tree [path]",
        "clear": "Clear screen",
        "watch": "Watch a registered server: watch <server-name> [-i seconds] [-m cpu,memory] [-n count]",
        "watch-server": "Watch a registered server: watch-server <server-name> [-i seconds] [-m cpu,memory] [-n count]",
        "add-server": "Register a server: add-server <name> <ip> <port>",
        "remove-server": "Remove a server: remove-server <name>",
        "servers": "List all registered servers",
        "logs": "Watch the logs of a file <name>",
        "help": "Show this help",
        "exit": "Exit shell",
        "q": "Exit shell (alias)",
    }

    @staticmethod
    def help(args):
        """Display help information for available commands.
        
        Usage: help
        """
        print("\nAvailable Commands:")
        for cmd, desc in HelpCommand.HELP_TEXT.items():
            print(f"  {cmd:<8}  {desc}")
        print()
