"""Network commands."""
import socket
import subprocess
import socket
import requests
import psutil
import platform

#  need improvement
#  netstat. (remaining)
#  port-scan. (Nmap command flags required are )
class NetWorkcommands:
    """Handles network-related shell commands."""

    @staticmethod
    def _print_ip_usage():
        print("Usage: ip [options] [hostname]")
        print("Options:")
        print("  -4, --ipv4        Show IPv4 address")
        print("  -6, --ipv6        Show IPv6 address")
        print("  -a, --all         Show all resolved addresses")
        print("  -h, --help        Show this help message")

    def ping(self, args):
        if not args:
            print("Usage: ping <host>")
            return

        host = args[0]
        try:
            subprocess.run(["ping", "-c", "4", host], check=False)
        except Exception as e:
            print(f"Error: {e}")

    def dns(self, args):
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
    
    def ip(self, args):
        if not args or args[0] in {"-h", "--help"}:
            self._print_ip_usage()
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
                self._print_ip_usage()
                return
            elif arg.startswith("-"):
                print(f"Unknown option: {arg}")
                self._print_ip_usage()
                return
            elif target is None:
                target = arg
            else:
                print("Error: only one hostname or address can be provided")
                self._print_ip_usage()
                return
            i += 1

        if ipv4 and ipv6:
            print("Error: choose either IPv4 or IPv6")
            self._print_ip_usage()
            return

        if target is None:
            target = socket.gethostname()

        try:
            addresses = []
            for family, _, _, _, sockaddr in socket.getaddrinfo(target, None, type=socket.SOCK_STREAM):
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
    


    def _print_usage(self):
        print("""
    curl usage:
      curl <url>                                   # GET request (default)
      curl -X POST <url>                           # POST request
      curl -H "Content-Type: application/json" <url>
    """)

    def curl(self, args):
        if not args or "-h" in args or "--help" in args: 
            self._print_usage() 
            return 
            
        method = "GET"
        headers = {} 
        data = None 
        url = None
        
        i = 0
        while i < len(args):
            arg = args[i] 
            if arg in ("-X", "--request"): 
                i += 1 
                if i >= len(args): 
                    print("Error: Missing HTTP method") 
                    return 
                method = args[i].upper() 
            elif arg in ("-H", "--header"): 
                i += 1
                if i >= len(args): 
                    print("Error: Missing header value") 
                    return
                 
                header = args[i] 
                if ":" not in header: 
                    print("Error: Header must be in format 'Key: Value'") 
                    return 
                key, value = header.split(":", 1) 
                headers[key.strip()] = value.strip() 
            elif arg in ("-d", "--data"): 
                i += 1 
                if i >= len(args): 
                    print("Error: Missing data value") 
                    return 
                data = args[i] 
            elif not arg.startswith("-"):
                # If it's not an option, assume it's the url
                url = arg
            else: 
                print(f"Unknown option: {arg}") 
                self._print_usage() 
                return 
            i += 1 
            
        if not url:
            print("Error: Missing URL")
            self._print_usage()
            return
            
        try: 
            response = requests.request(method=method, url=url, headers=headers, data=data, timeout=10) 
            print("=" * 50) 
            print(f"URL: {url}") 
            print(f"Method: {method}") 
            print(f"Status Code: {response.status_code}") 
            print("=" * 50) 
            print(response.text) 
        except requests.exceptions.Timeout: 
            print("Error: Request timed out") 
        except requests.exceptions.ConnectionError: 
            print("Error: Unable to connect to server") 
        except requests.exceptions.RequestException as e: 
            print(f"Error: {e}")

    # def _print_usage(self):
    #     print("""
    #         netstat usage:
    #         netstat                            # Show all connections
    #         netstat -t                         # Show TCP connections
    #         netstat -u                         # Show UDP connections
    #         netstat -a                         # Show all connections
    #         netstat -p                         # Show process names
    #     """)

    # def netstat(self,args):
        # show_tcp = False
        # show_udp = False
        # show_process = False

        # for arg in args:

        #     if arg == "-t":
        #         show_tcp = True

        #     elif arg == "-u":
        #         show_udp = True

        #     elif arg == "-p":
        #         show_process = True

        #     elif arg == "-a":
        #         pass

        #     else:
        #         print("Unknown option")
        #         self._print_usage()
        #         return

        # print("=" * 80)

        # header = (
        #             f"{'PROTO':<10}"
        #             f"{'LOCAL':<25}"
        #             f"{'REMOTE':<25}"
        #             f"{'STATE':<15}"
        # )

        # if show_process:
        #     header += "PROCESS"

        # print(header)

        # print("=" * 80)

        # connections = []
        # try:
        #     for conn in psutil.net_connections():
        #         connections.append((conn, getattr(conn, 'pid', None), None))
        # except psutil.AccessDenied:
        #     for p in psutil.process_iter(['pid', 'name']):
        #         try:
        #             for conn in p.net_connections():
        #                 connections.append((conn, p.info['pid'], p.info['name']))
        #         except (psutil.AccessDenied, psutil.NoSuchProcess):
        #             pass

        # for conn, pid, p_name in connections:

        #     proto = "TCP"

        #     if conn.type == socket.SOCK_DGRAM:
        #         proto = "UDP"

        #     if show_tcp and proto != "TCP":
        #         continue

        #     if show_udp and proto != "UDP":
        #         continue

        #     local = (
        #         f"{conn.laddr.ip}:{conn.laddr.port}"
        #         if conn.laddr
        #         else "-"
        #     )

        #     remote = (
        #         f"{conn.raddr.ip}:{conn.raddr.port}"
        #         if conn.raddr
        #         else "-"
        #     )

        #     state = conn.status

        #     row = (
        #         f"{proto:<10}"
        #         f"{local:<25}"
        #         f"{remote:<25}"
        #         f"{state:<15}"
        #     )

        #     if show_process:

        #         process_name = "Unknown"
                
        #         if p_name:
        #             process_name = p_name
        #         elif pid:
        #             try:
        #                 process_name = psutil.Process(pid).name()
        #             except:
        #                 pass

        #         row += process_name

        #     print(row)



    def traceroute(self, args):
        if not args:
            print("Usage: traceroute <hostname> [-d]")
            return
    
        # Extract the target (first argument that doesn't start with '-')
        target = None
        flags = []
        for arg in args:
            if arg.startswith("-"):
                flags.append(arg)
            elif target is None:
                target = arg

        if not target:
            print("Usage: traceroute <hostname> [-d]")
            return
    
        try:
            if platform.system().lower() == "windows":
                command = ["tracert"] + flags + [target]
            else:
                # 'traceroute' on macOS/Linux uses '-n' for no DNS resolution, but if user inputs '-d', 
                # we can map it or just pass it directly. 'traceroute' uses '-n'.
                if "-d" in flags:
                    flags.remove("-d")
                    flags.append("-n")
                command = ["traceroute"] + flags + [target]
    
            print(f"Tracing the path to {target}... Please wait.\n")
    
            # Run the command and get the output live, combining stdout and stderr
            with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) as process:
                for line in process.stdout:
                    # Print without extra newlines to preserve traceroute's native formatting
                    print(line, end="", flush=True)
                
                process.wait()
                
        except Exception as e:
            print(f"Error: {e}")

    def nslookup(self, args):
        if not args:
            print("Usage: nslookup <hostname>")
            return
        hostname = args[0]
        try:
            if hostname.replace(".", "").isdigit():
                # Reverse lookup
                name = socket.gethostbyaddr(hostname)[0]
                print("=" * 40)
                print(f"Name: {name}")
                print(f"Address: {hostname}")
                print("=" * 40)
            else:
                # Forward lookup
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

    # def nmap(self,args):
        # if not args:
        #     print("Usage: nmap <hostname>")
        #     return 

        # try:
        #     subprocess.run(["nmap"] + args, check=False)

        # except Exception as e:
        #     print(f"Error: {e}")
            