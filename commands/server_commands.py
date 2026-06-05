"""Server registry management commands."""


class ServerCommands:
    """Commands to add, remove, and list servers in the registry."""

    def __init__(self, registry):
        self.registry = registry

    @staticmethod
    def _print_add_usage():
        print("Usage: add-server <name> <ip> <port>")
        print("  Registers a new server for monitoring.")
        print("Example:")
        print("  add-server web1 192.168.1.20 9000")

    @staticmethod
    def _print_remove_usage():
        print("Usage: remove-server <name>")
        print("  Removes a server from the registry.")
        print("Example:")
        print("  remove-server web1")

    def add_server(self, args):
        """Register a new server in the registry.

        Usage: add-server <name> <ip> <port>
        """
        if not args or "-h" in args or "--help" in args:
            self._print_add_usage()
            return

        if len(args) < 3:
            print("Error: Missing arguments.")
            self._print_add_usage()
            return

        name, ip, port_str = args[0], args[1], args[2]

        try:
            port = int(port_str)
            if port < 1 or port > 65535:
                raise ValueError
        except ValueError:
            print("Error: Port must be an integer between 1 and 65535.")
            return

        if name in self.registry:
            print(f"Server '{name}' already exists. Remove it first or use a different name.")
            return

        self.registry[name] = {"ip": ip, "port": port}
        print(f"Server '{name}' registered at {ip}:{port}")

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

        print(f"\n{'Name':<15} {'IP':<20} {'Port':<8}")
        print("-" * 43)
        for name, info in self.registry.items():
            print(f"{name:<15} {info['ip']:<20} {info['port']:<8}")
        print()
