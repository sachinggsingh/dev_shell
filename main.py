"""Entry point for the dev_shell application."""
from commands.network_commands import NetWorkcommands
from shell import Shell


if __name__ == "__main__":
    shell = Shell(NetWorkcommands())
    shell.run()