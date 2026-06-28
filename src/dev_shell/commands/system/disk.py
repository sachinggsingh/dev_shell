"""Disk usage commands."""

import psutil

from ._helpers import bytes_to_human, section


def disk(args):
    """Display disk usage for mounted partitions.

    Usage:
      disk          Show main partitions
      disk -a       Show all partitions (including virtual/loop)
    """
    try:
        show_all = "-a" in args
        partitions = psutil.disk_partitions(all=show_all)

        section("Disk Usage")
        header = (
            f"  {'Device':<20} {'FS':<10} {'Total':>10} {'Used':>10} "
            f"{'Free':>10} {'Use%':>6}"
        )
        print(header)
        print("  " + "-" * (len(header) - 2))

        for part in partitions:
            try:
                usage = psutil.disk_usage(part.mountpoint)
            except PermissionError:
                continue
            print(
                f"  {part.device:<20} {part.fstype:<10}"
                f" {bytes_to_human(usage.total):>10}"
                f" {bytes_to_human(usage.used):>10}"
                f" {bytes_to_human(usage.free):>10}"
                f" {usage.percent:>5.1f}%"
            )

    except Exception as exc:
        print(f"[disk] Error: {exc}")
