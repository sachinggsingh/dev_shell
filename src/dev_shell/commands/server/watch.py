"""Real-time server monitoring command."""

import time

from dev_shell.monitoring.provider.grafana import GrafanaProvider
from dev_shell.render.metrics_panel import render_metrics_panel


class WatchServerCommand:
    """Stream Grafana-backed metrics for a registered server."""

    def __init__(self, registry, provider=None):
        self.registry = registry
        self.provider = provider or GrafanaProvider()

    @staticmethod
    def _print_usage():
        print("Usage: watch-server <server-name> [-i seconds] [-n count]")
        print("Options:")
        print("  -i, --interval <seconds>   Refresh interval in seconds (default: 2)")
        print("  -n, --count <number>       Number of update cycles before exiting")
        print("  -h, --help                 Show this usage information")

    def execute(self, args):
        if not args or "-h" in args or "--help" in args:
            self._print_usage()
            return

        interval = 2.0
        count = None
        positional_args = []
        i = 0

        while i < len(args):
            arg = args[i]
            if arg in ("-i", "--interval"):
                i += 1
                if i >= len(args):
                    print("Error: Missing value for interval")
                    self._print_usage()
                    return
                try:
                    interval = float(args[i])
                except ValueError:
                    pass
                else:
                    if interval <= 0:
                        interval = -1  # trigger error below
                if interval <= 0:
                    print("Error: Interval must be a positive number")
                    return
            elif arg in ("-n", "--count"):
                i += 1
                if i >= len(args):
                    print("Error: Missing value for count")
                    self._print_usage()
                    return
                try:
                    count = int(args[i])
                except ValueError:
                    pass
                else:
                    if count < 1:
                        count = 0  # trigger error below
                if count is not None and count < 1:
                    print("Error: Count must be a positive integer")
                    return
            elif arg.startswith("-") and arg not in ("-m", "--metrics"):
                print(f"Unknown option: {arg}")
                self._print_usage()
                return
            elif arg in ("-m", "--metrics"):
                i += 1
            else:
                positional_args.append(arg)
            i += 1

        if not positional_args:
            self._print_usage()
            return

        server_name = positional_args[0]

        if server_name not in self.registry:
            print(f"Server '{server_name}' is not registered")
            return

        server = self.registry[server_name]
        job_name = server.get("job")
        if not job_name:
            print(f"Error: Server '{server_name}' has no job configured for Grafana")
            return

        if not self.provider.ping():
            print(
                "Error: Grafana is unreachable. "
                "Check src/dev_shell/config/grafana.json "
                "(host, port, api_key, datasource_uid)."
            )
            return

        loop_count = 0
        error_msg = ""

        try:
            while count is None or loop_count < count:
                summary = {}
                online = True

                try:
                    summary = self.provider.get_summary(job_name)
                except OSError as e:
                    online = False
                    error_msg = str(e)

                render_metrics_panel(
                    summary,
                    source_name="grafana",
                    target=f"{server_name} ({job_name})",
                )

                status_text = "Healthy" if online else f"Offline ({error_msg})"
                print(f"\n  Status: {status_text}")

                loop_count += 1
                if count is not None and loop_count >= count:
                    break
                time.sleep(interval)

        except KeyboardInterrupt:
            print("\nStopped monitoring")
