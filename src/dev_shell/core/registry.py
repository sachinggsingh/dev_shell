"""Central command registry for the dev_shell dispatcher."""

from dev_shell.commands.directory import DirectoryCommands
from dev_shell.commands.file import FileCommands
from dev_shell.commands.logs import LogCommands
from dev_shell.commands.meta import HelpCommand
from dev_shell.commands.network import NetWorkcommands
from dev_shell.commands.permissions import Permissions
from dev_shell.commands.server import ServerCommands, WatchServerCommand
from dev_shell.commands.system import SystemCommands
from dev_shell.integration.git_commands import GitCommands


def build_command_registry(shell) -> dict:
    """Return the mapping of command names to handler callables."""
    server_watcher = WatchServerCommand(shell.server_registry)
    server_cmds = ServerCommands(shell.server_registry)
    network = shell.network_commands or NetWorkcommands()
    git = GitCommands()

    return {
        # File & directory
        "pwd": DirectoryCommands.pwd,
        "ls": FileCommands.ls,
        "mkdir": DirectoryCommands.mkdir,
        "rmdir": DirectoryCommands.rmdir,
        "find": FileCommands.find,
        "touch": FileCommands.touch,
        "rm": FileCommands.rm,
        "cd": DirectoryCommands.cd,
        "rename": FileCommands.rename,
        "cat": FileCommands.cat,
        "copy": FileCommands.cp,
        "move": FileCommands.move,
        "head": FileCommands.head,
        "tail": FileCommands.tail,
        "grep": FileCommands.grep,
        "stat": FileCommands.stat,
        "edit": FileCommands.edit,
        "checksum": FileCommands.checksum,
        "diff": FileCommands.diff,
        "tree": DirectoryCommands.tree,
        "size": FileCommands.file_size,
        "perm": Permissions.execute,
        "logs": LogCommands.logs,
        # Server monitoring
        "watch": server_watcher.execute,
        "watch-server": server_watcher.execute,
        "add-server": server_cmds.add_server,
        "remove-server": server_cmds.remove_server,
        "servers": server_cmds.list_servers,
        # Network
        "ping": network.ping,
        "dns": network.dns,
        "ip": network.ip,
        "curl": network.curl,
        "traceroute": network.traceroute,
        "nslookup": network.nslookup,
        # System
        "clear": SystemCommands.clear,
        "system": SystemCommands.system,
        "hardware": SystemCommands.hardware,
        "cpu": SystemCommands.cpu,
        "memory": SystemCommands.memory,
        "disk": SystemCommands.disk,
        "network": SystemCommands.network,
        "processes": SystemCommands.processes,
        "env": SystemCommands.env,
        "uptime": SystemCommands.uptime,
        "gpu": SystemCommands.gpu,
        "services": SystemCommands.services,
        "packages": SystemCommands.packages,
        # Integration
        "git": git.execute,
        # Meta
        "help": HelpCommand.help,
        "exit": shell._handle_exit,
        "q": shell._handle_exit,
    }
