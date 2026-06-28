"""Local network interface information."""

import socket

import psutil

from ._helpers import bytes_to_human, row, section


def network(args):
    """Display network information.

    Usage: network
    """
    try:
        section("Network Information")

        hostname = socket.gethostname()
        try:
            ip_address = socket.gethostbyname(hostname)
        except socket.gaierror:
            ip_address = "N/A"

        row("Hostname:", hostname)
        row("IP Address:", ip_address)

        io = psutil.net_io_counters()
        row("Bytes Sent:", bytes_to_human(io.bytes_sent))
        row("Bytes Received:", bytes_to_human(io.bytes_recv))

        print()
        section("Network Interfaces")
        addrs = psutil.net_if_addrs()
        for iface, addr_list in addrs.items():
            print(f"  [{iface}]")
            for addr in addr_list:
                family_name = str(addr.family).replace("AddressFamily.", "")
                if addr.address:
                    print(f"    {family_name:<12} {addr.address}")
                if addr.netmask:
                    print(f"    {'Netmask':<12} {addr.netmask}")

    except Exception as exc:
        print(f"[network] Error: {exc}")
