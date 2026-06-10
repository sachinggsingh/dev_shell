"""Server registry management commands."""


class ServerCommands:
    """Commands to add, remove, and list servers in the registry."""

    def __init__(self, registry):
        self.registry = registry

    @staticmethod
    def _print_add_usage():
        print("Usage: add-server <name> <job>")
        print("  Registers a new server for monitoring via Prometheus.")
        print("Example:")
        print("  add-server backend backend-api")

    @staticmethod
    def _print_remove_usage():
        print("Usage: remove-server <name>")
        print("  Removes a server from the registry.")
        print("Example:")
        print("  remove-server web1")

    def add_server(self, args):
        """Register a new server in the registry.

        Usage: add-server <name> <job>
        """
        if not args or "-h" in args or "--help" in args:
            self._print_add_usage()
            return

        if len(args) < 2:
            print("Error: Missing arguments.")
            self._print_add_usage()
            return

        name, job = args[0], args[1]

        if name in self.registry:
            print(f"Server '{name}' already exists. Remove it first or use a different name.")
            return

        self.registry[name] = {"job": job}
        print(f"Server '{name}' registered with job '{job}'")

    def remove_server(self, args):
        """Remove a server from the registry.

        Usage: remove-server <name>
        """
        if not args or "-h" in args or "--help" in args:
            self._print_remove_usage()
            return

        name = args[0]

        if name not in self.registry:
            print(f"Server '{name}' is not registered.")
            return

        del self.registry[name]
        print(f"Server '{name}' removed.")

    def list_servers(self, args):
        """List all registered servers.

        Usage: servers
        """
        if not self.registry:
            print("No servers registered.")
            return

        print(f"\n{'Name':<15} {'Job':<20}")
        print("-" * 36)
        for name, info in self.registry.items():
            print(f"{name:<15} {info.get('job', 'N/A'):<20}")
        print()
