"""IP address lookup command."""

import socket


def _print_ip_usage():
    print("Usage: ip [options] [hostname]")
    print("Options:")
    print("  -4, --ipv4        Show IPv4 address")
    print("  -6, --ipv6        Show IPv6 address")
    print("  -a, --all         Show all resolved addresses")
    print("  -h, --help        Show this help message")


def ip(args):
    if not args or args[0] in {"-h", "--help"}:
        _print_ip_usage()
        return

    ipv4 = False
    ipv6 = False
    show_all = False
    target = None
    i = 0

    while i < len(args):
        arg = args[i]
        if arg in {"-4", "--ipv4"}:
            ipv4 = True
        elif arg in {"-6", "--ipv6"}:
            ipv6 = True
        elif arg in {"-a", "--all"}:
            show_all = True
        elif arg in {"-h", "--help"}:
            _print_ip_usage()
            return
        elif arg.startswith("-"):
            print(f"Unknown option: {arg}")
            _print_ip_usage()
            return
        elif target is None:
            target = arg
        else:
            print("Error: only one hostname or address can be provided")
            _print_ip_usage()
            return
        i += 1

    if ipv4 and ipv6:
        print("Error: choose either IPv4 or IPv6")
        _print_ip_usage()
        return

    if target is None:
        target = socket.gethostname()

    try:
        addresses = []
        for family, _, _, _, sockaddr in socket.getaddrinfo(
            target, None, type=socket.SOCK_STREAM
        ):
            address = sockaddr[0]
            if family == socket.AF_INET and (not ipv6):
                addresses.append(address)
            elif family == socket.AF_INET6 and (ipv6 or not ipv4):
                addresses.append(address)

        if not addresses:
            print(f"No addresses found for '{target}'")
            return

        print("=" * 40)
        print("Network Information")
        print("=" * 40)
        print(f"Target: {target}")

        if show_all:
            print("Addresses:")
            for address in addresses:
                print(f"  - {address}")
        else:
            print(f"IP Address: {addresses[0]}")

    except socket.gaierror as exc:
        print(f"Unable to resolve '{target}': {exc}")
