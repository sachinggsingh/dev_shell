"""Environment variable commands."""

import os

from ._helpers import section


def env(args):
    """Display environment variables.

    Usage:
      env            Show all environment variables
      env PATH       Show the value of a specific variable
    """
    try:
        if args:
            key = args[0]
            value = os.environ.get(key)
            if value is None:
                print(f"[env] Variable '{key}' not found.")
            else:
                section(f"Environment: {key}")
                print(f"  {value}")
        else:
            section("Environment Variables")
            for key, value in sorted(os.environ.items()):
                print(f"  {key}={value}")

    except Exception as exc:
        print(f"[env] Error: {exc}")
