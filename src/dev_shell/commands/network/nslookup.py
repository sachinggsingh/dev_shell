"""NS lookup command."""

import socket


def nslookup(args):
    if not args:
        print("Usage: nslookup <hostname>")
        return

    hostname = args[0]
    try:
        if hostname.replace(".", "").isdigit():
            name = socket.gethostbyaddr(hostname)[0]
            print("=" * 40)
            print(f"Name: {name}")
            print(f"Address: {hostname}")
            print("=" * 40)
        else:
            ip_address = socket.gethostbyname(hostname)
            print("=" * 40)

            try:
                print(f"DNS Server: {socket.gethostbyname(socket.gethostname())}")
            except socket.gaierror:
                pass
            print(f"Name: {hostname}")
            print(f"Address: {ip_address}")
            print("=" * 40)
    except socket.gaierror:
        print(f"Unable to resolve '{hostname}'")
    except Exception as e:
        print(f"Error: {e}")
