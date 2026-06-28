"""Real-time server monitoring command."""

import os
import time

from dev_shell.monitoring.prometheus_client import PrometheusClient
from dev_shell.monitoring.queries import Queries


class WatchServerCommand:
    """Stream Prometheus metrics for a registered server."""

    def __init__(self, registry):
        self.registry = registry
        self.prom_client = PrometheusClient()

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
                    if interval <= 0:
                        raise ValueError
                except ValueError:
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
                    if count < 1:
                        raise ValueError
                except ValueError:
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
            print(f"Error: Server '{server_name}' has no job configured for Prometheus")
            return

        queries = Queries.get_queries(job_name)
        loop_count = 0
        error_msg = ""

        try:
            while count is None or loop_count < count:
                os.system("cls" if os.name == "nt" else "clear")

                metrics_data = {}
                online = True
                try:
                    metrics_data["cpu"] = self.prom_client.query(queries["cpu"])
                    metrics_data["memory"] = self.prom_client.query(queries["memory"])
                    metrics_data["requests_per_sec"] = self.prom_client.query(
                        queries["requests_per_sec"]
                    )
                    metrics_data["error_rate"] = self.prom_client.query(
                        queries["error_rate"]
                    )
                    metrics_data["latency_p95"] = self.prom_client.query(
                        queries["latency_p95"]
                    )
                except Exception as e:
                    online = False
                    error_msg = str(e)

                print("=" * 40)
                print(f"Watching: {server_name}")
                print("=" * 40)
                print()

                if metrics_data.get("cpu") is not None:
                    cpu_val = float(metrics_data["cpu"]) * 100
                    print(f"CPU: {cpu_val:.2f}%")
                else:
                    print("CPU: unavailable")

                print()

                if metrics_data.get("memory") is not None:
                    mem_val = float(metrics_data["memory"]) / (1024 * 1024)
                    print(f"Memory: {mem_val:.2f} MB")
                else:
                    print("Memory: unavailable")

                print()

                if metrics_data.get("requests_per_sec") is not None:
                    req_val = float(metrics_data["requests_per_sec"])
                    print(f"Requests/sec: {req_val:.2f}")
                else:
                    print("Requests/sec: unavailable")

                print()

                if metrics_data.get("error_rate") is not None:
                    err_val = float(metrics_data["error_rate"]) * 100
                    print(f"Error Rate: {err_val:.2f}%")
                else:
                    print("Error Rate: unavailable")

                print()

                if (
                    metrics_data.get("latency_p95") is not None
                    and str(metrics_data["latency_p95"]).lower() != "nan"
                ):
                    lat_val = float(metrics_data["latency_p95"]) * 1000
                    print(f"Latency P95: {lat_val:.2f}ms")
                else:
                    print("Latency P95: unavailable")

                print()
                status_text = "Healthy" if online else f"Offline ({error_msg})"
                print(f"Status: {status_text}")
                print()
                print("=" * 40)

                loop_count += 1
                if count is not None and loop_count >= count:
                    break
                time.sleep(interval)

        except KeyboardInterrupt:
            print("\nStopped monitoring")
