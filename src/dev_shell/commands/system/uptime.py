"""System uptime commands."""

import time
from datetime import datetime, timedelta

import psutil

from ._helpers import row, section


def uptime(args):
    """Display system uptime information.

    Usage: uptime
    """
    try:
        boot_ts = psutil.boot_time()
        boot_dt = datetime.fromtimestamp(boot_ts)
        uptime_secs = int(time.time() - boot_ts)
        delta = timedelta(seconds=uptime_secs)

        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        human = []
        if days:
            human.append(f"{days} day{'s' if days != 1 else ''}")
        if hours:
            human.append(f"{hours} hour{'s' if hours != 1 else ''}")
        if minutes:
            human.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
        if seconds or not human:
            human.append(f"{seconds} second{'s' if seconds != 1 else ''}")

        section("System Uptime")
        row("Boot Time:", boot_dt.strftime("%Y-%m-%d %H:%M:%S"))
        row("Total Uptime:", str(delta))
        row("Human Readable:", ", ".join(human))

    except Exception as exc:
        print(f"[uptime] Error: {exc}")
