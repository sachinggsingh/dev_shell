"""Grafana monitoring commands."""

from dev_shell.monitoring.grafana_client import GrafanaClient, _default_config_path
from dev_shell.monitoring.provider.grafana import GrafanaProvider


class GrafanaCommands:
    """Shell commands for Grafana connectivity checks."""

    def __init__(self, provider=None):
        self.provider = provider or GrafanaProvider()

    @staticmethod
    def _print_usage():
        print("Usage: grafana <subcommand>")
        print("Subcommands:")
        print("  ping     Check Grafana health endpoint")
        print("  config   Show active Grafana configuration")

    def execute(self, args):
        if not args or args[0] in ("-h", "--help"):
            self._print_usage()
            return

        subcommand = args[0]
        sub_args = args[1:]

        if subcommand == "ping":
            self.ping(sub_args)
        elif subcommand == "config":
            self.config(sub_args)
        else:
            print(f"Unknown grafana subcommand: {subcommand}")
            self._print_usage()

    def ping(self, args):
        """Check whether Grafana is reachable."""
        if self.provider.ping():
            print("Grafana: reachable")
        else:
            print("Grafana: unreachable")

    def config(self, args):
        """Show the bundled Grafana config path and loaded settings."""
        client = self.provider.client
        config_path = _default_config_path()

        print(f"Config file: {config_path}")
        print(f"Host:        {client.host}")
        print(f"Port:        {client.port}")
        print(f"Datasource:  {client.datasource_uid or '(not set)'}")
        print(f"API key:     {'set' if client.api_key else 'not set'}")
