import json
import time
import urllib.request
import os


class WatchServerCommand:

    def __init__(self, registry):
        self.registry = registry

    @staticmethod
    def _print_usage():
        print("Usage: watch-server <server-name> [-i seconds] [-m cpu,memory] [-n count]")
        print("Options:")
        print("  -i, --interval <seconds>   Refresh interval in seconds (default: 2)")
        print("  -m, --metrics <list>       Comma-separated metrics to show (cpu,memory)")
        print("  -n, --count <number>       Number of update cycles before exiting")
        print("  -h, --help                 Show this usage information")

    def execute(self, args):
        if not args or "-h" in args or "--help" in args:
            self._print_usage()
            return

        interval = 2.0
        count = None
        metrics = ["cpu", "memory"]
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
            elif arg in ("-m", "--metrics"):
                i += 1
                if i >= len(args):
                    print("Error: Missing value for metrics")
                    self._print_usage()
                    return
                metrics = [m.strip().lower() for m in args[i].split(",") if m.strip()]
            elif arg.startswith("-"):
                print(f"Unknown option: {arg}")
                self._print_usage()
                return
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
        url = f"http://{server['ip']}:{server['port']}/metrics"
        supported_metrics = {"cpu": "CPU", "memory": "Memory"}
        active_metrics = [m for m in metrics if m in supported_metrics]

        if not active_metrics:
            print("Error: No supported metrics selected. Use cpu,memory")
            return

        loop_count = 0
        error_msg = ""
        try:
            while count is None or loop_count < count:
                os.system("cls" if os.name == "nt" else "clear")

                try:
                    with urllib.request.urlopen(url, timeout=5) as response:
                        metrics_data = json.loads(response.read())
                    online = True
                except Exception as e:
                    metrics_data = {}
                    online = False
                    error_msg = str(e)

                print("=" * 40)
                print(f"Watching: {server_name}")
                print("=" * 40)

                for metric in active_metrics:
                    label = supported_metrics[metric]
                    value = metrics_data.get(metric)
                    if value is None:
                        print(f"{label}: unavailable")
                    else:
                        print(f"{label}: {value}%")

                status_text = "Online" if online else f"Offline ({error_msg})"
                print(f"Status: {status_text}")

                loop_count += 1
                if count is not None and loop_count >= count:
                    break
                time.sleep(interval)

        except KeyboardInterrupt:
            print("\nStopped monitoring")
