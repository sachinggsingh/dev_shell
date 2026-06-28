"""ICMP ping command."""

import subprocess


def ping(args):
    if not args:
        print("Usage: ping <host>")
        return

    host = args[0]
    try:
        subprocess.run(["ping", "-c", "4", host], check=False)
    except Exception as e:
        print(f"Error: {e}")
