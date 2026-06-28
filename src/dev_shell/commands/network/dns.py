"""DNS resolution command."""

import socket


def dns(args):
    if not args:
        print("Usage: dns <hostname>")
        return

    hostname = args[0]
    try:
        ip_address = socket.gethostbyname(hostname)
        print("=" * 40)
        print(f"Hostname: {hostname}")
        print(f"IP Address: {ip_address}")
        print("=" * 40)
    except socket.gaierror:
        print(f"Unable to resolve '{hostname}'")
