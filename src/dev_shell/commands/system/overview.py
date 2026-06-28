"""System overview commands."""

import os
import platform
import socket
import sys
import time
from datetime import timedelta

import getpass
import psutil

from ._helpers import bytes_to_human, row, section


def system(args):
    """Display a comprehensive system overview.

    Usage: system
    """
    try:
        section("System Information")

        row("Hostname:", socket.gethostname())
        row("Username:", getpass.getuser())
        row("Operating System:", platform.system())
        row("OS Version:", platform.version())
        row("Kernel Version:", platform.release())
        row("Architecture:", " / ".join(platform.architecture()))
        row("Processor:", platform.processor() or "N/A")
        row("Python Version:", sys.version.split()[0])
        row("Shell:", os.environ.get("SHELL", os.environ.get("COMSPEC", "N/A")))
        row("Working Directory:", os.getcwd())

        print()
        section("Resource Usage")

        cpu_pct = psutil.cpu_percent(interval=0.5)
        row("CPU Usage:", f"{cpu_pct:.1f}%")

        mem = psutil.virtual_memory()
        row(
            "Memory Usage:",
            f"{bytes_to_human(mem.used)} / {bytes_to_human(mem.total)}"
            f"  ({mem.percent:.1f}%)",
        )

        disk = psutil.disk_usage("/")
        row(
            "Disk Usage:",
            f"{bytes_to_human(disk.used)} / {bytes_to_human(disk.total)}"
            f"  ({disk.percent:.1f}%)",
        )

        boot_ts = psutil.boot_time()
        uptime_secs = time.time() - boot_ts
        row("Uptime:", str(timedelta(seconds=int(uptime_secs))))

    except Exception as exc:
        print(f"[system] Error: {exc}")


def hardware(args):
    """Display hardware information.

    Usage: hardware
    """
    try:
        section("Hardware Information")

        freq = psutil.cpu_freq()
        freq_str = f"{freq.current:.0f} MHz" if freq else "N/A"
        row("CPU Model:", platform.processor() or "N/A")
        row("Physical Cores:", str(psutil.cpu_count(logical=False) or "N/A"))
        row("Logical Cores:", str(psutil.cpu_count(logical=True) or "N/A"))
        row("CPU Frequency:", freq_str)

        print()

        mem = psutil.virtual_memory()
        row("Total RAM:", bytes_to_human(mem.total))
        row("Available RAM:", bytes_to_human(mem.available))

        print()

        disk = psutil.disk_usage("/")
        row("Total Disk:", bytes_to_human(disk.total))
        row("Free Disk:", bytes_to_human(disk.free))

        print()

        battery = psutil.sensors_battery()
        if battery is not None:
            section("Battery")
            row("Battery:", f"{battery.percent:.1f}%")
            row("Charging:", "Yes" if battery.power_plugged else "No")
        else:
            print("  Battery: Not available on this system.")

    except Exception as exc:
        print(f"[hardware] Error: {exc}")
