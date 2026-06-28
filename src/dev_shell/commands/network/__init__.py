"""Network diagnostic commands."""

from . import dns, http, ip, nslookup, ping, traceroute


class NetWorkcommands:
    """Handles network-related shell commands."""

    ping = staticmethod(ping.ping)
    dns = staticmethod(dns.dns)
    ip = staticmethod(ip.ip)
    curl = staticmethod(http.curl)
    traceroute = staticmethod(traceroute.traceroute)
    nslookup = staticmethod(nslookup.nslookup)

    @staticmethod
    def _print_ip_usage():
        ip._print_ip_usage()
