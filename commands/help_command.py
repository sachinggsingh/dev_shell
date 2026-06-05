"""Help command."""


class HelpCommand:
    """Handles the help command."""

    HELP_TEXT = {
        "pwd": "Show current directory",
        "ls": "List files/folders [path] [-a] [-l] [-d]",
        "mkdir": "Create folder       <name> [-p]",
        "rmdir": "Remove folder       <name> [-r]",
        "touch": "Create/update file  <name>",
        "cd": "Change directory    <path>",
        "cat": "Show the file content <name>",
        "size": "Show file size <path>",
        "rm": "Remove file <name> [-f]",
        "perm": "Show file permissions for a path",
        "tree": "Show directory tree [path]",
        "clear": "Clear screen",
        "watch": "Watch CPU usage for a server: watch <server-name> (local supported)",
        "logs": "watch the logs of the file     <name>",
        "size": "size of the file <name>",
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
