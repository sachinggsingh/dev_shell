"""ICMP ping command."""

import subprocess


def ping(args):
    if not args:
        print("Usage: ping <host>")
        return

    host = args[0]
    try:
        subprocess.run(["ping", "-c", "4", host], check=False)  # noqa: S603 S607
    except OSError as e:
        print(f"Error: {e}")
