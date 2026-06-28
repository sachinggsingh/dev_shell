"""CLI entry point for dev_shell."""

from dev_shell.commands.network import NetWorkcommands
from dev_shell.core.shell import Shell


def main() -> None:
    """Start the interactive dev_shell session."""
    shell = Shell(network_commands=NetWorkcommands())
    shell.run()


if __name__ == "__main__":
    main()
