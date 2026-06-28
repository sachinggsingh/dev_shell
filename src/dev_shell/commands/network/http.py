"""HTTP request command."""

import requests


def _print_usage():
    print("""
    curl usage:
      curl <url>                                   # GET request (default)
      curl -X POST <url>                           # POST request
      curl -H "Content-Type: application/json" <url>
    """)


def curl(args):
    if not args or "-h" in args or "--help" in args:
        _print_usage()
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
            url = arg
        else:
            print(f"Unknown option: {arg}")
            _print_usage()
            return
        i += 1

    if not url:
        print("Error: Missing URL")
        _print_usage()
        return

    try:
        response = requests.request(
            method=method, url=url, headers=headers, data=data, timeout=10
        )
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
