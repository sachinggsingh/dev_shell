"""Help command."""


class HelpCommand:
    """Handles the help command."""

    HELP_TEXT = {
        "File & Directory Commands": {
            "pwd": "Show current directory",
            "ls": "List files/folders [path] [-a] [-l] [-h] [-d]",
            "mkdir": "Create folder       <name> [-p]",
            "rmdir": "Remove folder       <name> [-r]",
            "find": "Find files or directories <name> [-f] [-d] [-l]",
            "touch": "Create/update file  <name>",
            "cd": "Change directory    <path>",
            "cat": "Show the file content <name>",
            "copy": "Copy files/directories <source> <destination>",
            "rename": "Rename file <old_file> <new_file>",
            "move": "Move/Rename files <source> <destination>",
            "stat": "Show detailed file metadata <path>",
            "grep": "Search text inside files <pattern> <file>  [-i] [-n] [-c] [-v] [-r]",
            "checksum": "Generate checksum of a file <file>",
            "diff": "Compare two files <file1> <file2>",
            "head": "Show first N lines <file> [-n lines]",
            "tail": "Show last N lines <file> [-n lines]",
            "edit": "Edit the file content <name>",
            "size": "Show file size <path>",
            "rm": "Remove file <name> [-f]",
            "perm": "Show file permissions for a path",
            "tree": "Show directory tree [path]",
            "logs": "Watch the logs of a file <name>",
        },
        "Network Commands": {
            "ping": "Send ICMP echo requests: ping <host>",
            "dns": "Resolve a hostname to an IP address: dns <hostname>",
            "ip": "Show IP information: ip [options] [hostname]",
            "curl": "Makes a web request: curl <url> [-X <method>] [-H <header>] [-d <data>]",
            # "netstat": "Show network connections: netstat [-t] [-u] [-a] [-p]",
            "traceroute": "Show the route to a host: traceroute <hostname> [-d]",
            "nslookup": "Resolve a hostname to an IP address: nslookup <hostname>",
        },
        "Server Monitoring Commands": {
            "watch": "Watch a registered server: watch <server-name> [-i seconds] [-m cpu,memory] [-n count]",
            "watch-server": "Watch a registered server: watch-server <server-name> [-i seconds] [-m cpu,memory] [-n count]",
            "add-server": "Register a server: add-server <name> <ip> <port>",
            "remove-server": "Remove a server: remove-server <name>",
            "servers": "List all registered servers",
        },
        "System Commands": {
            "clear": "Clear screen",
            "help": "Show this help",
            "exit": "Exit shell",
            "q": "Exit shell (alias)",
        }
    }

    @staticmethod
    def help(args):
        """Display help information for available commands.
        
        Usage: help
        """
        print("\nAvailable Commands:")
        for category, commands in HelpCommand.HELP_TEXT.items():
            print(f"\n[{category}]")
            for cmd, desc in commands.items():
                print(f"  {cmd:<14}  {desc}")
        print()
